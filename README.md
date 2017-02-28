## EUBON Butterfly visualisation project

[Basic demo](http://bl.ocks.org/benlaken/9fc0db2e992a24267a5bc48936d9e926) of raw data displayed on web-map using carto.js.


### Summary

We designed this project to showcase the [EuroLST data](http://www.geodati.fmach.it/eurolst.html),
using the narrative of butterfly observations across Europe. We will need to show several maps from Euro LST data as basemaps, and overlay vectors based on
butterfly observations from [GBIF](http://www.gbif.org). We can make these data comparable (at least in a qualitative manner) in both space (i.e. across areas or national averages) and time (i.e. over temporal bins of 4 years) by calculating **relative proportions**: *i.e. for each area we can calculate the relative percentage of butterfly seen that were of a given type*.

E.g. If a given area shows 10 observations, 5 of butterfly type 1, 3 of butterfly type 2, and 2 of butterfly type 3, then the relative abundance is 50%, 30% and 20% respectively. Doing this will enable us to generalise over time and space, despite the widely different sampling frequency. (The only difference a higher-sampling frequency will have, is to increase the accuracy of the estimate.)

Aggregated, this data should show 1) how relative abundance changes in space, and 2) if changes in relative abundance have occurred in time (during the last 16 years of EurLST data for which we will construct co-temporal analysis). We will also show for the area averaged abundance the temperature anomaly detected from EurLST over this time.


Features to note:
* Observer effect: A strong country dependence is evident in the data, which relates to prevalence of observers in different countries. These raw data  mainly reflect where observers are, and so must be turned in to relative abundance before comparing in time and space.
* Variability: (In temperature data) we will try to minimise this volatility by presenting data in 4-year blocks. This will also help with scarcity of butterfly observations, and the considerable size of the EurLST data.
* Trends: Actual trends in population range may occur with changes in climate, as insects respond rapidly to environmental change. The data may indeed reflect this, but we should note the qualitative nature of this association due to the limits of interpreting these data. The trends may be distinct for butterflies that migrate vs those which do not (we have selected both types).

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

** IN PROGRESS **

To create widgets that respond rapidly we should pre-calculate the national-level statistics. I intend the table to roughly have the following format:


 Country_code     | Year_group     | EuroLST| species_1| species_2
------------- | ------------- | ------------- | -------------
ENG      | 2000       | 0.80 | 1000 | 300
ENG      | 2004       | 0.95 | 1100 | 310


The table will be uploaded to Carto. Note, the values will be in counts, and must be converted to
relative abundance on the front-end, based on the species the user has requested. (i.e. if only two species are requested then relative abundance would be calculated, e.g. for species_1 as relAbundanceSpecies1=species_1/(speces_1 + species_2) * 100.

# visualisation components

The components of this visualisation are:

1. Map, with base layer of minified EuroLST data, and over-plotted butterfly point observations.
  * EuroLST data is too large to display in full, and butterfly data is too patchy display at high-frequency.
  Thus 4 year temperature anomalies, with 4-year groupings of butterfly observations could work well.
  Covering periods of 200-2004, 2005-2008, 2008-2012, 2012-206.
1. Map Widget:
  * User clicks on the map can return a widget displaying relative abundance of a given species over a buffered area, or nation.
1. Feed of most recent observations in GBIF database for relevant butterfly species:
  * Using the RESTFUL API of GBIF, we can request butterfly data for the species we desire, over Europe,
  which contains photos, and display the most recent observations only, to assist in building the narrative of this being a project based in citizen science.
1. National level summary statistics displayed as a widget.
  * Country-level relative abundance of observations over time (2000-2004, 2005-2008, 2009-2012, 2013-2016) per species, and also averages over the EuroLST data per country for the same times.


## 1. Map

### Map demo/SQL for returning butterfly observation data

We have created a small prototype version of a map using Carto.js to expose butterfly and EuroLST example data, leaving examples of the settings that can be used to build the website.

* Python server: cd into `./simple_server` and execute `./start.sh`. The map should be viewable at [http://0.0.0.0:8000](http://0.0.0.0:8000). Alternativley, you can view a [version running on bl.ocks.org](http://bl.ocks.org/benlaken/9fc0db2e992a24267a5bc48936d9e926).

## 2. Map Widget

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


## 3. Recent butterfly observation Feed

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

## 4. National Level Statistics

* The [GBIF API](http://www.gbif.org/developer/occurrence#p_taxonKey) can create summary Statistics per country using the *Occurrence Metrics* feature.

* Alternatively, and better for our use case, we can make SQL queries to the data in Carto, and return statistics over specified country geometries, for both the butterfly observations, and the EuroLST basemaps which we will upload in a single table.

** In Progress **



## Stretch Goal: Extending the visualisation with Species Distribution model raster layers

There is a possibility to extend this visualisation by using the observations to create a derivative product in the form of a Species Distribution Model. While these have their own limitations and caveats, and would essentially be a more processed form of the data we are already presenting, it would have advantages in that it would more closely twine the temperature and species observation data, and create the appearance of a more consistent dataset. It is however more complicated to produce, and will take more time.
