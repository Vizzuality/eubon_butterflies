# Shapefiles for national locations are taken from: http://thematicmapping.org/downloads/world_borders.php
# EUROLST BIOCLIM DATA DOWNLOADED FROM https://courses.neteler.org/eurolst-seamless-gap-free-daily-european-maps-land-surface-temperatures/
# For countries of interest, identified by ISO3 codes, extract raster information
# from intersections between a BIOCLIM EuroLST tif file, and national vectors.
# Belgium, UK, germany, denmark, italy, spain, portugal, switzerland, Sweeden, Norway, Finland,

import pandas as pd
import geopandas as gpd
from rasterstats import zonal_stats
import rasterio
import pyproj
from tqdm import tqdm

# Point to the uncompressed BIOCLIM file below and national shapefile data
input_raster = "/Users/Ben/Downloads/eurolst_clim/eurolst_clim.bio01.tif"
nations = gpd.read_file('/Users/Ben/Downloads/TM_WORLD_BORDERS-0/TM_WORLD_BORDERS-0.3.shp')
eurolst_key = input_raster.split('.')[-2]
eurolst_multiplier = {'bio01': 10, 'bio04':100, 'bio05':10, 'bio06':10,
                      'bio10': 10, 'bio11':10}

def unpack_result(d, country):
    """Extract dictionary results from rasterstats zonal_stats output and
    return in csv format. Division by a magnitude in the eurolst_multiplier
    dictionary is due to the data packing, and based on values from the website
    link given above."""
    count = d['count']
    max = d['max'] / eurolst_multiplier.get(eurolst_key, 1)
    mean = d['mean'] / eurolst_multiplier.get(eurolst_key, 1)
    mean = float('{0:4.2f}'.format(mean))
    min = d['min'] / eurolst_multiplier.get(eurolst_key, 1)
    name = country['NAME'].values[0]
    iso3 = country['ISO3'].values[0]
    return [iso3, name, min, mean, max]

with rasterio.open(input_raster, blockxsize=256, blockysize=256) as inData:
    profile = inData.profile
    meta = inData.meta
tif_projection = profile['crs']['proj']
print("TIF projection in {0}".format(pyproj.pj_list[tif_projection]))
# Based on http://spatialreference.org/ref/?search=laea&srtext=Search
# Lambert Equal Area Projection is epsg="3035". We can use this code to repoject
# the national polygons.

national_stats = []
iso3_codes = ['BEL','GBR','DEU', 'DNK', 'ITA', 'ESP', 'PRT', 'CHE', 'SWE', 'NOR', 'FIN']
for iso3_code in tqdm(iso3_codes):
    country = nations[nations.ISO3 == iso3_code]
    assert len(country) > 0,'No country shape identified for {0}'.format(iso3_code)
    country_raster = zonal_stats(country.to_crs(epsg="3035"), input_raster,
                                 band=1, all_touched=True, raster_out=True)
    #plt.imshow(country_raster[0]['mini_raster_array']) # to visually verify the
    #plt.show()                      # right part of the array has been isolated
    national_stats.append(unpack_result(country_raster[0], country))

df = pd.DataFrame(national_stats, columns=['ISO3','NAME', eurolst_key+'_MIN',
                                           eurolst_key+'_MEAN', eurolst_key+'_MAX'])
df.to_csv('./national_stats.csv', index=False)
print("Program finished normally.")


# --- To Extract these data in a JSON based structure ----
from pprint import pprint
nstats = pd.read_csv('./eurolst_process/national_stats.csv')
dic = {}
for iso3 in nstats.ISO3:
    minval = float('{0:4.2f}'.format(nstats[nstats.ISO3 == iso3].bio01_MIN.values[0]))
    maxval = float('{0:4.2f}'.format(nstats[nstats.ISO3 == iso3].bio01_MAX.values[0]))
    meanval = float('{0:4.2f}'.format(nstats[nstats.ISO3 == iso3].bio01_MEAN.values[0]))
    dic[iso3] = {'min': minval, 'mean': meanval,'max': maxval}
pprint(dic)
