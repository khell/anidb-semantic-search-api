# What is this?
This repo contains a simple Python Flask webserver that hosts a single API:
```
/api/anidb/id?name={series_name}
```

Calling this API will download a pre-generated Pytorch embedding and Huggingface dataset for AniDB series titles from this Huggingface repo: https://huggingface.co/datasets/khellific/anidb-series-embeddings. The API will then load the embeddings into a [sentence-transformers](https://www.sbert.net/) model and perform the default cosine similarity search from the library of `series_name` and return the highest ranked match's AniDB id as JSON of the form:

```
{ id: "anidb-id", "name": "anidb entry match title", "score": "similarity score" }
```

This API is intended to be used with my [forked version of the HamaTV Plex agent](https://github.com/khell/Hama.bundle) to match anime series with AniDB entries, allowing users to disregard the typical naming conventions required for that agent to normally work.

Note that the embeddings obviously need to be updated (and you need to download new versions) to keep this server up to date if you choose to run it yourself (see below).

# Do I need to run it myself?
I'm hosting a version of it (and keeping it updated where possible) on spare capacity here:
```
https://anidb.khell.net/api/anidb/id
```
It is behind Cloudflare so you may get rate-limited. I make no guarantees about its availability, reliability, latency or otherwise, and you should understand that while I don't explicitly retain any logs they are kept in Docker memory for the lifetime of the container (so I can theoretically see what you query).

# Running manually
1. Setup a virtual environment with Python 3.10.9 (other versions will most likely work, but I didn't test them).
2. Install requirements: `pip install -r requirements.txt`
3. If you are running on an Apple Silicon Mac: 
```
gunicorn 'main:app' --workers 1 --timeout 60 --bind 127.0.0.1:8080
```
4. Otherwise, you must set `TORCH_DEVICE` as an environment variable to either `cpu` or `cuda` (if available). On Unix systems, you can launch like this:
```
TORCH_DEVICE=cpu gunicorn 'main:app' --workers 1 --timeout 60 --bind 127.0.0.1:8080
```
5. You may want to configure `TRUST_X_FORWARDED` to any integer n, where n is the number of reverse proxies you are running behind (if any).
6. First startup may be slow, as embeddings and dataset must be downloaded from Huggingface.

# Running with Docker
1. You can just use the prebuilt image with Docker Compose: `docker compose up -d`
2. You might want to change the `TORCH_DEVICE` environment variable in the Compose file. It's set to run on `cpu` by default.
3. Note that `mps` is not available through Docker even if running on Apple Silicon: https://github.com/pytorch/pytorch/issues/81224
4. By default `TRUST_X_FORWARDED` is set to trust reverse proxies to a depth of 1. This is suitable for the default Compose configuration.