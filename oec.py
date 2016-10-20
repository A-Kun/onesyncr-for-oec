"""
Data Structure

System:
 - name
 - declination (+/- dd mm ss)
 - rightascension (hh mm ss)
 - distance (parsec)
 - epoch (BJD)
 {Planet, Star, Binary}
 
 
Binary:
 - name
 - semimajoraxis
 - separation
 - positionangle
 - binary
 - eccentricity
 - periastron
 - longitude
 - meananomoly
 - inclination
 - period
 - transittime
 - periastrontime
 - maximumrvtime
 - magB
 - magV
 - magR
 - magI
 - magJ
 - magH
 - magK
 {Planet, Star, Binary}
 
Star:
 - name
 - mass (solar masses)
 - radius (solar radii)
 - temperature
 - age (Gyr)
 - metallicity (log, relative to solar)
 - spectraltype
 - magB
 - magV
 - magR
 - magI
 - magJ
 - magH
 - magK
 {Planet}

Planet:
 - name
 - semimajoraxis
 - separation
 - eccentricity
 - periastron
 - longitude
 - meananomaly
 - ascendingnode
 - inclination
 - impactparameter
 - period
 - periastrontime
 - maximumrvtime
 - mass
 - radius
 - temperature
 - age
 - spectraltype
 - magB
 - magV
 - magR
 - magI
 - magJ
 - magH
 - magK
 - discoverymethod
 - istransiting
 - description
 - discoveryyear
 - lastupdate
 - spinorbitalalignment

"""


class System:
    """Root container object for a system."""

    def __init__(self, name):
        # Basic Attributes
        self._name = [name]
        self._declination = ""
        self._rightascension = ""
        self._distance = ""
        self._epoch = ""

        # Childs
        self._child = []
        
    def get_star(self, name):
        for item in self._child:
            if item._name == name:
                return item



class CelestialObject:
    """Celestial Object"""
    
    def __init__(self, name):
        self._name = [name]
        self._magB = []
        self._magV = []
        self._magR = []
        self._magI = []
        self._magJ = []
        self._magH = []
        self._magK = []
        self._mag = ["", "", "", "", "", "", ""]


class Planet(CelestialObject):
    """Planet"""
    pass


class Star(CelestialObject):
    """Star"""

    def __init__(self, name):
        CelestialObject.__init__(self, name)
        self._mass = []
        self._radius = []
        self._temperature = []
        self._age = []
        self._metallicity = []
        self._spectraltype = []
        self._planets = []


class Binary(CelestialObject):
    """Binary"""
    pass