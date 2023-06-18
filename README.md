# What is this?
This repo contains a simple Python Flask webserver that hosts a single API:
```
/api/anidb/id?name={series_name}
```

Calling this API will download a pre-generated embedding and dataset for AniDB series titles from this Huggingface repo: https://huggingface.co/datasets/khellific/anidb-series-embeddings. The API will then load the embeddings into a [sentence-transformers](https://www.sbert.net/) model and perform the default cosine similarity search from the library of `series_name` and return the highest ranked match's AniDB id as JSON of the form:

```
{ id: "anidb-id", "name": "anidb entry match title", "score": "similarity score" }
```

This API is intended to be used with my [forked version of the HamaTV Plex agent](https://github.com/khell/Hama.bundle) to match anime series with AniDB entries, allowing users to disregard the typical naming conventions required for that agent to normally work.

# Running
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
5. First startup may be slow, as embeddings and dataset must be downloaded from Huggingface.