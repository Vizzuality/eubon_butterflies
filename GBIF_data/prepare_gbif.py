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

name_to_number = {'Vanessa atalanta Linnaeus, 1758':1,
                 'Pieris napi (Linnaeus, 1758)':2,
                 'Pieris brassicae (Linnaeus, 1758)':3,
                 'Nymphalis xanthomelas Denis & Schiffermüller, 1775':4,
                 'Vanessa cardui (Linnaeus, 1758) Linnaeus, 1758':5,
                 'Araschnia levana Linnaeus, 1758':6,
                 'Apatura ilia Denis & Schiffermüller, 1775': 7,
                 'Apatura iris Linnaeus, 1758': 8}

def process_table(df):
    """Convert a table to a stripped down version, centered over Europe."""
    df = df[df.date == df.date]      # exclude data with no valid time value:
    df_eu = restrict_area_of_df(df)  # exclude data outside of the EU region
    t = [pd.to_datetime(dt).date() for dt in df_eu.date]
    yr = [y.year for y in t]
    name = df_eu.nameComplete[0]
    if name in name_to_number:
        species = name_to_number[name] * len(df_eu)
    else:
        raise ValueError("Butterfly Name was not in dictionary of classifcation")
    df_eu = df_eu.drop(['occurrenceid', 'date', 'nameComplete'], axis=1)
    df_eu['date'] = t
    df_eu['year'] = yr
    df_eu['species'] = species
    return df_eu


def extract_data(input_file_list):
    """Take a list of input files from GBIF database, and strip out non-essential info.
    Compile dataframes into a single df, and return it."""
    cleaned = []
    for input_file in input_file_list:
        print("Processing {0}".format(input_file))
        if input_file is not "output.csv":
            assert os.path.isfile(input_file), "{infile} was not found".format(infile=input_file)
            f = pd.read_csv(input_file, sep='	', low_memory=False)
            df = pd.DataFrame()
            df['occurrenceid'] = f['occurrenceid']
            df['nameComplete'] = f['scientificname']
            df['date'] = f['eventdate']
            df['decimallatitude'] = f['decimallatitude']
            df['decimallongitude'] = f['decimallongitude']
            cleaned.append(process_table(df))
    big_df = pd.concat(cleaned, ignore_index=True)
    return big_df

if __name__ == '__main__':
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))
    input_files = sys.argv[1:]
    output_file = "output.csv"
    print(len(sys.argv[1:])," input files: ", sys.argv[1:])
    big_df = extract_data(input_files)
    if os.path.isfile(output_file):
        print("{outfile} exists. Overwriting file.".format(outfile=output_file))
    big_df.to_csv(output_file, index=False)
    print("Program sucsess.")
