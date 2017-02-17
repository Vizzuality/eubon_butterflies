from __future__ import print_function
import pandas as pd
import os
import sys


def restrict_area_of_df(df, north=80, east=50, south=30, west=-20):
    """Restrict the points in a dataframe by position"""
    tmp = df[df.decimallatitude > south]
    tmp = tmp[tmp.decimallatitude < north]
    tmp = tmp[tmp.decimallongitude > west]
    tmp = tmp[tmp.decimallongitude < east]
    return tmp


def process_table(df):
    """Convert a table to a stripped down version, centered over Europe."""
    df = df[df.date == df.date]      # exclude data with no valid time value:
    df_eu = restrict_area_of_df(df)  # exclude data outside of the EU region
    t = [pd.to_datetime(dt).date() for dt in df_eu.date]
    yr = [y.year for y in t]
    name = df_eu.nameComplete[0]
    if name == 'Vanessa atalanta Linnaeus, 1758':
        print("{n} = category 1".format(n=name))
        species = [1] * len(df_eu)
    elif name == 'Pieris napi (Linnaeus, 1758)':
        print("{n} = category 2".format(n=name))
        species = [2] * len(df_eu)
    elif name == 'Pieris brassicae (Linnaeus, 1758)':
        print("{n} = category 3".format(n=name))
        species = [3] * len(df_eu)
    df_eu = df_eu.drop(['occurrenceid', 'date', 'nameComplete'], axis=1)
    df_eu['date'] = t
    df_eu['year'] = yr
    df_eu['species'] = species
    return df_eu


def extract_data(input_file, output_file):
    """Take a raw input file from GBIF database, and strip out non-essential info.
    Save it as a csv file, with the name provided."""
    assert os.path.isfile(input_file), "{infile} was not found".format(infile=input_file)
    f = pd.read_csv(input_file, sep='	', low_memory=False)
    df = pd.DataFrame()
    df['occurrenceid'] = f['occurrenceid']
    df['nameComplete'] = f['scientificname']
    df['date'] = f['eventdate']
    df['decimallatitude'] = f['decimallatitude']
    df['decimallongitude'] = f['decimallongitude']
    cleaned = process_table(df)
    if os.path.isfile(output_file):
        print("{outfile} exists. Overwriting file.".format(outfile=output_file))
    cleaned.to_csv(output_file, index=False)
    print("Program sucsess.")
    return

if __name__ == '__main__':
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    extract_data(input_file, output_file)
