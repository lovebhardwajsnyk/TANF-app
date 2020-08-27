 #!/bin/sh
touch tdrs-backend/vars-backend.yml && touch tdrs-frontend/vars-frontend.yml
echo docker-backend: goraftdocker/tdp-backend:$1\ > tdrs-backend/vars-backend.yml
echo docker-frontend: goraftdocker/tdp-frontend:$1\ > tdrs-frontned/vars-frontend.yml
