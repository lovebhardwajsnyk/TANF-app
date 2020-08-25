#!/bin/sh
#
# This script will attempt to create the services required
# and then launch everything.
#

# This is the hostname for the route set for the
CGHOSTNAME_FRONTEND="${CGHOSTNAME_FRONTEND:-tdp-frontend}"

if [ "$1" = "setup" ] ; then  echo
	# set up app
	if cf app tdp-frontend >/dev/null 2>&1 ; then
		echo tdp-frontend app already set up
	else
		cf push tdp-frontend --docker-image ${DOCKER_IMAGE_FRONTEND}
	fi
fi

# launch the app
if [ "$1" = "rolling" ] ; then
	# Do a zero downtime deploy.  This requires enough memory for
	# two apps to exist in the org/space at one time.
	cf push tdp-frontend --no-route -f manifest.yml --strategy rolling || exit 1
else
	cf push tdp-frontend -f manifest.yml --no-route
fi
cf map-route tdp-frontend app.cloud.gov --hostname "$CGHOSTNAME_FRONTEND"

# tell people where to go
echo
echo
echo "to log into the site, you will want to go to https://${CGHOSTNAME_FRONTEND}.app.cloud.gov/"
echo 'Have fun!'
