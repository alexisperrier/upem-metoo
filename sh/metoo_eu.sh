#!/usr/bin/

DATETIME="`date '+%Y%m%d%H%M%S'`"
echo $DATETIME

FILENAME="data/metoo_eu_${DATETIME}.txt"
echo $FILENAME

curl -XPOST 'http://lisis.elasticsearch.spinn3r.com/content_*/_search?pretty=true' \
     -H "X-vendor: lisis" \
     -H "X-vendor-auth: 55aYKKiL6DTWzhvArKGBMP7QdEU" \
     -d '{
          "size": 1000,
            "query": {
                "query_string" : {
                    "query" : "(tags:quellavoltache) OR (main: *quellavoltache* ) OR (tags:yotambien) OR (main: *yotambien* ) OR (tags:jagocksa) OR (main: *jagocksa* ) OR (tags:EuTambem) OR (main: *EuTambem* ) OR (tags:metoo) OR (main: *metoo* )"
                }
            },
            "filter": {
              "query" : {
                  "query_string" : {
                      "query" : "((lang:es) OR (lang:it) OR (lang:de) OR (lang:da) OR (lang:nl) OR (lang:no) OR (lang:pt) OR (lang:ru) OR (lang=sv))  AND (domain:twitter.com)"
                  }
              }
            }
        }
        ' >> $FILENAME
