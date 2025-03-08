cd image
docker build . -t as_front
cd ..
docker-compose down
docker-compose up -d --force-recreate
docker logs -f as_front
