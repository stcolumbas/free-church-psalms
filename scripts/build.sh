set -e

# generate plain text, .tex, pptx and ProPresenter files:
docker-compose build
docker-compose run psalms

# build site
cd site/
yarn
yarn build
cd ../
# copy files
cp -R output/ dist/
