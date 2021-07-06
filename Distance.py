from math import *


class Distance:
    def __init__(self, latitudeMy=0, longitudeMy=0, latitude2=0, longitude2=0, earth=6371):
        """Rad - means angel in radians, earth - means radius of Earth"""
        self.latMy = latitudeMy
        self.lonMy = longitudeMy
        self.lat2 = latitude2
        self.lon2 = longitude2
        self.eaR = earth
        self.lat1Rad = radians(self.latMy)
        self.lon1Rad = radians(self.lonMy)
        self.lat2Rad = radians(self.lat2)
        self.lon2Rad = radians(self.lon2)

    def radians(self):
        return {"lat1": self.lat1Rad, "lon1": self.lon1Rad, "lat2": self.lat2Rad, "lon2": self.lon2Rad}

    def distance(self):
        """length - distance between two points"""
        length = self.eaR * 2 * asin(sqrt((sin((self.lat1Rad-self.lat2Rad)/2))**2 + cos(self.lat1Rad) * cos(self.lat2Rad)*(sin((self.lon1Rad-self.lon2Rad)/2))**2))
        return length

    def angle(self):
        """This function can be used for finding angel between OY and vector moving (+) for first and forth quadrant"""
        local_lat = self.lat2 - self.latMy
        angel = 90 - asin(local_lat/self.distance())
        if self.lonMy > self.lon2:
            angel *= -1
        return angel