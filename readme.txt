###  Requirements:
- installing requirments.txt (in .venv)
>>> pip3 install -r requirements.txt

- install dockerdesktop (application)


### Run server
- build docker container (bash or use vs code extentions)
>>> docker compose -f 'docker_setup/docker-compose.yml' up -d --build 

- dashboard available with
http://localhost:4200/dashboard

when run python scripts from vs code:
>>> export PREFECT_API_URL=http://localhost:4200/api
- deploy flow
>>> python <python_filename_with_flow.py>
- scedule a deployment
>>>


### Problem solving
- Set profiles.yml to local project:
>>> dbt run --profiles-dir docker_setup

- Register the block types in the prefect-dbt module to make them available for use.
>>> prefect block register -m prefect_dbt


