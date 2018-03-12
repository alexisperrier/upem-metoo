# Women's day twitter extraction

* Span: March 1st to March 15
* API: Spinner Hot

Hashtags are case sensitive and keywords are not

So extraction for keyword: WomensDay
will include tweets with hashtags #internationalwomensday2018 and #InternationalWomensDay

# Hashtags & keywords (case insensitive)
* 8march
* FGM
* SexSelection
* [added] WomensDay
* [added] SexDetermination
* [added] IWD2018
* [added] March8
* 8mars

# Hashtags only (case sensitive)
* InternationalWomensDay2018
* InternationalWomensDay
* WomensDay2018
* IWD
* 8M
* JournéeDesDroitsDesFemmes
* Weltfrauentag
* DíaInternacionalDeLaMujer

Hashtags linked to Global Agenda:


#GlobalGoals
#HealthForAll
#TimeIsNow
#genderequality
#GenderEquality
#KeepItEqual
#genderparity
#PressforProgress
#GenderEqualityIsForMenToo
#GBV
#ENDviolence

Female Genital Cutting:

#EndFGC
#endFGM
#EndFGM
#FGM
#FGC
#FemaleCircumcision
#Femalecircumcision
#FCvsFGM
#AllAboutFC


#GBSS
#SexSelection
#sexselectiveabortion
#SexDetermination
#SaveTheGirlChild
#BetiBachaoBetiPadhao
#girlchild
#daughterdeficit






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
                { "term": { "tags": "8march" }   },
                { "term": { "main": "8march" }   }
            ],
            "minimum_should_match": 1
          }
        }
}
