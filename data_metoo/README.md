# Metoo day twitter extraction

* Span: Oct 1st 2017 to March 30 2018
* API: Spinner All

Hashtags are case sensitive and keywords are not


# queries
{
    "size": 10000,
    "query":
        {
          "bool": {
            "must": [
                { "term":  {"domain": "twitter.com"} },
                { "range": { "published": { "gte": "2018-03-01T00:00:00Z", "lt": "2018-03-09T00:00:00Z", "format": "date_time_no_millis" } } }
            ],
            "should": [
                { "term": { "tags": "metoo" }   },
                { "term": { "main": "metoo" }   }
            ],
            "minimum_should_match": 1
          }
        }
}

1femmesur2,keyword,7
alexiadaval,keyword,7
balancetatruie,keyword,7

balancetonforum,keyword,7
balancetonporc,keyword,7
boycottcesar,keyword,7
boycottwebedia,keyword,7
buffymars,keyword,7
consentement,hashtag,7
cultureduviol,keyword,7
femen,keyword,7
feminicide,keyword,7
harcelement,hashtag,7
howiwillchange,keyword,7
ihave,hashtag,7
jonathanndaval,keyword,7
march4women,keyword,7
moiaussi,keyword,7
NadiaDaam,keyword,7
nerienlaisserpasser,keyword,7
notallmen,keyword,7
noviolence,hashtag,7
occupywomen,keyword,7
QuellaVoltaChe,keyword,7
RapeCulture,keyword,7
slutshaming,keyword,7
stilleforopptak ,keyword,7
stopabuse,keyword,7
TariqRamadan,keyword,7
timesup,keyword,7
uniteblue,keyword,7
victimblaming,keyword,7
violencecontrelesfemmes,keyword,7
violencesconjugales,keyword,7
Weinstein,keyword,7
metoo,keyword,1
