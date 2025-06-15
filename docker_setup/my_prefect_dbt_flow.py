from prefect import flow


@flow(log_prints=True)
def my_flow(name: str = "world"):
    print(f"Hello, {name}!")


if __name__ == "__main__":
    my_flow.deploy(
        name="my-deployment",
        work_pool_name="general-work-pool",
        image="dabi_2025-cli:latest",
        push=True,  #can't find the image when False
        build=False
    )
    my_flow(name="DABI 2025")