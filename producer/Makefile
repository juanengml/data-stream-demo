TSURU_APP_PREFIX = producer-data-stream
TSURU_APP_TEAM = infra-team

UNAME_S := $(shell uname -s)
ifeq (${UNAME_S}, Darwin)
	DETECTED_OS := darwin
endif
ifeq (${UNAME_S}, Linux)
	DETECTED_OS := linux
endif

define USAGE

Usage:
  make deploy-prod

  make info-dev
  make start-prod
  
endef
export USAGE

all:
	@echo "$$USAGE"


deploy-prod:
	sudo docker build -t  ${TSURU_APP_PREFIX} .
	sudo docker run  -d  --restart=always ${TSURU_APP_PREFIX} 

start-prod:
	sudo docker run  -d  --restart=always ${TSURU_APP_PREFIX} 

