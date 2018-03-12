#!/usr/bin/env python
'''
OTHER QUERIES:
 metoo EN
"query" : "(lang:ru) AND (domain:twitter.com) AND ( (tags:Навальный) OR (main: Навальный ) )"
'''

import requests
import json
import pandas as pd
import datetime
import os

# Attention to not disclose the auth keys on github
VENDOR_DATASTREAM      = os.environ['VENDOR_DATASTREAM']
VENDOR_DATASTREAM_AUTH = os.environ['VENDOR_DATASTREAM_AUTH']

CONTENT_URL = "http://{0}.elasticsearch.datastreamer.io/content*/_search?scroll=5m&pretty=true".format(VENDOR_DATASTREAM)
SCROLL_URL  = "http://{0}.elasticsearch.datastreamer.io/_search/scroll?scroll=5m&pretty=true".format(VENDOR_DATASTREAM_AUTH)


def header():
    return { 'X-vendor': VENDOR_DATASTREAM, 'X-vendor-auth': VENDOR_DATASTREAM_AUTH }

def json_query(start_date, end_date):
    '''
    To restrict to English add:
                { "term": {"lang": "en"} },
    To restrict to Hastags remove :
                { "term": { "main": "metoo" } },
    Size: Max number of tweets per request, saved in file
    Date are formatted  strftime(%Y-%m-%dT%H:%M:%SZ)
    '''

    return """
{
    "size": 1000,
    "query":
        {
          "bool": {
            "must": [
                { "term": {"domain": "twitter.com"} },
                { "range": { "published": { "gte": "%s", "lt": "%s", "format": "date_time_no_millis" } } }
            ],
            "should": [
                { "term": { "main": "navalny" } },
                { "term": { "tags": "Навальный" } },
                { "term": { "tags": "Путин" } }
            ],
            "minimum_should_match": 1
          }
        }
}
""" % (start_date, end_date)

def inspect():
    if (len(data['hits']['hits']) > 0):
        tweets = [d['_source']['main']  for d in data['hits']['hits'] if d['_source']['main_length'] > 10   ]

        print("\n---- {}) hit_count {}".format(page_count, hit_count))
        print("[first:] {} \n[last:] {}".format(tweets[0], tweets[-1]  ))

def to_file(start_date, page_count):
    filename    = "../data/navalny_{0}_{1}.json".format(start_date.strftime('%Y_%m_%d_%H%M'), str(page_count).zfill(3))
    print("writing {} to {}".format(hit_count, filename))
    f=open( filename, "w" );
    f.write( json.dumps(data['hits']['hits'], indent = 0))
    f.close()

if __name__== '__main__':

    # start with tweets from 2017 oct 13
    start_date = datetime.datetime(2018, 1, 8,0,0,0)
    #
    # time range could be hours = 4, minutes = 30, ...
    step = datetime.timedelta(days =2)

    # Iterate until now
    while (start_date < datetime.datetime.now()):
        end_date = start_date + step
        print("="*30)
        print("Start: {} \t End {}".format(start_date, end_date))
        # ----------------------------------------------------------------------
        # First query on the CONTENT_URL
        # ----------------------------------------------------------------------
        page_count  = 0

        # Build the query
        query = json_query(
            start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
            end_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
        ).encode("utf-8")

        # Get the data
        response    = requests.post( CONTENT_URL, headers=header(), data=query )
        data        = json.loads(response.content)
        hit_count   = len(data['hits']['hits'])

        # if hit_count > 0:
        #     # save to filename
        to_file(start_date, page_count)
        inspect()

        # ----------------------------------------------------------------------
        # Iterate on that first query using the scroll_id
        # ----------------------------------------------------------------------
        scroll_id   = data["_scroll_id"]

        while hit_count > 0:
            page_count += 1

            # Use the SCROLL_URL to get the data
            response    = requests.post( SCROLL_URL, headers=header(), data=scroll_id )
            data        = json.loads(response.content)
            hit_count   = len(data['hits']['hits'])
            scroll_id   = data["_scroll_id"]
            if hit_count > 0:
                to_file(start_date, page_count)
                inspect()
        start_date = end_date
