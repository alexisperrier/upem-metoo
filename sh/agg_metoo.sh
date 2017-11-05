#!/usr/bin/

curl -XPOST 'http://admin.elasticsearch.spinn3r.com/content_*/_search?pretty=true' -H "X-vendor: lisis" -H "X-vendor-auth: 55aYKKiL6DTWzhvArKGBMP7QdEU" -d '
{
  "size": 0,

  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "lang": "en"
          }
        }, {
          "term": {
            "domain": "twitter.com"
          }
        },
        {
          "range": {
            "published": {
              "gte": "14/10/2017",
              "lt": "17/10/2017",
              "format": "dd/MM/yyyy"
            }
          }
        }
      ],
      "should": [
        {
          "term": {
            "main": "metoo"
          }
        },
        {
          "term": {
            "tags": "metoo"
          }
        }
      ],
      "minimum_should_match": 1
    }
  },
  "aggs": {
    "published_metoo": {
      "date_histogram": {
        "field": "published",
        "interval": "2h"
      }
    }
  }
}
'
