#!/usr/bin/env python
'''
# case insensitive search on keyword
python metoo.py --api all --keyword 8march --since_date 2018-03-01
# case sensitive search on #hashtag
python metoo.py --api all --hashtag 8march --since_date 2018-03-01
'''

import requests
import json
import pandas as pd
import datetime
from dateutil import parser
import os
import logging
import argparse

# ----------------------------------------------------------------------------------------------
#  Params
# ----------------------------------------------------------------------------------------------
TITLE       = 'womensday'
print(TITLE)
BUCKET       = 'upem-iwd2018'
print(BUCKET)
DATA_FOLDER = '/Users/alexis/amcp/upem/metoo/data_{}/'.format(TITLE)
print(DATA_FOLDER)
KEYWORD_FILE = "{}{}.csv".format(DATA_FOLDER,TITLE )
STEP        = datetime.timedelta(days =7)
print(STEP)
# STEP = datetime.timedelta(hours =6)
# STEP = datetime.timedelta(minutes =30)

prsr = argparse.ArgumentParser()
prsr.add_argument('--api', help='all, hot, warm, cold', default="hot")
prsr.add_argument('--zipupload', help='Set to True to zip, upload to google storage and delete original json data', default=False)
prsr.add_argument('--keyword', help='case insensitive search. body includes the char chain in keyword')
prsr.add_argument('--hashtag', help='case sensitive search. body includes the #hashtag')
prsr.add_argument('--since_date', nargs = '?', const="2017-10-01", default="2017-10-01 00:00:00",
                    help='Since date',
                    type=str)
args = prsr.parse_args()


API        = prsr.parse_args().api
print(API)
ZIPUPLOAD  = prsr.parse_args().zipupload
print(ZIPUPLOAD)
KEYWORD     = prsr.parse_args().keyword
print(KEYWORD)
HASHTAG     = prsr.parse_args().hashtag
print(HASHTAG)

SINCE_DATE  = prsr.parse_args().since_date
print(SINCE_DATE)
SINCE_DATE  = parser.parse(SINCE_DATE)
# UNTIL_DATE  = parser.parse("2017-10-31 00:00:00")
UNTIL_DATE  = datetime.datetime.now()
print(UNTIL_DATE)

df = pd.read_csv(KEYWORD_FILE)


# ----------------------------------------------------------------------------------------------
#  Logger
# ----------------------------------------------------------------------------------------------

logger = logging.getLogger(TITLE)
hdlr = logging.FileHandler('/Users/alexis/amcp/upem/metoo/log/{}.log'.format(TITLE))
formatter = logging.Formatter('%(asctime)s %(levelname)s {} %(message)s '.format(API))
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

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

def json_query(start_date, end_date):
    '''
    To restrict to English add:
                { "term": {"lang": "en"} },
    To restrict to Hastags remove :
                { "term": { "main": "metoo" } },
    Size: Max number of t   weets per request, saved in file
    Date are formatted  strftime(%Y-%m-%dT%H:%M:%SZ)
    '''
    if HASHTAG is not None:
        return """
{
    "size": 10000,
    "query":
        {
          "bool": {
            "must": [
                { "term":  {"domain": "twitter.com"} },
                { "range": { "published": { "gte": "%s", "lt": "%s", "format": "date_time_no_millis" } } }
            ],
            "should": [
                { "term": { "tags": "%s" }   }
            ],
            "minimum_should_match": 1
          }
        }
}
""" % (start_date, end_date, HASHTAG)

    if KEYWORD is not None:
        return """
{
    "size": 10000,
    "query":
        {
          "bool": {
            "must": [
                { "term":  {"domain": "twitter.com"} },
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
""" % (start_date, end_date, KEYWORD, KEYWORD)

def inspect():
    if (len(data['hits']['hits']) > 0):
        tweets = [d['_source']['main']  for d in data['hits']['hits'] if d['_source']['main_length'] > 10   ]
        print("---- {}) hit_count {}".format(page_count, hit_count))
        print("[first:] {} \n[last:] {}".format(tweets[0], tweets[-1]  ))

def to_file(start_date, page_count, hit_count):
    filename    = DATA_FOLDER + "{0}_{1}_{2}_{3}_{4}.json".format(
        KEYWORD,
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
    logger.info("=="*30)
    logger.info(API)
    logger.info(CONTENT_URL)
    logger.info("SINCE: {} \t UNTIL {}".format(SINCE_DATE, UNTIL_DATE))

    logger.info( "STEP: {}".format(STEP))
    logger.info("--"*30)
    logger.info( json_query( SINCE_DATE.strftime('%Y-%m-%dT%H:%M:%SZ'), UNTIL_DATE.strftime('%Y-%m-%dT%H:%M:%SZ') ))
    logger.info(" ")
    logger.info("--"*30)


    start_date = SINCE_DATE
    while (start_date < UNTIL_DATE):
        end_date = start_date + STEP
        # ----------------------------------------------------------------------
        # First query on the CONTENT_URL
        # ----------------------------------------------------------------------
        page_count  = 0

        # Build the query
        query = json_query(
            start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
            end_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        )

        # Get the data
        response    = requests.post( CONTENT_URL, headers=header(), data=query )
        try:
            data        = json.loads(response.content)
        except:
            logger.error(response.content)
            raise
        hit_count   = len(data['hits']['hits'])
        logger.info("=== [{}] Start: {} \t End {}".format(hit_count, start_date, end_date))
        if hit_count > 9999:
            logger.warning("Over 10k for {}".format(start_date))

        if hit_count > 0:
            # save to filename
            to_file(start_date, page_count, hit_count)
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
            except:
                logger.error(response.content)
                raise

            hit_count   = len(data['hits']['hits'])
            scroll_id   = data["_scroll_id"]
            if hit_count > 0:
                if hit_count > 9999:
                    logger.warning("Over 10k for {}_{}".format(start_date, page_count))
                to_file(start_date, page_count, hit_count)
                inspect()
        start_date = end_date

    # ----------------------------------------------------------------------
    # Compress files
    # ----------------------------------------------------------------------
    if ZIPUPLOAD:
        WORD = KEYWORD if HASHTAG is None else HASHTAG

        zip_filename    = "{0}{1}_{2}_{3}_to_{4}.zip".format(
            DATA_FOLDER,
            WORD,
            API,
            SINCE_DATE.strftime('%Y%m%d'),
            UNTIL_DATE.strftime('%Y%m%d'),

        )
        data_files = "{0}{1}*.json".format(DATA_FOLDER,WORD)
        print("compressing and uploading to google")
        # compress
        cmd = "zip -r {0} {1}".format(zip_filename,data_files)
        os.system(cmd)
        # send to google storage
        cmd = "gsutil cp  {} gs://{}/".format(zip_filename, BUCKET)
        os.system(cmd)
