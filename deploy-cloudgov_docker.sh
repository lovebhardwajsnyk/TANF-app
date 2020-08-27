#!/bin/sh
#
# This script will attempt to create the services required
# and then launch everything.
#

# These are the hostnames and docker image file names
DEPLOY_STRATEGY=${1}
CGHOSTNAME_BACKEND=${2}
CGHOSTNAME_FRONTEND=${3}
DOCKER_IMAGE_BACKEND=${4}
DOCKER_IMAGE_FRONTEND=${5}
CIRCLE_BRANCH=${6}

echo DEPLOY_STRATEGY: $DEPLOY_STRATEGY
echo BACKEND_HOST: $CGHOSTNAME_BACKEND
echo FRONTEND_HOST: $CGHOSTNAME_FRONTEND
echo DOCKER_BACKEND_IMAGE: $DOCKER_IMAGE_BACKEND
echo DOCKER_FRONTEND_IMAGE: $DOCKER_IMAGE_FRONTEND
echo CIRCLE_BRANCH=$CIRCLE_BRANCH


# function to check if a service exists
service_exists()
{
  cf service "$1" >/dev/null 2>&1
}

update_frontend()
{
	if [ "$1" = "rolling" ] ; then
	    echo WOOO
		# Do a zero downtime deploy.  This requires enough memory for
		# two apps to exist in the org/space at one time.
		# --strategy rolling || exit 1
	else
	    echo WEEE
		#cf push $CGHOSTNAME_FRONTEND -f tdrs-frontend/manifest.yml --no-route
	fi
	#cf map-route $CGHOSTNAME_FRONTEND app.cloud.gov --hostname "${2}"
}

update_backend()
{
	if [ "$1" = "rolling" ] ; then
		# Do a zero downtime deploy.  This requires enough memory for
		# two apps to exist in the org/space at one time.
		#cf push $CGHOSTNAME_BACKEND --no-route -f tdrs-backend/manifest.yml --var docker-backend=$DOCKER_IMAGE_BACKEND --strategy rolling || exit 1
		echo wip
	else
		#cf push $CGHOSTNAME_BACKEND --no-route -f tdrs-backend/manifest.yml --var docker-backend=$DOCKER_IMAGE_BACKEND --no-route
        
		# set up JWT key if needed
		if cf e $CGHOSTNAME_BACKEND | grep -q JWT_KEY ; then
		   echo jwt cert already created
		else
		   echo wooop
		   #export SETUPJWT="True"
	   fi
	fi
	#cf map-route $CGHOSTNAME_BACKEND app.cloud.gov --hostname "$CGHOSTNAME_BACKEND"
}

# launch the app
if [ "$1" = "rolling" ] ; then
	# set up backend
	if cf app tdp-backend >/dev/null 2>&1 ; then
		echo tdp-backend app already set up
	else
	    update_backend 'rolling'
	fi

	# set up frontend
	if cf app tdp-frontend >/dev/null 2>&1 ; then
		echo tdp-frontend app already set up
	else
	    update_frontend 'rolling'
	fi
fi


if [ "$1" = "setup" ] ; then  echo
	# create services (if needed)
	if service_exists "tdp-app-deployer" ; then
	  echo tdp-app-deployer already created
	else
	  cf create-service cloud-gov-service-account space-deployer tdp-app-keys
	  cf create-service-key tdp-app-keys deployer
	  echo "to get the CF_USERNAME and CF_PASSWORD, execute 'cf service-key tdp-app-keys deployer'"
	fi

	if service_exists "db-raft" ; then
	  echo db-raft already created
	else
	  if [ "$6" = "prod" ] ; then
	    cf create-service aws-rds medium-psql-redundant db-raft
		  echo sleeping until db is awake
		  for i in 1 2 3 ; do
		  	sleep 60
		  	echo $i minutes...
		  done
	  else
	    cf create-service aws-rds shared-psql db-raft
	    sleep 2
	  fi
	fi

	# set up backend
	if cf app tdp-backend >/dev/null 2>&1 ; then
		echo tdp-backend app already set up
	else
	    update_backend
	fi

	# set up frontend
	if cf app tdp-frontend >/dev/null 2>&1 ; then
		echo tdp-frontend app already set up
	else
	    update_frontend
	fi
fi

generate_jwt_cert() 
{
	echo "regenerating JWT cert/key"
	yes 'XX' | openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -sha256
	cf set-env tdp-backend JWT_CERT "$(cat cert.pem)"
	cf set-env tdp-backend JWT_KEY "$(cat key.pem)"

	# make sure that we have something set that you can later override with the
	# proper value so that the app can start up
	if cf e tdp-backend | grep -q OIDC_RP_CLIENT_ID ; then
		echo OIDC_RP_CLIENT_ID already set up
	else
		echo "once you have gotten your client ID set up with login.gov, you will need to set the OIDC_RP_CLIENT_ID to the proper value"
		echo "you can do this by running: cf set-env tdp-backend OIDC_RP_CLIENT_ID 'your_client_id'"
		echo "login.gov will need this cert when you are creating the app:"
		cat cert.pem
		cf set-env tdp-backend OIDC_RP_CLIENT_ID "XXX"
	fi
}

# regenerate jwt cert
if [ "$1" = "regenjwt" ] ; then
	generate_jwt_cert
fi


# tell people where to go
echo
echo
echo "to log into the site, you will want to go to https://${CGHOSTNAME_FRONTEND}.app.cloud.gov/"
echo 'Have fun!'