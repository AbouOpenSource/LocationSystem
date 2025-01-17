from flask import Flask
from flask import request, jsonify

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

import re
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

    def __init__(self, _mac_address):
        self.mac_address = _mac_address


class Location(base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    
    def __init__(self, _x, _y, _z):
        self.x = _x
        self.y = _y
        self.z = _z


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
    if request.method == 'POST':
        raw_data = request.values
    else:
        raw_data = request.args

    ap_addr = raw_data['ap']

    if not validateMAC(ap_addr):
        return 'AP mac address is not valid.\n'

    print('raw data is \n')
    print(raw_data)

    session = Session()
    ap = session.query(AccessPoint).filter(AccessPoint.mac_address==ap_addr).first()

    if(ap is None):
        ap = AccessPoint(ap_addr)
        session.add(ap)
        session.commit()    

    for d in raw_data:
        if (d != 'ap'):
            if not validateMAC(d):
                return 'MAC address of one of the measured device is not valid.\n'
            sample = Sample(ap_id=ap.id, source_address=d, timestamp=time.time(), rssi=raw_data[d], ap=ap)
            session.add(sample)

    session.commit()
    
    calibrating_data = session.query(CalibratingMobile).filter(CalibratingMobile.mac_address == ap.mac_address).all()

    for c_data in calibrating_data:
        loc = c_data.location

        all_samples = session.query(Sample).filter(Sample.source_address == ap.mac_address).filter(Sample.timestamp >= (time.time() - 1)).all()
        all_samples = session.query(Sample).filter(Sample.source_address == ap.mac_address).all()

        if (all_samples is not None):
            for sample in all_samples:
                fingerprint_value = FingerprintValue(loc_id=loc.id, ap_id=sample.ap.id, rssi=sample.rssi, location=loc, ap=sample.ap)
                session.add(fingerprint_value)

    # confirm the transactions
    session.commit() 
    session.close()

    # data = request.args.to_dict(flat=False)
    return 'RSSI Samples and AP added to database. \n'


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

    if request.method == 'POST':
        raw_data = request.values
    else:
        raw_data = request.args

    mac_addr = raw_data['mac_addr']
    x = raw_data['x']
    y = raw_data['y']
    z = raw_data['z']

    if not validateMAC(mac_addr):
        return 'MAC address is not valid.\n'
    
    session = Session()

    location = Location(x, y, z)

    session.add(location)
    session.commit()

    # print('location is {}'.format(location.id))

    calibrating_mobile = session.query(CalibratingMobile).filter(CalibratingMobile.mac_address==mac_addr).first()
    
    if(calibrating_mobile is not None):
        print('Calibration already running for this address.\n')
    else:    
        calibrating_mobile = CalibratingMobile(mac_address=mac_addr, loc_id=location.id, location=location)
        # add the calibrating data to the table
        session.add(calibrating_mobile)

    all_samples = session.query(Sample).filter(Sample.source_address == mac_addr).filter(Sample.timestamp >= (time.time() - 1)).all()
    # all_samples = session.query(Sample).filter(Sample.source_address == mac_addr).all()
    if all_samples is not None:
        for sample in all_samples:
            fingerprint_value = FingerprintValue(loc_id=location.id, ap_id=sample.ap.id, rssi=sample.rssi, location=location, ap=sample.ap)
            session.add(fingerprint_value)

    session.commit()  # confirm the sql transaction
    session.close()

    return "Calibration started.\n"


@app.route("/stop_calibration", methods=['GET', 'POST'])
def stop_calibration():
    """
        TODO: implement this function
        It receives one parameter: mac_addr (string)
        It must delete any calibrating_mobile entry whose mac_address equal parameter mac_addr
    """
    if request.method == 'POST':   
        mac_addr = request.values['mac_addr']
    else:
        mac_addr = request.args['mac_addr']

    if not validateMAC(mac_addr):
        return 'MAC address is not valid.\n'

    session = Session()	
    session.query(CalibratingMobile).filter(CalibratingMobile.mac_address==mac_addr).delete()
    session.commit()
    session.close()

    return "Calibration Stopped for {}\n".format(mac_addr)


@app.route("/locate", methods=['GET', 'POST'])
def locate():
    """
        TODO: implement this function
        It receives one parameter: mac_addr (string)
        Must locate the device based on samples less than 1 second old, whose source address equals mac_addr
        These samples are compared to the content of fingerprint_value table
        Use the closest in RSSI algorithm to find a fingerprint sample matching current sample and return its location
    """

    if request.method == 'POST':        
        mac_addr = request.values['mac_addr']
    else:
        mac_addr = request.args['mac_addr']
    
    if not validateMAC(mac_addr):
        return 'MAC address is not valid.\n'

    session = Session()

    raw_samples = session.query(Sample).filter(Sample.source_address == mac_addr).filter(Sample.timestamp >= (time.time() - 1)).all()
    # raw_samples = session.query(Sample).filter(Sample.source_address == mac_addr).all()

    # for sample in raw_samples:
    #     samples.append((
    #         sample.ap.mac_address,
    #         sample.rssi
    #     ))

    samples_dict = {} 
    for sample in raw_samples:
        if(sample.source_address in samples_dict):
            tr = samples_dict[sample.source_address]
            tr[0] += sample.rssi
            tr[1] += 1
        else:
            samples_dict[sample.source_address] = [sample.rssi, 1]

    sample = SimpleFingerprintData()

    # for mac_addr, data in samples_dict.items():
    #     sample.add(mac_addr, data)

    for mac, val in samples_dict.items(): # To add datas to sample_fingerprint dictionnary for the location
        sample.add(mac, val[0]/val[1])


    fingerprint = SimpleFingerprint()
    raw_fingerprint_value = session.query(FingerprintValue).all()

    print('raw fingerprint data is \n')
    print(raw_fingerprint_value)

    for fingerprint_value in raw_fingerprint_value:
        fingerprint.add_data(
            fingerprint_value.location,
            fingerprint_value.ap.mac_address,
            float(fingerprint_value.rssi)
        )

    if len(fingerprint.db) == 0:
        return "Fingerprint database is empty.\n"

    location = fingerprint.closest_in_rssi(sample)

    print('location is \n')
    print(location)

    if location is None:
        return "Location couldn't be found\n"

    print('x:{}\ny:{}\nz:{}\n'.format(location.x, location.y, location.z))
    # return 'good\n'
    return "The location calculated is x:{}, y:{} and z:{}\n".format(location.x, location.y, location.z)


def validateMAC(mac):
    if re.match("^(([a-fA-F0-9]{2}-){5}[a-fA-F0-9]{2}|([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}|([0-9A-Fa-f]{4}.){2}[0-9A-Fa-f]{4})?$", mac.lower()):
        return True
    else:
        return False
