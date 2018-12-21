# pawatt-spiders
# 1. Setup
```sh
# build environment container
$ make build

# run environment container
$ make start

# authenticate with shub
$ shub login

# update requirements.txt
$ pip freeze > requirements.txt

# deploy from environment container
$ shub deploy
```

# 2. Running Spiders
```sh
# scrap current Uganda power outages (https://www.umeme.co.ug/planned-outages/)
$ scrapy crawl sp_outage_ug
```

# 3. Periodic Jobs
| Spider | Country | Schedule |
| --- | --- | --- |
| `sp_outage_ug` | Uganda | Weekly: Mondays |
