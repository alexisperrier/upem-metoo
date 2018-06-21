import requests
import json, csv
import numpy as np
import pandas as pd
import datetime
from dateutil import parser
import os
import argparse

DATA_FOLDER = '/Users/alexis/amcp/upem/metoo/data_metoo_june/'
files = ['balancetonporc_any_all_2018_05_28_0000_000_292.csv',
'balancetonporc_any_all_2018_05_29_0000_000_226.csv',
'balancetonporc_any_all_2018_05_30_0000_000_123.csv']

df = pd.read_csv(DATA_FOLDER + 'btp_02.csv')

df.columns =

bq load  eu_metoo.twitter_13 btp_02.csv
