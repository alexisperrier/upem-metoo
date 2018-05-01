gsutil acl get gs://upem-airpollution  > upem-airpollution.json
gsutil -m acl ch -u emile.provendier@gmail.com:R gs://dmi2018/**
gsutil -m defacl ch -u emile.provendier@gmail.com:R gs://dmi2018
