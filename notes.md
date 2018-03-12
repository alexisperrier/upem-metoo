donc pour recapituler

1) les extractions metoo et balancetonporc sont sur google. Emma devrait pouvoir acceder.

=> Il y a un gap entre les endpoints spinn2r entre le 1er nov et le 31 dec. Aucun tweet entre ces 2 dates.
J'ai ouvert un ticket chez spinn2r.

2) J'ai relancé notre demande d'extraction complete pour la liste de 50+ hashtags. Je relance si pas de reponse d'ici demain.

3) On sait maintenat que spinn3r nous donne pas les RT. L'API search de twitter donne acces a 100 RT max par tweet.
Est ce que cela peut etre interessant bien que non exhaustif?




# metoo

with warm endpoint, 1st tweet is on 2016-10-07, building up quickly



# Balancetonporc


Debut le 2017-10-14
https://twitter.com/search?f=tweets&vertical=default&q=%23balancetonporc%20since%3A2017-10-13%20until%3A2017-10-14&src=typd

warm jusqu'a 2017-10-31 (1200 res)
puis 0 avec warm

on bascule sur hot
zero resultats de 2017-11-01 a 2017-12-31 sauf pour le 2017-12-15 (210 results)
ca reprend le 2018-01-01 avec 200 resultats


# Issues

warm_content_* endpoint
works until  Start: 2017-10-31 with [4718] results on that day the zero for the following days
but switching to the hot content: still gives zero results until 2017-11-20 but for only a handful of results
in the following days

it seems
* there's gap between 2017-10-31 and 2017-11-20
* not all tweets are retrieved with he HOT endpoint after 2017-11-20
* only picks up on 2017-12-01 with a sudden jump from 258 tweets to 3416 tweets in a day.


# DOC
We use a hot/warm/cold architecture for storing content long term to maximize both performance and content density.
http://docs.datastreamer.io/#hot-warm-cold-architecture

* content_* 	    Access content in the last 30 days on ultra-fast SSD with 25% of is cached in memory
* warm_content_*	Access an additional 6 months of content on a larger cluster of HDD machines
* cold_content_*	Access an additional 3 months of content on higher density HDD machines

# Tags vs Main

* searching on the tags is case sensitive, on the "main" is case insensitive
* searching on the tags returns less results than searching on the main (checked for duplicates)
for Start: 2017-11-01 00:00:00 	 End 2017-11-02 00:00:00
                { "term": { "tags": "metoo" }   },
                { "term": { "tags": "Metoo" }   },
                { "term": { "tags": "MeToo" }   },
returns 1000 results while
                { "term": { "tags": "metoo" }   },
                { "term": { "tags": "Metoo" }   },
                { "term": { "tags": "MeToo" }   },
                { "term": { "main": "metoo" }   }
returns 2000 results
as does the search on just the main and not the tags
                { "term": { "main": "metoo" }   }
