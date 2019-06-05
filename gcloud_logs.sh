#!/usr/bin/env bash

gcloud beta logging read \
      'timestamp>="2019-06-03T17:17:00Z" AND
   timestamp<="2019-06-03T18:08:00Z"'# > data/gcloud2.log
