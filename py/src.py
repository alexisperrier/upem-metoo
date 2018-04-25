#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import os
import urllib


VENDOR_DATASTREAM      = os.environ['VENDOR_DATASTREAM']
VENDOR_DATASTREAM_AUTH = os.environ['VENDOR_DATASTREAM_AUTH']
CONTENT_URL = "http://{0}.elasticsearch.datastreamer.io/content_*/_search?scroll=5m&pretty=true".format(VENDOR_DATASTREAM)

def header():
    return { 'X-vendor': VENDOR_DATASTREAM, 'X-vendor-auth': VENDOR_DATASTREAM_AUTH }

word = 'JoTambé'
query = """
{
     "size": 1000,
       "query": {
           "query_string" : {
               "query" : "(tags:%s)"
           }
       },
       "filter": {
         "query" : {
             "query_string" : {
                 "query" : "domain:twitter.com"
             }
         }
       }
   }
""" % word


response    = requests.post(
    CONTENT_URL,
    headers=header(),
    data=query

    )

print(response.content)
