#! /bin/sh

export CONF_HOME=/tmp/chaos-conf
mkdir -p $CONF_HOME
cp chaos.cfg $CONF_HOME

python manager.py dbinit

export C_FORCE_ROOT=true
export OAUTHLIB_INSECURE_TRANSPORT=true

agent_tag=`cat ''$CONF_HOME'/chaos.cfg'|grep 'agent_tag'|awk -F '= ' '{print $2}'`

queue=`hostname|sed 's/[-.]/\_/g'`_$agent_tag

if [ $agent_tag ] ;then
    echo "agent模式启动:" $queue
    nohup python -m celery -A agent worker -Q $queue --loglevel=info &
else
    echo "master模式启动"
    nohup python -m celery -A tasks worker --loglevel=info &
fi
gunicorn -c gunicorn.py manager:app --log-level info -w 3
