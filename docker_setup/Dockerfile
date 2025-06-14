FROM prefecthq/prefect:3.4.6-python3.12

# Set working directory for prefect and dbt.
WORKDIR /root/flows

RUN apt-get update && apt-get install -y curl docker.io

# Copy requirements and install them.
COPY ./requirements_worker.txt ./requirements_worker.txt
RUN pip install -r requirements_worker.txt --no-cache-dir


# Copy scripts to the image.
COPY ./start-worker.sh /opt/prefect/start-worker.sh

# Run scrips. Make sure the script is executable.
RUN chmod +x /opt/prefect/start-worker.sh

# Default command (can be overridden by docker-compose)
CMD ["/bin/bash"]
