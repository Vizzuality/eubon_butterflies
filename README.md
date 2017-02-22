## EUBON Butterfly visualisation

This project showcases the [EuroLST data](http://www.geodati.fmach.it/eurolst.html),
using the narrative of butterfly observations across Europe.

We will need to show several maps from Euro LST data as basemaps, and overlay vectors based on
butterfly observations from [GBIF](http://www.gbif.org).

The raw observation data of three species of butterfly are processed to make the files smaller,
condescend into one file, and uploaded to a Carto account.

The basemaps of EuroLST are also optimised (as each raw file is ~750mb). We remap the values between 1--256,
setting 0 as the missing value. Then compress the data with lzw compression, and convert to 8-bit integers.
This minified data is then uploaded to Carto as raw data.

The basemaps and vectors are then requested and mapped Cartodb.js.

For 3 different types of butterfly species.

Select and download observations of butterfly occurrence per species from GBIF online database.

Locally, run prepare_gbif.py to extract only the key data. This program is located in the folder ``./GBIF_data`.
E.g. converting the file `0060414-160910150852091.csv` to `butterfly_1.csv` as below.

`python prepare_gbif.py 0060414-160910150852091.csv butterfly_1.csv`

* Vanessa Atalanta Linnaeus, 1758 = category 1
* Vanessa Pieris Napi (Linnaeus, 1758) = category 2
* Vanessa Pieris Brassicae (Linnaeus, 1758) = category 3


## Running server Locally

* Python server: cd into `./simple_server` and execute `./start.sh`. The map should be viewable at [http://0.0.0.0:8000](http://0.0.0.0:8000).

## Story

Note: The observations depend on:
* observer effect: A strong country dependence is evident in the data, which cannot be corrected.
* Population variability: we will try to minimise this volatility by presenting data in 5-year blocks.
* trends: Actual shifts in location will occur with changes in climate, as insects respond rapidly to environmental change.

## EuroLST data

I will need to minify the Eurolst data. A script to compress these data is in the `eurolst_process` folder. At the moment it is crude, and under development. It can be run via `python main.py`.
