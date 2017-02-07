# 新詞林

## Environments

`python 3.4.3`

## Run server

```
uwsgi --http 0.0.0.0:12345 --module buzz --callable app --processes 2 --threads 2
uwsgi --http 0.0.0.0:12346 --module app --callable app --processes 2 --threads 2
```
