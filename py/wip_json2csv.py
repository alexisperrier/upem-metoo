'''
Given a folder with zipped json files extracted from spinn3r, the script

* unzip the files into ./tmp/
* converts the json to csv files using pandas
* zips the csv files
* upload the files to a google storage bucket


'''
import json
import pandas as pd
import datetime
from dateutil import parser
import os
import glob
from tqdm import tqdm

BUCKET          = 'upem-wakanda'
source_folder   = '/Users/alexis/amcp/upem/metoo/data_wakanda/'
tmp_folder      = '/Users/alexis/amcp/upem/metoo/data_wakanda/tmp/'
csv_folder      = '/Users/alexis/amcp/upem/metoo/data_wakanda/csv/'

if __name__== '__main__':

    for zip_file in glob.glob(source_folder + '*.zip'):

        print("processing " + zip_file)

        # Unzip
        cmd = "unzip {0} -d {1} ".format(zip_file, tmp_folder)
        os.system(cmd)
        json_files = glob.glob(tmp_folder + '*.json')
        print(" {} json files".format(len(json_files)))

        for json_file in tqdm(json_files):
            # convert to csv
            df  = pd.read_json(json_file)
            dd  = pd.DataFrame.from_dict(list(df['_source'].values))

            csv_file = csv_folder + json_file.split('/')[-1].split('.')[0] + '.csv'
            dd.to_csv(csv_file)

        print("compressing")
        # compress
        csvzip_filename    = zip_file.split('/')[-1].split('.')[0] + "_csv.zip"
        cmd = "zip -r -j {0} {1}".format(csvzip_filename,csv_folder + "*.csv")
        os.system(cmd)
        # send to google storage
        print("upload to {}".format(BUCKET))

        # cmd = "gsutil cp  {} gs://{}/".format(csvzip_filename, BUCKET)
        # os.system(cmd)
        # delete json  and csv files
        print("delete tmp/ folder")
        cmd = "rm  {}".format(csv_folder + "*.csv")
        os.system(cmd)
        cmd = "rm  {}".format(tmp_folder + "*.json")
        os.system(cmd)
