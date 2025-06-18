FROM prefecthq/prefect:3.4.6-python3.12

# Set working directory for prefect and dbt.
WORKDIR /root/flows

RUN apt-get update && apt-get install -y curl docker.io postgresql-client

# Copy requirements and install them.
COPY ./requirements_worker.txt ./requirements_worker.txt
RUN pip install -r requirements_worker.txt --no-cache-dir


# Copy scripts to the image.
COPY ./start-worker.sh /opt/prefect/start-worker.sh
COPY macros macros
COPY models models
COPY flows flows

# Run scrips. Make sure the script is executable.
RUN chmod +x /opt/prefect/start-worker.sh

ENV PREFECT_API_URL="http://server:4200/api"

# Default command (can be overridden by docker-compose)
CMD ["/bin/bash"]
