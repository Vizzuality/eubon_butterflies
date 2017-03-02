## EUBON Butterfly visualisation project

[Basic demo](http://bl.ocks.org/benlaken/9fc0db2e992a24267a5bc48936d9e926) of raw data displayed on web-map using carto.js.


### Summary

We designed this project to showcase the [EuroLST data](http://www.geodati.fmach.it/eurolst.html),
using the narrative of butterfly observations across Europe. We will need to use the Euro LST data as a basemap, and overlay vectors based on
butterfly observations from [GBIF](http://www.gbif.org). We can make these data comparable (at least in a qualitative manner) in both space (i.e. across areas or national averages) and time (i.e. over temporal bins of 4 years) by calculating **relative proportions**: *i.e. for each area we can calculate the relative percentage of butterfly seen that were of a given type*. We will do this with pre-processing, calculating some national-level statisticsics in advance (uising the software in this repo), and uploading these (csv) tables and basemap raster (tif) to carto.

Aggregated, this data should show 1) how relative abundance changes in space, and 2) if changes in relative abundance have occurred in time (during the last 16 years of EurLST data for which we will construct co-temporal analysis). We will also show for the area averaged abundance the temperature anomaly detected from EurLST over this time.

Features to note:
* Observer effect: A strong country dependence is evident in the data, which relates to prevalence of observers in different countries. These raw data  mainly reflect where observers are, and so must be turned in to relative abundance before comparing in time and space.
* Variability: (In temperature data) we will try to minimise this volatility by presenting data in 4-year blocks. This will also help with scarcity of butterfly observations, and the considerable size of the EurLST data.
* Trends: Actual trends in population range may occur with changes in climate, as insects respond rapidly to environmental change. The data may indeed reflect this, but we should note the qualitative nature of this association due to the limits of interpreting these data. The trends may be distinct for butterflies that migrate vs those which do not (we have selected both types).


#### Relative abundance *vs.* counts
 If a given area shows 10 observations (10 counts), 5 of butterfly type 1, 3 of butterfly type 2, and 2 of butterfly type 3, then the relative abundance is 50%, 30% and 20% respectively. Doing this will enable us to generalise over time and space, despite the widely different sampling frequency. Therefore only difference a higher-sampling frequency will have, is to increase the accuracy of the estimate.
We have calculated a table of national-level statistics with count per species over a four-year-period. These should be converted to relative abandance in the front-end, depending on what species a user is interested in.


## Data

### Butterfly observations

We will use observations of several different butterfly species, [prepared and loaded into a Carto table](https://benlaken.carto.com/dataset/butterfly_sightings):

* [Vanessa Atalanta Linnaeus, 1758](http://www.gbif.org/species/1898286): taxonomy code 1898286, category 1 in the Carto table
* [Vanessa Pieris Napi (Linnaeus, 1758)](http://www.gbif.org/species/1920494): taxonomy code 1920494, category 2 in the Carto table
* [Vanessa Pieris Brassicae (Linnaeus, 1758)](http://www.gbif.org/species/1920506): taxonomy code 1920506, category 3 in the Carto table
* [Nymphalis xanthomelas](http://www.gbif.org/species/5130587) taxonomy code 5130587, category 4 in the Carto table
* [Vanessa cardui](http://www.gbif.org/species/4299368): taxonomy code 4299368, category 5 in Carto table
* [Araschnia levana Linneaus, 1758](http://www.gbif.org/species/1902533) taxonomy code 1902533, category 6 in the Carto table
* [Apatura ilia Denis & Schiffermüller, 1775](http://www.gbif.org/species/8138711) taxonomy code 8138711, category 7 in the Carto table
* [Apatura iris Linnaeus, 1758](http://www.gbif.org/species/5131910) taxonomy code 5131910, category 8 in the Carto table

# visualisation components

The components of this visualisation are:

1. Map, with base layer of minified EuroLST data, and over-plotted butterfly point observations.
  * EuroLST data is too large to display in full, and butterfly data is too patchy display at high-frequency.
  Thus 4 year temperature anomalies, with 4-year groupings of butterfly observations could work well.
  Covering periods of 200-2003, 2004-2007, 2008-2011, 2012-2015.
1. National level summary statistics displayed as a widget.
  * Country-level relative abundance of observations over time (2000-2004, 2005-2008, 2009-2012, 2013-2016) per species, and also averages over the EuroLST data per country for the same times.
1. Map Widget (*low priority*):
  * User could click on the map and return a widget displaying relative abundance of a given species over a buffered area.
1. Feed of most recent butterfly observations in GBIF database (*low priority, and probably not needed*):
  * Using the RESTFUL API of GBIF, we can request butterfly data for the species we desire, over Europe,
  which contains photos, and display the most recent observations only, to assist in building the narrative of this being a project based in citizen science.

## 1. Map

### Map demo/SQL for returning butterfly observation data

We have created a small prototype version of a map using Carto.js to expose butterfly and EuroLST example data, leaving examples of the settings that can be used to build the website.

* Python server: cd into `./simple_server` and execute `./start.sh`. The map should be viewable at [http://0.0.0.0:8000](http://0.0.0.0:8000). Alternativley, you can view a [version running on bl.ocks.org](http://bl.ocks.org/benlaken/9fc0db2e992a24267a5bc48936d9e926).


## 2. National Level Statistics

For our use case, we have pre-processed the butterfly observations, and EUROLST
raster data using national boundary shapefiles and produced summary statistics in
simple JSON format which can be used to create a widget or summary plot. The results of
this processing is below, and can be directly embedded into the website code.

```bash
iso3_to_name = {'BEL':'Belgium',
                'GBR':'United Kingdom',
                'DEU':'Germany',
                'DNK':'Denmark',
                'ITA':'Italy',
                'ESP':'Spain',
                'PRT':'Portugal',
                'CHE':'Switzerland',
                'SWE':'Sweden',
                'NOR','Norway',
                'FIN','Finland'}

# Mean National temperature from EUROLST BIO01 data
euroLST_bio01 = {'BEL': {'max': 12.2, 'mean': 10.03, 'min': 7.1},
                 'CHE': {'max': 14.6, 'mean': 6.14, 'min': -9.7},
                 'DEU': {'max': 12.5, 'mean': 8.98, 'min': -0.7},
                 'DNK': {'max': 9.3, 'mean': 7.75, 'min': 6.6},
                 'ESP': {'max': 22.6, 'mean': 16.08, 'min': -0.8},
                 'FIN': {'max': 5.4, 'mean': -0.18, 'min': -5.8},
                 'GBR': {'max': 12.6, 'mean': 8.56, 'min': 2.5},
                 'ITA': {'max': 21.4, 'mean': 13.98, 'min': -9.9},
                 'NOR': {'max': 8.0, 'mean': 0.09, 'min': -8.4},
                 'PRT': {'max': 21.9, 'mean': 17.2, 'min': 10.9},
                 'SWE': {'max': 8.7, 'mean': 1.27, 'min': -8.8}}


# Butterfly Counts per-year group, per-country, per-species
butterfly_obs = {'2000_2003': {'BEL': {'S1': 13602,
                                       'S2': 8369,
                                       'S3': 8269,
                                       'S4': 0,
                                       'S5': 8791,
                                       'S6': 6038,
                                       'S7': 0,
                                       'S8': 5},
                               'CHE': {'S1': 1514,
                                       'S2': 2540,
                                       'S3': 974,
                                       'S4': 0,
                                       'S5': 1859,
                                       'S6': 385,
                                       'S7': 22,
                                       'S8': 96},
                               'DEU': {'S1': 241,
                                       'S2': 297,
                                       'S3': 214,
                                       'S4': 0,
                                       'S5': 181,
                                       'S6': 125,
                                       'S7': 5,
                                       'S8': 15},
                               'DNK': {'S1': 77,
                                       'S2': 6,
                                       'S3': 21,
                                       'S4': 2,
                                       'S5': 195,
                                       'S6': 188,
                                       'S7': 0,
                                       'S8': 32},
                               'ESP': {'S1': 0,
                                       'S2': 13,
                                       'S3': 3,
                                       'S4': 0,
                                       'S5': 3,
                                       'S6': 0,
                                       'S7': 1,
                                       'S8': 1},
                               'FIN': {'S1': 930,
                                       'S2': 2279,
                                       'S3': 283,
                                       'S4': 2,
                                       'S5': 493,
                                       'S6': 106,
                                       'S7': 3,
                                       'S8': 39},
                               'GBR': {'S1': 4135,
                                       'S2': 2668,
                                       'S3': 4129,
                                       'S4': 0,
                                       'S5': 2579,
                                       'S6': 0,
                                       'S7': 0,
                                       'S8': 3},
                               'ITA': {'S1': 8,
                                       'S2': 12,
                                       'S3': 13,
                                       'S4': 0,
                                       'S5': 13,
                                       'S6': 0,
                                       'S7': 1,
                                       'S8': 1},
                               'NOR': {'S1': 42,
                                       'S2': 55,
                                       'S3': 9,
                                       'S4': 0,
                                       'S5': 32,
                                       'S6': 0,
                                       'S7': 0,
                                       'S8': 0},
                               'PRT': {'S1': 0,
                                       'S2': 1,
                                       'S3': 7,
                                       'S4': 0,
                                       'S5': 13,
                                       'S6': 0,
                                       'S7': 1,
                                       'S8': 0},
                               'SWE': {'S1': 532,
                                       'S2': 1196,
                                       'S3': 670,
                                       'S4': 0,
                                       'S5': 38,
                                       'S6': 93,
                                       'S7': 0,
                                       'S8': 24}},
                 '2004_2007': {'BEL': {'S1': 27260,
                                       'S2': 14999,
                                       'S3': 19407,
                                       'S4': 0,
                                       'S5': 8703,
                                       'S6': 4668,
                                       'S7': 0,
                                       'S8': 30},
                               'CHE': {'S1': 2129,
                                       'S2': 2454,
                                       'S3': 1561,
                                       'S4': 0,
                                       'S5': 1817,
                                       'S6': 422,
                                       'S7': 53,
                                       'S8': 203},
                               'DEU': {'S1': 271,
                                       'S2': 347,
                                       'S3': 281,
                                       'S4': 0,
                                       'S5': 132,
                                       'S6': 156,
                                       'S7': 14,
                                       'S8': 15},
                               'DNK': {'S1': 1234,
                                       'S2': 379,
                                       'S3': 330,
                                       'S4': 1,
                                       'S5': 715,
                                       'S6': 410,
                                       'S7': 0,
                                       'S8': 98},
                               'ESP': {'S1': 0,
                                       'S2': 6,
                                       'S3': 1,
                                       'S4': 0,
                                       'S5': 4,
                                       'S6': 0,
                                       'S7': 2,
                                       'S8': 0},
                               'FIN': {'S1': 1367,
                                       'S2': 3038,
                                       'S3': 494,
                                       'S4': 19,
                                       'S5': 722,
                                       'S6': 397,
                                       'S7': 76,
                                       'S8': 209},
                               'GBR': {'S1': 6490,
                                       'S2': 4132,
                                       'S3': 6292,
                                       'S4': 0,
                                       'S5': 2453,
                                       'S6': 0,
                                       'S7': 0,
                                       'S8': 23},
                               'ITA': {'S1': 18,
                                       'S2': 17,
                                       'S3': 37,
                                       'S4': 0,
                                       'S5': 29,
                                       'S6': 0,
                                       'S7': 0,
                                       'S8': 6},
                               'NOR': {'S1': 130,
                                       'S2': 80,
                                       'S3': 26,
                                       'S4': 0,
                                       'S5': 70,
                                       'S6': 0,
                                       'S7': 0,
                                       'S8': 0},
                               'PRT': {'S1': 0,
                                       'S2': 0,
                                       'S3': 0,
                                       'S4': 0,
                                       'S5': 2,
                                       'S6': 0,
                                       'S7': 0,
                                       'S8': 0},
                               'SWE': {'S1': 4641,
                                       'S2': 7565,
                                       'S3': 3623,
                                       'S4': 18,
                                       'S5': 53,
                                       'S6': 796,
                                       'S7': 0,
                                       'S8': 135}},
                 '2008_2011': {'BEL': {'S1': 25500,
                                       'S2': 16559,
                                       'S3': 13734,
                                       'S4': 0,
                                       'S5': 16163,
                                       'S6': 7834,
                                       'S7': 3,
                                       'S8': 89},
                               'CHE': {'S1': 941,
                                       'S2': 1509,
                                       'S3': 888,
                                       'S4': 0,
                                       'S5': 2852,
                                       'S6': 539,
                                       'S7': 29,
                                       'S8': 112},
                               'DEU': {'S1': 3057,
                                       'S2': 2713,
                                       'S3': 2323,
                                       'S4': 0,
                                       'S5': 2542,
                                       'S6': 1398,
                                       'S7': 116,
                                       'S8': 190},
                               'DNK': {'S1': 406,
                                       'S2': 382,
                                       'S3': 292,
                                       'S4': 1,
                                       'S5': 257,
                                       'S6': 386,
                                       'S7': 1,
                                       'S8': 118},
                               'ESP': {'S1': 59,
                                       'S2': 40,
                                       'S3': 47,
                                       'S4': 0,
                                       'S5': 42,
                                       'S6': 4,
                                       'S7': 4,
                                       'S8': 9},
                               'FIN': {'S1': 3341,
                                       'S2': 6020,
                                       'S3': 584,
                                       'S4': 14,
                                       'S5': 1902,
                                       'S6': 690,
                                       'S7': 344,
                                       'S8': 360},
                               'GBR': {'S1': 5726,
                                       'S2': 4978,
                                       'S3': 7769,
                                       'S4': 0,
                                       'S5': 3129,
                                       'S6': 0,
                                       'S7': 0,
                                       'S8': 47},
                               'ITA': {'S1': 68,
                                       'S2': 43,
                                       'S3': 53,
                                       'S4': 0,
                                       'S5': 115,
                                       'S6': 1,
                                       'S7': 0,
                                       'S8': 2},
                               'NOR': {'S1': 1220,
                                       'S2': 1439,
                                       'S3': 328,
                                       'S4': 0,
                                       'S5': 518,
                                       'S6': 0,
                                       'S7': 0,
                                       'S8': 0},
                               'PRT': {'S1': 0,
                                       'S2': 2,
                                       'S3': 3,
                                       'S4': 0,
                                       'S5': 1,
                                       'S6': 0,
                                       'S7': 0,
                                       'S8': 0},
                               'SWE': {'S1': 4622,
                                       'S2': 8403,
                                       'S3': 2926,
                                       'S4': 48,
                                       'S5': 98,
                                       'S6': 1881,
                                       'S7': 14,
                                       'S8': 340}},
                 '2012_2015': {'BEL': {'S1': 29679,
                                       'S2': 15382,
                                       'S3': 10436,
                                       'S4': 5,
                                       'S5': 6365,
                                       'S6': 11263,
                                       'S7': 0,
                                       'S8': 197},
                               'CHE': {'S1': 21,
                                       'S2': 2,
                                       'S3': 1,
                                       'S4': 0,
                                       'S5': 9,
                                       'S6': 0,
                                       'S7': 0,
                                       'S8': 0},
                               'DEU': {'S1': 8104,
                                       'S2': 5519,
                                       'S3': 3501,
                                       'S4': 11,
                                       'S5': 2279,
                                       'S6': 3692,
                                       'S7': 340,
                                       'S8': 246},
                               'DNK': {'S1': 888,
                                       'S2': 1578,
                                       'S3': 866,
                                       'S4': 260,
                                       'S5': 291,
                                       'S6': 429,
                                       'S7': 57,
                                       'S8': 212},
                               'ESP': {'S1': 471,
                                       'S2': 130,
                                       'S3': 427,
                                       'S4': 0,
                                       'S5': 479,
                                       'S6': 26,
                                       'S7': 32,
                                       'S8': 14},
                               'FIN': {'S1': 1824,
                                       'S2': 3763,
                                       'S3': 141,
                                       'S4': 1312,
                                       'S5': 582,
                                       'S6': 929,
                                       'S7': 385,
                                       'S8': 324},
                               'GBR': {'S1': 6606,
                                       'S2': 5137,
                                       'S3': 9295,
                                       'S4': 12,
                                       'S5': 2068,
                                       'S6': 0,
                                       'S7': 0,
                                       'S8': 71},
                               'ITA': {'S1': 95,
                                       'S2': 8,
                                       'S3': 18,
                                       'S4': 0,
                                       'S5': 41,
                                       'S6': 0,
                                       'S7': 7,
                                       'S8': 1},
                               'NOR': {'S1': 1667,
                                       'S2': 1245,
                                       'S3': 240,
                                       'S4': 26,
                                       'S5': 541,
                                       'S6': 0,
                                       'S7': 0,
                                       'S8': 0},
                               'PRT': {'S1': 9,
                                       'S2': 0,
                                       'S3': 5,
                                       'S4': 0,
                                       'S5': 4,
                                       'S6': 0,
                                       'S7': 0,
                                       'S8': 0},
                               'SWE': {'S1': 3751,
                                       'S2': 5415,
                                       'S3': 1479,
                                       'S4': 1040,
                                       'S5': 548,
                                       'S6': 1207,
                                       'S7': 2,
                                       'S8': 551}}}

```

To reproduce these data run `python ./eurolst_process/gen_national_table.py` and
`python ./GBIF_data/national_summary_stats.py`.


## 3. Map Widget (low priority)

If the decimal latitude and longitude can be passed to ST_POINT() function, with a given buffer (in decimal degrees), the following API call will return JSON containing the counts per species seen over a given area in a given time-period, which can be used to create a simple widget for display.

Note below, Lat = -0.032958984375, Lon = 51.5429188223739), and the buffer = 0.5. Also note the user account (below = benlaken) and table name (below = butterfly_sightings) may be different.

CARTO API GET request:

```html
https://benlaken.carto.com/api/v2/sql/?q=SELECT count(species), species FROM butterfly_sightings WHERE st_intersects(the_geom, ST_Buffer(st_setsrid(ST_point(-0.032958984375, 51.5429188223739),4326), 0.5)) AND year > 2009 AND year < 2016  group by species
```

This will return JSON in the form of:

```json
{
  "rows": [
    {
      "count": 3,
      "species": 1
    },
    {
      "count": 2,
      "species": 2
    },
    {
      "count": 8,
      "species": 3
    }
  ],
  "time": 0.09,
  "fields": {
    "count": {
      "type": "number"
    },
    "species": {
      "type": "number"
    }
  },
  "total_rows": 3
}
```

The count, per species should be converted to percentages before display. Returning temperature over the same area is more difficult, as the raster uploaded to Carto needs to be minified prior to use. Therefore EuroLST values will probably only be given at a national level (and will be precalculated).



## 4. Recent butterfly observation Feed

Questionable as to whether or not this adds value. Leaving the details incase we want to add this in the future.

If we wish to create a feed showing recent observations (with photos) of specific species sightings uploaded to GBIF we can do that via the GBIF API. We can construct requests as follows.

* TAXON_KEY is the taxnomy code listed above.


We need to use the [GBIF API](http://www.gbif.org/developer/occurrence#p_taxonKey) to construct a GET request:

```html
http://www.gbif.org/occurrence/search?TAXON_KEY=1898286&GEOMETRY=-10.55+57.15%2C-10.55+71.84%2C44.56+71.84%2C44.56+57.15%2C-10.55+57.15&HAS_GEOSPATIAL_ISSUE=false&MEDIA_TYPE=StillImage
```

This request will return a webpage that contains a list of occurrences that match the request. We will then need to scrape the [OCCURENCE info](http://www.gbif.org/developer/occurrence) by making a second call the GBIF API, to return the individual record as JSON, which contains the information we wish to present (username, date, photo url, species, country etc.).

For example, if we had identified the record 1415672278, we could retrieve the JSON with a GET request as follows:

```
http://www.gbif.org/occurrence/1415672278/fragment
```

```json
{"associatedSequences":"HM871278",
  "basisOfRecord":null,
  "catalogNumber":null,
  "class":"Insecta",
  "country":"Finland",
  "decimalLatitude":"65.052",
  "decimalLongitude":"24.876",
  "eventDate":"23-Sep-2006",
  "extensions":{"gbif:Multimedia":[{"license":"https://creativecommons.org/licenses/by-nc-sa/3.0/",
                                    "type":"StillImage",
                                    "title":"LEFIB379-10",
                                    "format":"image/jpeg",
                                    "identifier":"http://www.boldsystems.org/pics/LEFIB/IMG_8391%2B1272376882.JPG",
                                    "references":"http://bins.boldsystems.org/index.php/Public_RecordView?processid=LEFIB379-10"}]},
                "family":"Nymphalidae",
                "genus":"Vanessa",
                "id":"http://bins.boldsystems.org/index.php/Public_RecordView?processid=LEFIB379-10",
                "identifiedBy":"Marko Mutanen",
                "institutionCode":"University of Oulu",
                "lifeStage":"A",
                "locality":null,
                "occurrenceID":"http://bins.boldsystems.org/index.php/Public_RecordView?processid=LEFIB379-10",
                "order":"Lepidoptera",
                "otherCatalogNumbers":"MM00953",
                "phylum":"Arthropoda",
                "recordNumber":"MM00953",
                "recordedBy":"family Marko Mutanen",
                "scientificName":"Vanessa atalanta",
                "stateProvince":"Northern Ostrobothnia",
                "taxonID":"BOLD:AAA8638",
                "typeStatus":null}
```


Note, we are only returning observations that contain images, as these will be displayed on the website, as a means of highlighting the citizen science narrative.

Also, may be of use, it seems the EUBON website is digesting the same info at [this website](http://api.eurogeoss-broker.eu/eu-bon-portal). It may be helpful to look at the website code and see how they call the API to extract the records first.



#### Preparing the butterfly observation data for Carto upload

Using the GBIF.org website, you can search for data by species occurrence, and download, in csv format, all observations relevant to the European region. Sample data are present in this repo in the GBIF folder.
These raw data contain excessive information for our purposes, and since we need to ensure the data are optimised for size, we will reduce each entry down to simply decimallatitude, decimallongitude, date, year integer, and a category number to indicate species (see list above).

This preparation is done by running the `prepare_gbif.py` script with a list of raw data files. To do this, `cd` to the GBIF_data folder, place any additional csv files downloaded from GBIF in that location, and run `python prepare_gbif.py *.csv`. This should produce `output.csv` which contains minified data from all input files.

**Note:** if you are adding a new species, not in the above list, you will need to add its scientific name and a unique category value (integer) to associate with it in the python dictionary in `prepare_gbif.py`.

### EuroLST (base-map data)

We will use EuroLST as high-resolution temperature base maps. Uncompressed these data are  ~750mb, which is too large for uploading to Carto to use as a tile server. We have created a simple script to reduce the file size in `eurolst_process/main.py`. (*This software needs improvement, as is currently slow.*)

** Procedure is as follows**

* Remap values between 1--255, setting 0 as the missing value. and convert data-type to 8-bit integers.
* Add LZW compression.

### Creation of National-level statistics table

To create a summary table that respond rapidly we should pre-calculate the national-level statistics.
National statistics for the EUROLST data and butterflies needs to be calculated separately, and then aggregated, as they are two different problems:

1. National statistics over EuroLST data:
  - this is a vector to raster operation (subsetting and aggregating a raster by a vector). We have created a python 3.6 program to do this: `./eurolst_process/gen_national_table.py` which will produce a csv file as output.
  Note, we are only using a small subset of European and Scandinavian countries, as this project is a demo only, rather than a fully-featured tool.

2. National statistics over GBIF data:
  - This is a vector to vector operation (identify intersecting points within a national polygon).

The table will be uploaded to Carto. Note, the values will be in counts, and must be converted to
relative abundance on the front-end, based on the species the user has requested. (i.e. if only two species are requested then relative abundance would be calculated, e.g. for species_1 as relAbundanceSpecies1=species_1/(speces_1 + species_2) * 100.
