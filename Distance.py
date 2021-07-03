from math import *


class Distance:
    def __init__(self, latitude1=0, longitude1=0, latitude2=0, longitude2=0, earth=6371):
        """Rad - means angel in radians, earth - means radius of Earth"""
        self.lat1 = latitude1
        self.lon1 = longitude1
        self.lat2 = latitude2
        self.lon2 = longitude2
        self.eaR = earth
        self.lat1Rad = radians(self.lat1)
        self.lon1Rad = radians(self.lon1)
        self.lat2Rad = radians(self.lat2)
        self.lon2Rad = radians(self.lon2)

    def radians(self):
        return {"lat1": self.lat1Rad, "lon1": self.lon1Rad, "lat2": self.lat2Rad, "lon2": self.lon2Rad}

    def distance(self):
        """length - distance between two points"""
        length = self.eaR * 2 * asin(sqrt((sin((self.lat1Rad-self.lat2Rad)/2))**2 + cos(self.lat1Rad) * cos(self.lat2Rad)*(sin((self.lon1Rad-self.lon2Rad)/2))**2))
        return length

    def angle(self):
        """latitude = OY; longitude = OX (возможно надо брать в рабианах)"""
        dtX = self.lat2 - self.lat1
        dtY = self.lon2 - self.lon1
        angel = dtY/dtX
        return angel