#!/bin/bash

DATE=`date +%Y-%m-%d`
python /opt/suntorytime/goldDigger/scanner.py > /opt/suntorytime/goldDigger/out/log_$DATE.log

