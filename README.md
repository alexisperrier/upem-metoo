# upem-metoo
Social media content related to the metoo stream

**Do not put the Account Vendor Key in clear in the code!**

# Run with

> python py/metoo.py

Requires python3

Writes data to /data with filenames as:

    metoo_en_2017_10_13_0000_000.json
    <keyword>_<lang>_<date time>_<page number>_.json

Set:

* start_date
* steps The range of time for the query: 1: days, 4: hours, ...

Edit the json_query() function to modify the query.
For instance for metoo tags and content in English:

    {
        "size": 10000,
        "query":
            {
              "bool": {
                "must": [
                    { "term": {"lang": "en"} },
                    { "term": {"domain": "twitter.com"} },
                    { "range": { "published": { "gte": "%s", "lt": "%s", "format": "date_time_no_millis" } } }
                ],
                "should": [
                    { "term": { "main": "metoo" } },
                    { "term": { "tags": "metoo" } }
                ],
                "minimum_should_match": 1
              }
            }
    }

Query balancetonporc in all languages

{
    "size": 10000,
    "query":
        {
          "bool": {
            "must": [
                { "term": {"domain": "twitter.com"} },
                { "range": { "published": { "gte": "%s", "lt": "%s", "format": "date_time_no_millis" } } }
            ],
            "should": [
                { "term": { "main": "balancetonporc" } },
                { "term": { "tags": "balancetonporc" } }
            ],
            "minimum_should_match": 1
          }
        }
}


Remove { "term": {"lang": "en"} }, to increase volume of tweets.
