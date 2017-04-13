#!/bin/bash

gunicorn -w 4 -b 0.0.0.0:11235 news_server:app &>> server.log &
