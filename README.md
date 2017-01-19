# Project

Use Scrapy to crawl data from http://mangak.info. This is Vietnamese Manga Website

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Python 3.x
* Text Editor (Visual Studio Code)
* MongoDb
* RoboMongo

### Installing

A step by step series of examples that tell you have to get a development env running

settings.py

Change request delay time

```
DOWNLOAD_DELAY = 10
```

And your local Mongo Instance

```
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "allapi"
```


## Built With

* [Scrapy](https://scrapy.org/) - Python web crawl framework


## Authors

* **Phu Le**
