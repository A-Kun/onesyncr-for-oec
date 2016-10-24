import csv
import oec


# Global dictionary for all systems.
SYSTEMS = {}


def add_system(name, row):
    # Create new System object.
    system = oec.System(name)

    # declination
    system._declination = oec.deg_to_dms(row["dec"])
    
    # rightascension
    system._rightascension = oec.deg_to_hms(row["ra"])

    # distance & error -/+
    system._distance.extend([row["st_dist"],
                        row["st_disterr2"][1:],
                        row["st_disterr1"]])
    
    # epoch????


    SYSTEMS[name] = system



def add_star(system, row):
    star_name = row["pl_hostname"]

    star = oec.Star(star_name)



    # mass
    star._mass.extend([row["st_mass"],
                  row["st_masserr2"][1:],
                  row["st_masserr1"]])

    # radius
    star._radius.extend([row["st_rad"],
                  row["st_raderr2"][1:],
                  row["st_raderr1"]])

    # temperature
    star._temperature.extend([row["st_teff"],
                  row["st_tefferr2"][1:],
                  row["st_tefferr1"]])

    # age
    star._age.extend([row["st_age"],
                  row["st_ageerr2"][1:],
                  row["st_ageerr1"]])

    # metallicity
    star._metallicity.extend([row["st_metfe"],
                  row["st_metfeerr2"][1:],
                  row["st_metfeerr1"]])

    # spectraltype
    star._spectraltype = row["st_spstr"]

    # magB, magV, magR, magI, magJ, magH, magK
    star._magB.extend([])
    star._magV.extend([row["st_vj"], row["st_vjerr"], row["st_vjerr"]])
    star._magR.extend([row["st_rc"], row["st_rcerr"], row["st_rcerr"]])
    star._magI.extend([row["st_ic"], row["st_icerr"], row["st_icerr"]])
    star._magJ.extend([row["st_j"], row["st_jerr"], row["st_jerr"]])
    star._magH.extend([row["st_h"], row["st_herr"], row["st_herr"]])
    star._magK.extend([row["st_k"], row["st_kerr"], row["st_kerr"]])

    # Add star into System.
    system._stars[star_name] = star


def add_planet(system, row):
    planet_name = row["pl_name"]

    planet = oec.Planet(planet_name)
    
    # alternate names
    planet._names.add(row["hd_name"])
    planet._names.add(row["hip_name"])
    # remove empty strings
    if "" in planet._names:
        planet._names.remove("")
    
    # mass
    if row["pl_massj"]:
        planet._mass.extend([row["pl_massj"],
                        row["pl_massjerr2"][1:],
                        row["pl_massjerr1"]])
    else:
        planet._mass.extend([row["pl_msinij"],
                        row["pl_msinijerr2"][1:],
                        row["pl_msinijerr1"]])

    # radius
    planet._radius.extend([row["pl_radj"],
                      row["pl_radjerr2"][1:],
                      row["pl_radjerr1"]])
    
    # temperature
    planet._temperature.extend([row["pl_eqt"],
                           row["pl_eqterr2"][1:],
                           row["pl_eqterr1"]])
    # age
    
    # spectraltype

    # semimajoraxis
    planet._semimajoraxis.extend([row["pl_orbsmax"],
                             row["pl_orbsmaxerr2"][1:],
                             row["pl_orbsmaxerr1"]])

    # seperation
    
    # eccentricity
    planet._eccentricity.extend([row["pl_orbeccen"],
                            row["pl_orbeccenerr2"][1:],
                            row["pl_orbeccenerr1"]])
    
    # periastron
    planet._periastron.extend([row["pl_orblper"],
                          row["pl_orblpererr2"][1:],
                          row["pl_orblpererr1"]])
    
    # longitude
    
    # meananomaly
    
    # ascendingnode
    
    # inclination
    planet._inclination.extend([row["pl_orbincl"],
                           row["pl_orbinclerr2"][1:],
                           row["pl_orbinclerr1"]])
    
    # impactperameter
    
    # period
    planet._period.extend([row["pl_orbper"],
                      row["pl_orbpererr2"][1:],
                      row["pl_orbpererr1"]])
    
    # periastrontime
    planet._periastrontime.extend([row["pl_orbper"],
                              row["pl_orbpererr2"][1:],
                              row["pl_orbpererr1"]])
    
    # maximumrvtime
    
    # discoverymethod
    planet._discoverymethod = row["pl_discmethod"]
    
    # istransiting
    
    # description
    
    # discoveryyear
    planet._discoveryyear = row["pl_disc"]
    
    # lastupdate
    planet._lastupdate = row["rowupdate"]
    
    # spinorbitalalignment

    system._planets[planet_name] = planet
    system._stars[row["pl_hostname"]]._planets[planet_name] = planet



def get_nasa():
    # Read until header of file. *** optimize later ***
    csvfile = open('tmp/nasa2.csv')
    line = csvfile.readline()
    while(line.startswith("# ")):
        line = csvfile.readline()
    line = csvfile.readline()
    while(line.startswith("# ")):
        line = csvfile.readline()

    reader = csv.DictReader(csvfile)
    
    for row in reader:
        system_name = row["pl_hostname"]
        star_name = row["pl_hostname"]
        planet_name = row["pl_name"]
    
        # Create new system if system does not exit.
        if system_name not in SYSTEMS:
            add_system(system_name, row)
    
        # Create new star if star does not exit.    
        if star_name not in SYSTEMS[system_name]._stars:
            add_star(SYSTEMS[system_name], row)
        
        
        # Create new planet.
        add_planet(SYSTEMS[system_name], row)


    csvfile.close()
