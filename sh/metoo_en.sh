#!/usr/bin/

DATETIME="`date '+%Y%m%d%H%M%S'`"
echo $DATETIME

FILENAME="data/metoo_en_${DATETIME}.txt"
echo $FILENAME

curl -XPOST 'http://lisis.elasticsearch.spinn3r.com/content_*/_search?pretty=true' \
     -H "X-vendor: lisis" \
     -H "X-vendor-auth: 55aYKKiL6DTWzhvArKGBMP7QdEU" \
     -d '{
          "size": 1000,
            "query": {
                "query_string" : {
                    "query" : "(tags:metoo) OR (main: *metoo* )"
                }
            },
            "filter": {
              "query" : {
                  "query_string" : {
                      "query" : "(lang:en) AND (domain:twitter.com)"
                  }
              }
            }
        }
        ' >> $FILENAME
