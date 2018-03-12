#!/usr/bin/env python

import requests
import json

####
VENDOR="lisis"
# VENDOR_AUTH=""

####
# Define the query you want to run.
MAIN_REQUEST = "Firefox"

QUERY="""
{
    "size": 10,
    "query": {
        "query_string" : {
            "query" : "main: """ + MAIN_REQUEST + """ "
        }
    },
    "filter": {
      "query" : {
          "query_string" : {
              "query" : "(domain:cnn.com) AND (tags:linux) AND (geo_country:US)"
          }
      }
    }
}
"""

NUMBER_OF_PAGES=10

###
# generic function to just write data to disk
def handle_data(page, response):

    file_name="./" + MAIN_REQUEST + "%04d.json" % page

    print("Writing JSON data to: %s" % file_name)

    f=open( file_name, "w" );
    f.write( response.text )
    f.close()

###
# Perform the first request.  The URL needs to be slightly different because
# we have to specify the index name here.

url='http://%s.elasticsearch.spinn3r.com/content*/_search?scroll=5m&pretty=true' % VENDOR

print("Fetching from %s" % url)
print("Running query: ")
print(QUERY)

## we have to add our vendor code information to the request now.
headers = { 'X-vendor': VENDOR,
            'X-vendor-auth': VENDOR_AUTH }

response = requests.post( url, headers=headers, data=QUERY )

print(response.text)
####
# now that we have the first result we have to parse in the scroll ID. The first
# page is LITERALLY just the scroll ID.

data=json.loads(response.text)

scroll_id = data["_scroll_id"]

handle_data(0,response)

print("Query took: %sms" % data["took"])
print("Total hits: %s" % data["hits"]["total"])

for page in range( 1, NUMBER_OF_PAGES):

    url='http://%s.elasticsearch.spinn3r.com/_search/scroll?scroll=5m&pretty=true' % VENDOR

    response = requests.post( url, headers=headers, data=scroll_id )

    handle_data(page,response)

    scroll_id = response.json()["_scroll_id"]
