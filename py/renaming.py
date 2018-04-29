import json
import pandas as pd
import datetime
from dateutil import parser
import os
import glob
from tqdm import tqdm

for zip_file in glob.glob('./' + '*.zip'):
    tmp = zip_file.split('.')
    json_file = tmp[1] + '_json.' + tmp[2]
    cmd = "mv {} .{}".format(zip_file, json_file)
    print(cmd)
    os.system(cmd)
