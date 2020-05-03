#!/bin/bash

NAME="pipetaxon"
IMAGE="voorloop/pipetaxon:latest"


start() {
  echo -en "\r[....] Starting pipetaxon"
  if [ ! "$(docker ps -q -f name=$NAME)" ]; then
    if [ "$(docker ps -aq -f status=exited -f name=$NAME)" ]; then
      docker rm $NAME 2> /dev/null 1> /dev/null
    fi
    docker run -d -it -p 8888:8000 --restart always --name $NAME $IMAGE $SECRET 2> /dev/null 1> /dev/null
    if [ ! $? -eq 0 ]; then
      echo -en "\r[\e[31mFAIL\e[0m] Starting pipetaxon"
    fi
  fi

  sleep 3

  if [ ! "$(docker ps -q -f name=$NAME)" ]; then
    echo -en "\r[\e[31mFAIL\e[0m] Starting pipetaxon"
    echo
    echo
    echo " - Please check the logs to found the cause, type: pipetaxon log"
  else
    echo -en "\r[ \e[32mOK\e[0m ] Starting pipetaxon"
  fi
  echo
}

stop() {
  echo -en "\r[....] Stopping pipetaxon"
  sleep 1
  if [ "$(docker ps -q -f name=$NAME)" ]; then
    docker kill $NAME 2> /dev/null 1> /dev/null
    if [ $? -eq 0 ]; then
      echo -en "\r[ \e[32mOK\e[0m ] Stopping pipetaxon"
    else
      echo -en "\r[\e[31mFAIL\e[0m] Stopping pipetaxon"
    fi
  else
    echo -en "\r[ \e[32mOK\e[0m ] Stopping pipetaxon"
  fi
  echo
}

install() {
  docker pull $IMAGE
}

log() {
  docker logs -f $NAME
}

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  restart)
    stop
    start
    ;;
  install)
    install
    ;;
  log)
    log
    ;;
  *)
    echo $"Usage: $0 {start|stop|restart|install|log}"
    exit 1
esac

exit 0
