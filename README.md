## EUBON Butterfly visualisation project


### Summary

We designed this project to showcase the [EuroLST data](http://www.geodati.fmach.it/eurolst.html),
using the narrative of butterfly observations across Europe. We will need to show several maps from Euro LST data as basemaps, and overlay vectors based on
butterfly observations from [GBIF](http://www.gbif.org). We can make these data comparable (at least in a qualitative manner) in both space (i.e. across areas or national averages) and time (i.e. over temporal bins of 4 years) by calculating **relative proportions**: *i.e. for each area we can calculate the relative percentage of butterfly seen that were of a given type*.

E.g. If a given area shows 10 observations, 5 of butterfly type 1, 3 of butterfly type 2, and 2 of butterfly type 3, then the relative abundance is 50%, 30% and 20% respectively. Doing this will enable us to generalise over time and space, despite the widely different sampling frequency. (The only difference a higher-sampling frequency will have, is to increase the accuracy of the estimate.)

Aggregated, this data should show 1) how relative abundance changes in space, and 2) if changes in relative abundance have occurred in time (during the last 16 years of EurLST data for which we will construct co-temporal analysis). We will also show for the area averaged abundance the temperature anomaly detected from EurLST over this time.


Features to note:
* Observer effect: A strong country dependence is evident in the data, which relates to prevalence of observers in different countries. These raw data  mainly of the prevalence of citizen science, and must be turned in to relative abundance before being compared in time and space.
* Variability: (In temperature data) we will try to minimise this volatility by presenting data in 4-year blocks. This will also help with scarcity of butterfly observations, and the considerable size of the EurLST data.
* Trends: Actual trends in population range may occur with changes in climate, as insects respond rapidly to environmental change. The data may indeed reflect this, but we should note the qualitative nature of this association due to the limits of interpreting these data.

We will use three different butterfly species:

* [Vanessa Atalanta Linnaeus, 1758](http://www.gbif.org/species/1898286): taxonomy code 1898286, category 1 in the Carto table
* [Vanessa Pieris Napi (Linnaeus, 1758)](http://www.gbif.org/species/1920494): taxonomy code 1920494, category 2 in the Carto table
* [Vanessa Pieris Brassicae (Linnaeus, 1758)](http://www.gbif.org/species/1920506): taxonomy code 1920506, category 3 in the Carto table
* [Nymphalis xanthomelas](http://www.gbif.org/species/5130587) taxonomy code 5130587, category 4 in the Carto table
* [Vanessa cardui](http://www.gbif.org/species/4299368): taxonomy code 4299368, category 5 in Carto table
* [Araschnia levana Linneaus, 1758](http://www.gbif.org/species/1902533) taxonomy code 1902533, category 6 in the Carto table
* [Apatura ilia Denis & Schiffermüller, 1775](http://www.gbif.org/species/8138711) taxonomy code 8138711, category 7 in the Carto table
* [Apatura iris Linnaeus, 1758](http://www.gbif.org/species/5131910) taxonomy code 5131910, category 8 in the Carto table


## visualisation components

The components of this visualisation are:

1. Map, with base layer of minified EuroLST data, and over-plotted butterfly point observations.
  * EuroLST data is too large to display in full, and butterfly data is too patchy display at high-frequency.
  Thus 4 year temperature anomalies, with 4-year groupings of butterfly observations could work well.
  Covering periods of 200-2004, 2005-2008, 2008-2012, 2012-206.
1. Map Widget:
  * User clicks on the map can return a widget displaying relative abundance of a given species over a buffered area, or nation, and also average EurLST base-map temperature anomalies for the same area.
1. Feed of most recent observations in GBIF database for relevant butterfly species:
  * Using the RESTFUL API of GBIF, we can request butterfly data for the species we desire, over Europe,
  which contains photos, and display the most recent observations only, to assist in building the narrative of this being a project based in citizen science.
1. National level summary statistics displayed as a widget.
  * Country level relative abundance of observations over time (2000-2004, 2005-2008, 2009-2012, 2013-2016) per species, and also averages over the EuroLST data per country for the same times.


## 1. Map

### Map demo/SQL for returning butterfly observation data

We have created a small prototype version of a map using Carto.js to expose butterfly and EuroLST example data, leaving examples of the settings that can be used to build the website.

* Python server: cd into `./simple_server` and execute `./start.sh`. The map should be viewable at [http://0.0.0.0:8000](http://0.0.0.0:8000).

## 2. Map Widget

If the decimal latitude and longitude can be passed to ST_POINT() function, with a given buffer (in decimal degrees), the following API call will return JSON containing the counts per species seen over a given area in a given time-period, which can be used to create a simple widget for display.

Note below, Lat = -0.032958984375, Lon = 51.5429188223739), and the buffer = 0.5. Also note the user account (below = benlaken) and table name (below = butterfly_sanitized) may be different.

CARTO API GET request:

```html
https://benlaken.carto.com/api/v2/sql/?q=SELECT count(species), species FROM butterfly_sanitized WHERE st_intersects(the_geom, ST_Buffer(st_setsrid(ST_point(-0.032958984375, 51.5429188223739),4326), 0.5)) AND year > 2009 AND year < 2016  group by species
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

The count, per species should be converted to percentages before display. A separate call needs to be made to Carto to retrieve the temperature from EuroLST over the same area.

**Futher EXAMPLE of this to be added...**


## 3. Recent butterfly observation Feed

To return the required data from GBIF API, we can construct requests as follows.

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

We have multiple options here:

The [GBIF API](http://www.gbif.org/developer/occurrence#p_taxonKey) will enable us to create summary Statistics per country using the *Occurrence Metrics* feature.

Alternatively, and perhaps better for us, we can make SQL queries to the data in Carto, and return statistics over specified country geometries, for both the butterfly observations, and the EuroLST basemaps which we will upload.


## Notes for processing raw GBIF data

The raw observation data of three species of butterfly are processed to make the files smaller,
condescend into one file, and uploaded to a Carto account.

For 3 different types of butterfly species.

Select and download observations of butterfly occurrence per species from GBIF online database.

Locally, run prepare_gbif.py to extract only the key data. This program is located in the folder ``./GBIF_data`.
E.g. converting the file `0060414-160910150852091.csv` to `butterfly_1.csv` as below.

`python prepare_gbif.py 0060414-160910150852091.csv butterfly_1.csv`


## Notes for processing EuroLST data

** IN PROGRESS**

The basemaps of EuroLST must be made lightweight (as each raw file is ~750mb). It should then be uploaded to a Carto account and used as a raster layer.

* Remap values between 1--256,setting 0 as the missing value. and convert to 8-bit integers.
* LZW compression.

A script to compress these data is in the `eurolst_process` folder. At the moment it is crude, and under development. It can be run via `python main.py`.


## Stretch Goal: Extending the visualisation with Species Distribution model raster layers

There is a possibility to extend this visualisation by using the observations to create a derivative product in the form of a Species Distribution Model. While these have their own limitations and caveats, and would essentially be a more processed form of the data we are already presenting, it would have advantages in that it would more closely twine the temperature and species observation data, and create the appearance of a more consistent dataset. It is however more complicated to produce, and will take more time.
