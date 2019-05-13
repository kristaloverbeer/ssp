# SSP

## Usage

To start with, you need to create a local Docker network:
```bash
docker network create ssp_network
```

To launch the stack:
```bash
make run
```

To upgrade the database to the latest schema:
```bash
make upgrade
```

To execute the different tests suites:
```bash
make typing-check
make syntax-check
make tests
```

To enter the API container:
```bash
make sh
```

To watch the API container logs:
```bash
make log
```

To stop the stack:
```bash
make stop
```

To clean the containers created:
```bash
make clean
```

To clean old built images that are not used anymore:
```bash
make clean-dangling-images
```

### Feed data to the database
```bash
docker exec -it ssp_database sh

/ # psql postgresql://postgres:postgres@ssp_database/ssp

ssp=# \i /home/data.sql
```

## Endpoints

Enter here all referenced endpoints

- admin endpoint
```bash
GET http://localhost:8080/admin
```

## TODO List

- Find a way to install `ortools` on Docker
