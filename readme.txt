###  Requirements:
- installing requirments.txt (in .venv)
>>> pip3 install -r requirements.txt

- install dockerdesktop (application)


### Run server
- build docker container (bash or use vs code extentions)
>>> docker compose -f 'docker_setup/docker-compose.yml' up -d --build 

- dashboard available with
http://localhost:4200/dashboard


### Problem solving
- Set profiles.yml to local project:
>>> dbt run --profiles-dir docker_setup

- Register the block types in the prefect-dbt module to make them available for use.
>>> prefect block register -m prefect_dbt


