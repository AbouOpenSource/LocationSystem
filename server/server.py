from flask import Flask
from flask import request

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

import time
from fingerprint import SimpleFingerprint, SimpleFingerprintData

app = Flask(__name__)

engine = create_engine('sqlite:///rssi.db')
base = declarative_base()
Session = sessionmaker(bind=engine)


class AccessPoint(base):
    __tablename__ = "accesspoint"
    id = Column(Integer, primary_key=True)
    mac_address = Column(String)


class Location(base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)


class Sample(base):
    __tablename__ = "sample"
    ap_id = Column(Integer, ForeignKey("accesspoint.id"))
    source_address = Column(String, nullable=False, primary_key=True)
    timestamp = Column(Float, nullable=False, primary_key=True)
    rssi = Column(Float, nullable=False)
    ap = relationship("AccessPoint", backref="sample")

    def values(self, src, t, _rssi, _ap):
        source_address = src
        timestamp = t
        rssi = _rssi
        ap = _ap


class FingerprintValue(base):
    __tablename__ = "fingerprint_value"
    id = Column(Integer, primary_key=True)
    loc_id = Column(Integer, ForeignKey("location.id"))
    ap_id = Column(Integer, ForeignKey("accesspoint.id"))
    rssi = Column(Float, nullable=False)
    location = relationship("Location", backref="fingerprint_value")
    ap = relationship("AccessPoint", backref="fingerprint_value")


class CalibratingMobile(base):
    __tablename__ = "calibrating_mobile"
    mac_address = Column(String, primary_key=True)
    loc_id = Column(Integer, ForeignKey("location.id"))
    location = relationship("Location", backref="calibrating_mobile")


# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

@app.route("/rssi", methods=['GET', 'POST'])
def rssi():
    """
        TODO: Implement this function
        It receives data from the access points on the path /rssi
        with a parameter ap whose value is the sending AP MAC address
        and a series of pairs XX:XX:XX:XX:XX:XX=-YY.YYYY
        where the X's are the measured devices MAC addresses
        and the Y's are the avg RSSI values for the corresponding
        MAC address over the last second
        You have to put these information in the sqlite3 database
        named rssi.db whose schema can be displayed from the sqlite3
        prompt through the command .schema
        SQL Alchemy ORM classes and initialization are available above
    """

    raw_data = request.args
    print(raw_data)

    ap_addr = raw_data['ap']

    session = Session()
    ap = AccessPoint(mac_address=ap_addr)

    session.add(ap)

    ap2 = session.query(AccessPoint).first()

    for d in raw_data:
        if (d != 'ap'):
            sample = Sample(ap_id=ap2.id, source_address=d, timestamp=time.time(), rssi=raw_data[d], ap=ap2)
            session.add(sample)

    session.commit()
    # print('key is {} and value is {}'.format(d, raw_data[d]))

    calibrating_data = session.query(CalibratingMobile).filter(CalibratingMobile.mac_address == ap2.mac_address)

    for c_data in calibrating_data:
        loc = c_data.location

        all_samples = session.query(Sample).filter(Sample.source_address == ap2.mac_address,
                                                   Sample.timestamp >= (time.time() - 1))

        if (all_samples is not None):
            for sample in all_samples:
                fingerprint_value = FingerprintValue(loc_id=loc.id, ap_id=sample.ap.id, rssi=sample.rssi, location=loc,
                                                     ap=sample.ap)
                session.add(fingerprint_value)

    # confirm the transactions
    # session.commit() 

    # data = request.args.to_dict(flat=False)
    return 'GET \n'


@app.route("/start_calibration", methods=['GET', 'POST'])
def start_calibration():
    """
        TODO: implement this function
        It receives 4 parameters: mac_addr (string), x (float), y (float), and z (float)
        then must trigger 3 tasks:
        (1) Add MAC address and location to table calibrating_mobile
        (2) Find all samples in table sample, and whose source address matches mac_addr
            and whose timestamp is less than 1 second in the past.
            With those samples, insert into table fingerprint_value all entries with
            ap_id matching the AP that forwared the RSSI sample, location the device location
            and RSSI the RSSI from table sample
        (3) In /rssi route: add instructions that process all incoming RSSI samples like
            step (2) when received.
    """
    # Your code here
    session = Session()

    print(request.args)
    raw_data = request.args

    mac_addr = raw_data['mac_addr']
    x = raw_data['x']
    y = raw_data['y']
    z = raw_data['z']

    location = Location(x=x, y=y, z=z)
    print(location)
    # add the location coordinates to the location table
    session.add(location)

    loc = session.query(Location).first()
    print('location is {}'.format(loc.id))

    calibrating_mobile = CalibratingMobile(mac_address=mac_addr, loc_id=loc.id, location=location)
    # add the calibrating data to the table
    session.add(calibrating_mobile)

    all_samples = session.query(Sample).filter(Sample.source_address == mac_addr, Sample.timestamp >= (time.time() - 1))

    if all_samples is not None:
        for sample in all_samples:
            fingerprint_value = FingerprintValue(loc_id=loc.id, ap_id=sample.ap.id, rssi=sample.rssi, location=loc,
                                                 ap=sample.ap)
            session.add(fingerprint_value)

    session.commit()  # confirm the sql transaction

    return "Calibration started."


@app.route("/stop_calibration", methods=['GET', 'POST'])
def stop_calibration():
    """
        TODO: implement this function
        It receives one parameter: mac_addr (string)
        It must delete any calibrating_mobile entry whose mac_address equal parameter mac_addr
    """
    # Your code here
    mac_addr = request.args['mac_addr']
    delete(CalibratingMobile).where(mac_address=mac_addr)

    return "Calibration Stopped"


@app.route("/locate", methods=['GET', 'POST'])
def locate():
    """
        TODO: implement this function
        It receives one parameter: mac_addr (string)
        Must locate the device based on samples less than 1 second old, whose source address equals mac_addr
        These samples are compared to the content of fingerprint_value table
        Use the closest in RSSI algorithm to find a fingerprint sample matching current sample and return its location
    """
    # Your code here
    samples = []
    session = Session()

    mac_addr = request.args['mac_addr']
    raw_samples = session.query(Sample).filter(Sample.source_address == mac_addr, Sample.timestamp >= (time.time() - 1))

    for sample in raw_samples:
        samples.append((
            sample.ap.mac_address,
            sample.rssi
        ))

    samples_dict = dict(samples)

    sample = SimpleFingerprintData()

    for mac_addr, data in samples_dict.items():
        sample.add(mac_addr, data)

    fingerprint = SimpleFingerprint()
    raw_fingerprint_value = session.query(FingerprintValue).all()

    for fingerprint_value in raw_fingerprint_value:
        fingerprint.add_data(
            fingerprint_value.location,
            fingerprint_value.ap.mac_address,
            float(fingerprint_value.rssi)
        )

    if len(fingerprint.db) == 0:
        return "Fingerprint database is empty."

    location = fingerprint.closest_in_rssi(sample)

    if location is None:
        return "Location couldn't be found"

    return "The location calculated is x:{}, y:{} and z:{}".format(location[0], location[1], location[2])
