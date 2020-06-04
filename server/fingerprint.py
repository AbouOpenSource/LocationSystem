import math

"""
    Class SimpleFingerprintData holds a fingerprint with simple values samples
    Member location is a location (any kind of location)
    Member sample contains a dictionary whose keys are AP MAC addresse and
        whose values are average RSSI samples
"""
class SimpleFingerprintData():
    
    def __init__(self):
        self.sample = {}
    
    def add(self, mac_addr, rssi):
        if mac_addr not in self.sample:
            self.sample[mac_addr] = float(rssi)

    """
        Function RSSIDistance computes the RSSI distance between self sample
        and another sample as a dictionary whose keys are AP MAC addresses
        and values are RSSI dBm values
    """
    def RSSIDistance(self, sample, rssi_zero=-95.0):

        dst = 0.0
        mac_addresses = set(self.sample.keys()).union(sample.keys())

        for mac_addr in mac_addresses:
            sample_1 = sample.get(mac_addr, rssi_zero)
            sample_2 = self.sample.get(mac_addr, rssi_zero)

            dst += math.pow((sample_2 - sample_1), 2)

        return math.sqrt(dst)


"""
    Class SimpleFingerprint handles a fingerprint list and its useful
    methods.
"""
class SimpleFingerprint():
    def __init__(self):
        self.db = {}

    def add_data(self, location, mac_addr, rssi):
        
        fingerprint_record = self.db.get(location)

        if fingerprint_record is None:
            fingerprint_record = FingerprintRecord()
            self.db[location] = fingerprint_record

        fingerprint_record.add(mac_addr, rssi)

    """
        Function k_closest_in_rssi returns an array with k closest points
        from self.db relative to sample (dict whose keys=AP MACs and values
        are RSSI dBm values)
        Parameter sample is the RSSI sample
        Parameter k is the number of points to select
        Returns a list of (at most) k locations
    """
    def k_closest_in_rssi(self, sample, k):
        dists = []
        for data in self.db.items():
            dists.append((data.location, data.RSSIDistance(sample))) 

        dists.sort(key = lambda x: x[1])

        if len(dists) == 0:
            return []
        
        return [x[0] for x in dists[:k]]

    
    """
        Function closest_in_rssi returns the point from self.db whose RSSI
        distance from sample (sample dict) is shortest
        
        Parameter sample is the RSSI sample
        
        Returns one location
    """
    def closest_in_rssi(self, sample):
        return self.k_closest_in_rssi(sample, 1)[0]
