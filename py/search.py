# -*- coding: utf-8 -*-
'''
python search.py --envt sparrow --api all  --since_date 2018-01-01  --until_date 2018-04-25  --zipupload True
%run search.py --envt sparrow --api all  --since_date 2018-01-01  --until_date 2018-04-25  --zipupload True
%run search.py --envt sparrow --api all  --since_date 2018-04-01  --until_date 2018-04-15  --zipupload True
'''

import requests
import json
import numpy as np
import pandas as pd
import datetime
from dateutil import parser
import os
import argparse

# ----------------------------------------------------------------------------------------------
#  Params
# ----------------------------------------------------------------------------------------------
TITLE        = 'airpollution'
BUCKET       = 'upem-airpollution'

prsr = argparse.ArgumentParser()
prsr.add_argument('--api', help='all, hot, warm, cold', default="hot")
prsr.add_argument('--zipupload', help='Set to True to zip, upload to google storage and delete original json data', default='')
prsr.add_argument('--envt', help='envt: local or sparrow', default="sparrow")
prsr.add_argument('--since_date', nargs = '?', const="2017-10-01", default="2017-10-01 00:00:00",
                    help='Since date',
                    type=str)
prsr.add_argument('--until_date', help='Until date', type=str)
args = prsr.parse_args()


API         = prsr.parse_args().api
ZIPUPLOAD   = bool(prsr.parse_args().zipupload)
ENVT        = prsr.parse_args().envt
SINCE_DATE  = prsr.parse_args().since_date
SINCE_DATE  = parser.parse(SINCE_DATE)
UNTIL_DATE  = prsr.parse_args().until_date
UNTIL_DATE  = parser.parse(UNTIL_DATE)
# UNTIL_DATE  = parser.parse("2017-10-31 00:00:00")
# UNTIL_DATE  = datetime.datetime.now()
print(API)
print(ZIPUPLOAD)
print(SINCE_DATE)
print(UNTIL_DATE)


if ENVT == 'sparrow':
    DATA_FOLDER = '/home/alexis/amcp/upem-metoo/data_{}/'.format(TITLE)
elif (ENVT == 'local'):
    DATA_FOLDER   = '/Users/alexis/amcp/upem/metoo/data_{}/'.format(TITLE)
else:
    DATA_FOLDER   = './'

KEYWORD_FILE = "{}{}.csv".format(DATA_FOLDER,TITLE )
# STEP         = datetime.timedelta(days =7)
print(TITLE)
print(BUCKET)
print(DATA_FOLDER)
print(KEYWORD_FILE)
# STEP = datetime.timedelta(hours =6)


# Attention to not disclose the auth keys on github
VENDOR_DATASTREAM      = os.environ['VENDOR_DATASTREAM']
VENDOR_DATASTREAM_AUTH = os.environ['VENDOR_DATASTREAM_AUTH']

apis = {
    'all': 'cold_content_*,warm_content_*,content_*',
    'hot':'content_*',
    'warm':'warm_content_*',
    'cold':'cold_content_*'
}

CONTENT_URL = "http://{0}.elasticsearch.datastreamer.io/{1}/_search?scroll=5m&pretty=true".format(VENDOR_DATASTREAM, apis[API])
SCROLL_URL  = "http://{0}.elasticsearch.datastreamer.io/_search/scroll?scroll=5m&pretty=true".format(VENDOR_DATASTREAM_AUTH)

def header():
    return { 'X-vendor': VENDOR_DATASTREAM, 'X-vendor-auth': VENDOR_DATASTREAM_AUTH }

def json_query(start_date, end_date, word, search_mode, lang = None):
    '''
    To restrict to English add:
                { "term": {"lang": "en"} },
    To restrict to Hastags remove :
                { "term": { "main": "metoo" } },
    Size: Max number of tweets per request, saved in file
    Date are formatted  strftime(%Y-%m-%dT%H:%M:%SZ)
    '''

    if lang == 'any':
        lang_str = ''
    else:
        lang_str = '{ "term":  {"lang": "%s"} },' % lang

    if search_mode == 'hashtag':
        return """
{
    "size": 10000,
    "query":
        {
          "bool": {
            "must": [
                { "term":  {"domain": "twitter.com"} },
                %s
                { "range": { "published": { "gte": "%s", "lt": "%s", "format": "date_time_no_millis" } } }
            ],
            "should": [
                { "term": { "tags": "%s" }   }
            ],
            "minimum_should_match": 1
          }
        }
}
""" % (lang_str, start_date, end_date, word)

    if search_mode == 'keyword':
        return """
{
    "size": 10000,
    "query":
        {
          "bool": {
            "must": [
                { "term":  {"domain": "twitter.com"} },
                %s
                { "range": { "published": { "gte": "%s", "lt": "%s", "format": "date_time_no_millis" } } }
            ],
            "should": [
                { "term": { "tags": "%s" }   },
                { "term": { "main": "%s" }   }
            ],
            "minimum_should_match": 1
          }
        }
}
""" % (lang_str, start_date, end_date, word, word)

def inspect():
    if (len(data['hits']['hits']) > 0):
        tweets = [d['_source']['main']  for d in data['hits']['hits'] if d['_source']['main_length'] > 10   ]
        print("---- {}) hit_count {}".format(page_count, hit_count))
        print("[first:] {} \n[last:] {}".format(tweets[0], tweets[-1]  ))

def to_file(word, lang, start_date, page_count, hit_count):
    filename    = DATA_FOLDER + "{0}_{1}_{2}_{3}_{4}_{5}.json".format(
        word,
        lang,
        API,
        start_date.strftime('%Y_%m_%d_%H%M'),
        str(page_count).zfill(3),
        hit_count
    )
    print("========= [{}] \n writing {} to {}".format(start_date,hit_count, filename))
    f=open( filename, "w" );
    f.write( json.dumps(data['hits']['hits'], indent = 0))
    f.close()

if __name__== '__main__':
    print("=="*30)
    print(API)
    print(CONTENT_URL)
    print("SINCE: {} \t UNTIL {}".format(SINCE_DATE, UNTIL_DATE))

    df = pd.read_csv(KEYWORD_FILE)
    for i,d in df.iterrows():
        word = d.Keyword
        search_mode = d.nature
        lang = d.lang
        step = datetime.timedelta(days = int(d.step))

        print("--"*30)
        print("{} {} **{}** {}: ".format(search_mode, lang, word,step))
        print("--"*30)
        print("{} {} **{}** {}: ".format(search_mode, lang, word,step))
        print( json_query(
                        SINCE_DATE.strftime('%Y-%m-%dT%H:%M:%SZ'),
                        UNTIL_DATE.strftime('%Y-%m-%dT%H:%M:%SZ'),
                        word, search_mode, lang
                    )
                )
        print(" ")
        print("--"*30)
        start_date = SINCE_DATE
        while (start_date < UNTIL_DATE):
            end_date = start_date + step
            # ----------------------------------------------------------------------
            # First query on the CONTENT_URL
            # ----------------------------------------------------------------------
            page_count  = 0

            # Build the query
            query = json_query(
                start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                end_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                word, search_mode, lang
            )

            # Get the data
            response    = requests.post( CONTENT_URL, headers=header(), data=query )
            try:
                data    = json.loads(response.content)
            except:
                print(response.content)
                raise
            hit_count   = len(data['hits']['hits'])
            print("=== [{}] Start: {} \t End {}".format(hit_count, start_date, end_date))

            if hit_count > 0:
                # save to filename
                to_file(word, lang, start_date, page_count, hit_count)
                inspect()

            # ----------------------------------------------------------------------
            # Iterate on that first query using the scroll_id
            # ----------------------------------------------------------------------
            scroll_id   = data["_scroll_id"]

            while hit_count > 0:
                page_count += 1

                # Use the SCROLL_URL to get the data
                response    = requests.post( SCROLL_URL, headers=header(), data=scroll_id )
                try:
                    data        = json.loads(response.content)
                    hit_count   = len(data['hits']['hits'])
                    scroll_id   = data["_scroll_id"]
                    if hit_count > 0:
                        to_file(word, lang, start_date, page_count, hit_count)
                        inspect()
                except:
                    print(response.content)
                    print("==="*20)
                    print("ERROR NOT RAISED")
                    print("==="*20)
                    # raise

            start_date = end_date

        # ----------------------------------------------------------------------
        # Compress files
        # ----------------------------------------------------------------------
        zip_filename    = "{0}{1}_{2}_{3}_{4}_{5}_to_{6}.zip".format(
            DATA_FOLDER,
            word,
            lang,
            search_mode,
            API,
            SINCE_DATE.strftime('%Y%m%d'),
            UNTIL_DATE.strftime('%Y%m%d'),
        )
        data_files = "{0}{1}*.json".format(DATA_FOLDER,word)
        print("compressing and (uploading to google:PAUSED)")
        # compress
        cmd = "zip -r -j {0} {1}".format(zip_filename,data_files)
        os.system(cmd)
        # send to google storage
        if ZIPUPLOAD:
            cmd = "gsutil cp  {} gs://{}/".format(zip_filename, BUCKET)
            os.system(cmd)
        # delete original json files
        print("delete original json files")
        cmd = "rm  {}".format(data_files)
        print("delete json files: {}".format(cmd))
        os.system(cmd)
