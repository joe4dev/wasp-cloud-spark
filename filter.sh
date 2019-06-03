#!/usr/bin/env bash

cat data/multiply.log | ag 'Resizing|DURATION' > data/multiply_filtered.log

