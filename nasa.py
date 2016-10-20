import csv
import oec


SYSTEMS = {}

def add_system(name, data):
    """(str, dict of str) -> NoneType
    Add a new system object into global systems dictionary.
    """
    # Check if system exists.
    if name not in SYSTEMS:
        # If not, create new system.
        SYSTEMS[name] = []

    # If system exists, add planet into system.
    system = oec.System(name)

    dec = data["dec_str"].replace("d", " ").replace("m", " ").replace("s", "")
    ## Not sure if round up or down
    system.declination = dec.split(".")[0]

    ra = data["ra_str"].replace("h", " ").replace("m", " ").replace("s", "")
    ## Round up or down???
    system.rightascension = ra.split(".")[0]

    ## no distance found...
    system.distance = data["st_dist"]
    system.distance_error = [data["st_disterr1"], data["st_disterr2"]]


    SYSTEMS[name].append(system)


def add_star(name, data):
    """(str, dict of str) -> NoneType
    Add a new Star object into a Syteam object.
    """
    # Create new Star object.
    star = oec.Star(name)

    star.radius = data["st_rad"]
    star.radius_error = [data["st_raderr1"], data["st_raderr2"]]

    star.temperature = data["st_teff"]
    star.temperature_errpr = [data["st_tefferr1"], data["st_tefferr2"]]

    
    SYSTEMS[name].stars.append(star)


def add_planet(name, data):
    """(str, dict of str) -> NoneType
    Add a new Planet object into a Star object.
    """
    pass


# Call dlcsv to download csvs here




# Open NASA Exoplanet Archive CSV.
csvfile = open('tmp/nasa.csv')
reader = csv.DictReader(csvfile)


for row in reader:
    # Add system.
    add_system(row["pl_hostname"], row)
    # Add star.
    add_star(row["pl_hostname"], row)
    # Add planet.
    add_planet(row["pl_letter"], row)

    print(row['pl_hostname'], row['pl_letter'])
    break



print(systems)