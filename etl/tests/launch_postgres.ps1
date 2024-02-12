docker pull postgres:15.5
docker run -e "POSTGRES_PASSWORD=postgres" -p 5432:5432 --rm postgres:15.5