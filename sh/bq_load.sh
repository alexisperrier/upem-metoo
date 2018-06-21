#!/bin/bash
shopt -s nullglob
# bq mk --table upemnumi:eu_metoo.twitter /Users/alexis/amcp/upem/metoo/meta_metoo_june/schema_twitter.json
# DATA_FOLDER='/Users/alexis/amcp/upem/metoo/data_metoo_june/'
BQ_FOLDER='/Users/alexis/amcp/upem/metoo/data_metoo_june/bq/'
PROCD_FOLDER='/Users/alexis/amcp/upem/metoo/data_metoo_june/processed/'

for f in "$BQ_FOLDER"*.csv;
do
    echo "--load $f"
    bq load eu_metoo.twitter "$f"
    mv $f $PROCD_FOLDER
done



# upload each file
# start=`date +%s`
# bq mk --table upemnumi:eu_metoo.twitter_12 twitter_02.json
# for f in balancetonporc*.csv
# do
#     echo "Uploading- $f"
#     tail -n +2 "$f" > btp.csv
#     bq load  eu_metoo.twitter_12 btp.csv
# done
# bq query "select count(*) from eu_metoo.twitter_12"
# end=`date +%s`
# runtime=$((end-start))
# echo "runtime: $runtime"

# upload each file
# start=`date +%s`
# bq mk --table upemnumi:eu_metoo.twitter_13 twitter_02.json

# touch  btp_02.csv
# for f in balancetonporc*.csv
# do
#     echo "Tail- $f"
#     cat "$f" >> btp_02.csv
# done
#
# bq mk --table upemnumi:eu_metoo.twitter_02 schema_twitter.json
# bq load  eu_metoo.twitter_02 btp_02.csv
# bq query "select count(*) from eu_metoo.twitter_02"

# bq mk --table upemnumi:eu_metoo.twitter_05 twitter_02.json
#
# balancetonporc_any_all_2018_05_28_0000_000_292.csv
# balancetonporc_any_all_2018_06_02_0000_000_56.csv
# balancetonporc_any_all_2018_05_29_0000_000_226.csv
# balancetonporc_any_all_2018_06_03_0000_000_53.csv
#
# bq query "select count(*) from eu_metoo.twitter_04"
#
# tail -n +2 balancetonporc_any_all_2018_05_28_0000_000_292.csv > btp.csv
# bq load  eu_metoo.twitter_04 btp.csv
# tail -n +2 balancetonporc_any_all_2018_05_28_0000_000_292.csv > btp.csv
# bq load  eu_metoo.twitter_04 btp.csv
# tail -n +2 balancetonporc_any_all_2018_05_28_0000_000_292.csv > btp.csv
# bq load  eu_metoo.twitter_04 btp.csv
# tail -n +2 balancetonporc_any_all_2018_05_28_0000_000_292.csv > btp.csv
# bq load  eu_metoo.twitter_04 btp.csv
#
# for file in *.csv; do
#     [ -e "$file" ] || continue
#     # ... rest of the loop body
# done
