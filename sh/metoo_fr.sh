#!/usr/bin/

DATETIME="`date '+%Y%m%d%H%M%S'`"
echo $DATETIME

FILENAME="data/metoo_fr_${DATETIME}.txt"
echo $FILENAME

curl -XPOST 'http://lisis.elasticsearch.spinn3r.com/content_*/_search?pretty=true' \
     -H "X-vendor: lisis" \
     -H "X-vendor-auth: 55aYKKiL6DTWzhvArKGBMP7QdEU" \
     -d '{
          "size": 1000,
            "query": {
                "query_string" : {
                    "query" : "(tags:metoo) OR (tags:moiaussi) OR (main: *metoo* ) OR (main: *moiaussi* )"
                }
            },
            "filter": {
              "query" : {
                  "query_string" : {
                      "query" : "(lang:fr) AND (domain:twitter.com)"
                  }
              }
            }
        }
        ' >> $FILENAME
