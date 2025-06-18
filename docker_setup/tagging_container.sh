#docker tag dabi_2025-cli:latest  dabi_2025-cli:v1.0 
#docker tag dabi_2025-server:latest  dabi_2025-server:v1.0
#docker tag dabi_2025-worker:latest  dabi_2025-worker:v1.0 

#python docker_setup/setup/load_static_to_stg.py

#python flows/process_orders.py
docker tag dabi_2025-cli  localhost:6500/dabi_2025-cli
docker tag dabi_2025-server  localhost:6500/dabi_2025-server
docker tag dabi_2025-worker  localhost:6500/dabi_2025-worker

docker push localhost:6500/dabi_2025-cli
docker push localhost:6500/dabi_2025-server
docker push localhost:6500/dabi_2025-worker