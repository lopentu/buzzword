# 新詞林：新詞偵測與生命力預測系統

## Environments

`python 3.4.3`

## Installation

```
pip install -r pip.txt
```

## Create table

```
CREATE TABLE history (datetime DATETIME, ip CHAR(20), word CHAR);
CREATE TABLE cache (word PRIMARY KEY, json_data CHAR);

CREATE TABLE rating (datetime DATETIME, ip CHAR(20), word CHAR, score INTEGER, UNIQUE (ip, word));
CREATE UNIQUE INDEX rating_index ON rating (ip, word); 
```
 
## Run server

```
uwsgi --http 0.0.0.0:12345 --module buzz --callable app --processes 2 --threads 2
```
 
