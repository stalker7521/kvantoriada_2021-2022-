from math import *


class Distance:
    def __init__(self, latitudeMy=0.0, longitudeMy=0.0, latitude2=0.0, longitude2=0.0, earth=6371):
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

    def distance_main(self):
        """length - distance between two points"""
        length = 1000*self.eaR * 2 * asin(sqrt((sin((self.lat1Rad-self.lat2Rad)/2))**2 + cos(self.lat1Rad) * cos(self.lat2Rad)*(sin((self.lon1Rad-self.lon2Rad)/2))**2))
        return length

    def distance_lat(self):
        """length - distance between two points (if lon the same)"""
        length = 1000*self.eaR * 2 * asin(sqrt((sin((self.lat1Rad-self.lat2Rad)/2))**2))
        return length

    def angle(self):
        """This function can be used for finding angel between OY and vector moving (+) for first and forth quadrant"""
        dist_lat = self.distance_lat()
        main_dist = self.distance_main()
        angel = degrees(asin(dist_lat/main_dist))
        if (self.lonMy > self.lon2) and (self.latMy > self.lat2):
            angel = 270 - angel
        elif (self.lonMy < self.lon2) and (self.latMy < self.lat2):
            angel = 90 - angel
        elif (self.lonMy > self.lon2) and (self.latMy < self.lat2):
            angel = 270 + angel
        elif (self.lonMy < self.lon2) and (self.latMy > self.lat2):
            angel = 90 + angel
        elif (self.lonMy > self.lon2) and (self.latMy == self.lat2):
            angel = 270
        elif (self.lonMy < self.lon2) and (self.latMy == self.lat2):
            angel = 90
        elif (self.lonMy == self.lon2) and (self.latMy > self.lat2):
            angel = 180
        elif (self.lonMy == self.lon2) and (self.latMy < self.lat2):
            angel = 0
        return angel
# 56.846312308, 60.597864744, 56.8470502927, 60.599220277 ++++ 56.8470502927, 60.599220277, 56.846312308, 60.597864744
# 1.955199, 21.286198, 2.000503, 21.289058 ++++++ 43.400081, 39.964251, 43.400143, 39.965468
# 1.762074, 20.523258, 1.762042, 20.525658 ++++++
# [(43.400081,39.964251), (43.400585,39.963003), (43.399175,39.963610), (43.398381,39.963590),
# (43.398788,39.964401), (43.399534,39.964645), (43.400143,39.965468)]
d = Distance(43.398579, 39.963314, 43.399089, 39.963656)
print(d.angle())
