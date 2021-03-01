#!/usr/bin/env bash

ENV=${ENV:-product}
MODE=${MODE:-django}

cmd=""

if [ $MODE = 'django' ]; then
    mkdir -p /data/logs/uwsgi
    cmd="/usr/local/python3/bin/uwsgi --ini uwsgi.ini"
elif [ $MODE = 'celery_beat' ]; then
    cmd="/usr/local/python3/bin/celery beat -A drf_template -l info"
elif [ $MODE = 'celery_worker_queue_default' ]; then
    cmd="/usr/local/python3/bin/celery worker -A drf_template -l info -Q default"

# 其他runscript命令：直接通过环境变量来动态执行runscript_name命令，比如设置环境变量 MODE=runscript,runscript_name=test_runscript
elif [ $MODE = 'runscript' ]; then
    runscript_name=${runscript_name:-runscript_name}
    cmd="/usr/local/python3 manage.py runscript $runscript_name --traceback"
fi

# 执行命令
if [ "$cmd" != "" ];then
    echo cmd: $cmd
    $cmd
else
    while [ 1 ]
    do
        echo "Invalid MODE: ${MODE}"
        sleep 10
    done
fi
