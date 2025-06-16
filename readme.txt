###  Requirements:
- installing requirments.txt (in .venv)
>>> pip3 install -r requirements.txt

- install docker desktop (application)

- copy files (.csv and parquet) to 'data/' from
https://ilias.h-ka.de/ilias.php?baseClass=ilLinkResourceHandlerGUI&ref_id=976747&cmd=calldirectlink

### Run server
- build docker container (bash or use vs code extentions)
>>> docker compose -f 'docker_setup/docker-compose.yml' up -d --build 

- dashboard available with
http://localhost:4200/dashboard

when run python flows from vs code:
>>> export PREFECT_API_URL=http://localhost:4200/api

# >>> python <python_filename_with_flow.py>
#- scedule a deployment


### Problem solving
- Set profiles.yml to local project: (from docker_setup)
>>> dbt run --profiles-dir docker_setup

- Register the block types in the prefect-dbt module to make them available for use.  (from docker_setup)
>>> prefect block register -m prefect_dbt


