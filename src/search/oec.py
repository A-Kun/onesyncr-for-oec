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
        self._name = name
        self._names = {name}

        self._declination = ""
        self._rightascension = ""
        self._distance = ""
        self._epoch = ""

        # Childs
        self._stars = {}
        self._planets = {}

    


class Star:
    """Star"""

    def __init__(self, name):
        self._name = name
        self._names = {name}

        self._magB = []
        self._magV = []
        self._magR = []
        self._magI = []
        self._magJ = []
        self._magH = []
        self._magK = []

        self._mass = []
        self._radius = []
        self._temperature = []
        self._age = []
        self._metallicity = []
        self._spectraltype = ""

        # Childs
        self._planets = {}


class Planet:
    """Planet"""
    def __init__(self, name):
        self._name = name
        self._names = {name}

        self._magB = []
        self._magV = []
        self._magR = []
        self._magI = []
        self._magJ = []
        self._magH = []
        self._magK = []

        self._semimajoraxis = []
        self._separation = []
        self._eccentricity = []
        self._periastron = []
        self._longitude = []
        self._meananomaly = []
        self._ascendingnode = []
        self._inclination = []
        self._impactparameter = []
        self._period = []
        self._periastrontime = []
        self._maximumrvtime = []

        self._mass = []
        self._radius = []
        self._temperature = []
        self._age = []
        self._spectraltype = []

        self._discoverymethod = ""
        self._istransiting = ""
        self._description = ""
        self._discoveryyear = ""
        self._lastupdate = ""
        self._spinorbitalalignment = ""
        



def _get_whole(num):
    """(str) -> str
    Return whole units of a string float.
    """

    return num.split(".")[0]


def deg_to_dms(deg):
    """(str) -> str
    Convert a string of decimal degrees into a string of DMS.
    Unit for declination.
    """

    # Calculate deg min sec.
    fdeg = float(deg)
    degree = int(fdeg)
    fmin = (abs(fdeg) - degree) * 60
    minute = int(fmin)
    fsec = (fmin - minute) * 60
    second = int(fsec)

    # Add 0 if number is in single digit.
    sdeg = str(degree) if abs(degree) >= 10  else "0" + str(degree)
    smin = str(minute) if abs(minute) >= 10  else "0" + str(minute)
    ssec = str(second) if abs(second) >= 10  else "0" + str(second)
    
    # Concatenate deg min sec together.
    DMS = sdeg + " " + smin + " " + ssec
    
    # Add positive/negative sign.
    if fdeg > 0:
        return "+" + DMS
    else:
        return "-" + DMS


def deg_to_hms(deg):
    """(str) -> str
    Convert a string of decmial degrees into a string of HMS.
    Used for right ascension.
    """


    fhour = float(deg) / 15
    hour = int(fhour)
    fminute = (fhour - hour) * 60
    minute = int(fminute)
    fsecond = (fminute - minute) * 60
    second = int(fsecond)

    # Add 0 if number is in single digit.
    sH = str(hour) if hour >= 10 else "0" + str(hour)
    sM = str(minute) if minute >= 10 else "0" + str(minute)
    sS = str(second) if second >= 10 else "0" + str(second)

    return sH + " " + sM + " " + sS
