# Run this code from the eubon root 'python ./GBIF_data/national_summary_stats.py'
# Shapefiles for national locations are taken from: http://thematicmapping.org/downloads/world_borders.php
# Species observations downloaded from GBIF, and summary table produced frome data using prepare_gbif.py
# For countries of interest, identified by ISO3 codes, identify intersecting observations and create summary stats
# Belgium, UK, germany, denmark, italy, spain, portugal, switzerland, Sweeden, Norway, Finland,
# Note,the sjoin operation takes around 50 seconds per country.

import pandas as pd
import geopandas as gpd
from geopandas.tools import sjoin
import shapely
from tqdm import tqdm
from pprint import pprint

# Extract the national shapefile data and pre-processed GBIF data
df = pd.read_csv('./GBIF_data/output.csv')
nations = gpd.read_file('/Users/Ben/Downloads/TM_WORLD_BORDERS-0/TM_WORLD_BORDERS-0.3.shp')

def point_maker(lon, lat):
    """Create Shapley points from decimal lat and long positions"""
    return shapely.geometry.Point(lon, lat)

def species_sightings_in_time(df):
    """Return a dictionary with counts of species sightings per 4 year period,
    (eg from start of year 2000 to end of year 2003).
    Input dataframe should be per country (from the intersect operation)
    """
    d = {}
    year_increment = 3
    for start in [2000, 2004, 2008, 2012]:
        end = start + year_increment
        for species in range(1,9):
            tmp = df[df.species == species]
            tmp = tmp[tmp.year >= start]
            tmp = tmp[tmp.year <= end]
            var_name = 'S{0}_{1}_{2}'.format(species, start, end)
            d[var_name] = len(tmp)
    return d

def extract_specific_order(d, keys, country):
    """Will be iterating over nations, so will need to initially store info
    as such"""
    vals = [country.ISO3.values[0]]
    for key in keys[1:]:     # country key in first place
        vals.append(d[key])
    return vals

rows =[]
points = []
for val in df.values:
    lat, lon, date, year, species = val
    points.append(point_maker(lon,lat))
    rows.append([ date, year, species])

butterfly_obs = gpd.GeoDataFrame(rows, crs={'init':'epsg:4326'},
                                 geometry=points,
                                 columns=['date','year','species'])
# butterfly_obs[0:100].plot() # To preview a subset these observation data
# The coordinates of the observations and countries should be the same
# country.crs == butterfly_obs.crs

keys = ['ISO3','S1_2000_2003','S1_2004_2007','S1_2008_2011','S1_2012_2015','S2_2000_2003',
        'S2_2004_2007','S2_2008_2011','S2_2012_2015','S3_2000_2003','S3_2004_2007',
        'S3_2008_2011','S3_2012_2015','S4_2000_2003','S4_2004_2007','S4_2008_2011',
        'S4_2012_2015','S5_2000_2003','S5_2004_2007','S5_2008_2011','S5_2012_2015',
        'S6_2000_2003','S6_2004_2007','S6_2008_2011','S6_2012_2015','S7_2000_2003','S7_2004_2007',
        'S7_2008_2011','S7_2012_2015','S8_2000_2003','S8_2004_2007','S8_2008_2011','S8_2012_2015']

national_stats = []
iso3_codes = ['BEL','GBR','DEU', 'DNK', 'ITA', 'ESP', 'PRT', 'CHE', 'SWE', 'NOR', 'FIN']
for iso3_code in tqdm(iso3_codes):
    country = nations[nations.ISO3 == iso3_code]
    assert len(country) > 0,'No country shape identified for {0}'.format(iso3_code)
    assert country.crs == butterfly_obs.crs, 'Butterfly/countries in diffrent CRS'
    per_country_sightings = sjoin(butterfly_obs, country, how='inner', op='intersects')
    national_counts_in_time = species_sightings_in_time(per_country_sightings)
    national_stats.append(extract_specific_order(national_counts_in_time, keys, country))
summary_stats = pd.DataFrame(national_stats, columns=keys)
summary_stats.to_csv('./GBIF_data/national_sightings_in_time.csv', index=False)


# ---------------------------
# Note, the above output is not packed efficently. Convert these data to a json
# dictionary with keys {time: {iso3:{S1:x, S2:X,...S8:X}}}
# where time is a string like '2000_2003', and iso3 is a code like 'GBR'
# This can be included directly on the EUBON butterfly vizulisation site,
# with a similar table for the national EuroLST stats. The below does this.

df = pd.read_csv('./GBIF_data/national_sightings_in_time.csv')

d = {}
for start in [2000, 2004, 2008, 2012]:
    end = start + year_increment
    time_string = '{0}_{1}'.format(start, end)
    country_dic = {}
    for country_index in df.index:
        tmp_dic = {}
        species_dic = {}
        for snum in range(1,9):
            df_key = 'S{species}_{time}'.format(species=snum, time=time_string)
            species_dic['S{0}'.format(snum)] = df[df_key][country_index]
        country_dic[df.ISO3[country_index]] = species_dic
    d[time_string] = country_dic

pprint(d)
