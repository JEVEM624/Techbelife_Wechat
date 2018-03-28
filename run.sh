#!/bin/bash
work_path=$(dirname $(readlink -f $0))

uwsgi --http :5002 --wsgi-file $work_path/main.py --callable app -H $work_path --daemonize $work_path/uwsgi.log
