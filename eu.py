import csv
import oec


SYSTEMS = {}


def add_system(name, row):
    # Create new System object.
    system = oec.System(name)

    # declination
    
    # rightascension

    # distance & error -/+
    system._distance = [row["star_distance"],
                        row["star_distance_error_min"],
                        row["star_distance_error_max"]]
    
    # epoch????


    # Add star. OR Binary????
    add_star(system, row)

    SYSTEMS[name].append(system)



def add_star(system, row):
    star_name = row["star_name"]
    star = system.get_star(star_name)

    # Create new Star object.
    if not star:
        star = oec.Star(star_name)
        # alternate names
        star_alt_names = row["star_alternate_names"].split(",")
        
        if "" in star_alt_names: star_alt_names.remove("")
        star._name.extend(star_alt_names)
    
        # mass
        star._mass = [row["star_mass"],
                      row["star_mass_error_min"],
                      row["star_mass_error_max"]]
    
        # radius
        star._radius = [row["star_radius"],
                      row["star_radius_error_min"],
                      row["star_radius_error_max"]]
    
        # temperature
        star._temperature = [row["star_teff"],
                      row["star_teff_error_min"],
                      row["star_teff_error_max"]]
    
        # age
        star._age = [row["star_age"],
                      row["star_age_error_min"],
                      row["star_age_error_max"]]
    
        # metallicity
        star._metallicity = [row["star_metallicity"],
                      row["star_metallicity_error_min"],
                      row["star_metallicity_error_max"]]
    
        # spectraltype ???
        star._spectraltype = []
    
        # magB, magV, magR, magI, magJ, magH, magK
        # missing magB and magR
        star._mag[1] = row["mag_v"]
        star._mag[3] = row["mag_i"]
        star._mag[4] = row["mag_j"]
        star._mag[5] = row["mag_h"]
        star._mag[6] = row["mag_k"]

        system._child.append(star)


    add_planet(star, row)


def add_planet(star, row):
    pass



# Call dlcsv to download csvs

csvfile = open('tmp/eu.csv')
reader = csv.DictReader(csvfile)


for row in reader:
    system_name = row['star_name']
    # Check if system exists.
    if system_name not in SYSTEMS:
        SYSTEMS[system_name] = []
        add_system(system_name, row)
    
    

    a = (row.keys())
    if row["# name"] == "Kepler-152 b":
        break


for k, v in row.items():
    print(k, "+++++++++++++++++",  v)
    