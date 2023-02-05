# Johnny Cache

I wrote a stupid cache service so I could use this pun for a name.

# Why?

For Fun

# How (do I use this)?

You really shouldn't but if you insist...

## Natively

1. `git clone git@github.com:BenDavidAaron/johnny-cache.git` (get a copy of the repo)
1. `cd johnny-cache` (go into the repo)
1. `python3.10 -m venv venv` (make a new venv)
1. `source venv/bin/activate` (turn on your venv)
1. `export JOHNNY_CACHE_DATA_PATH=~/path/down/to/mexico` (pick a place to persist your cache in case of crash)
1. `export JOHNNY_CACHE_FLUSH_SIZE=1000` (set max number of puts before an object is persisted, depends on your usage pattern)
1. `./scripts/run.sh` (to start a development server)

## Docker

1. `git clone git@github.com:BenDavidAaron/johnny-cache.git` (get a copy of the repo)
1. `cd johnny-cache` (go into the repo)
1. `docker build -t johnny-cache .` (feed Johnny to the Whale)
1. `docker run johnny-cache -p NNNN:80 -v ~/opt/data/:/local/path/to_cache` (swim away)
