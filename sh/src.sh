#!/usr/bin/
curl -XPOST 'http://lisis.elasticsearch.spinn3r.com/content_*/_search?pretty=true' \
     -H "X-vendor: lisis" \
     -H "X-vendor-auth: " \
     -d '{
          "size": 1000,
            "query": {
                "query_string" : {
                    "query" : "(tags:JoTambé)"
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
        '
