from prefect import flow


@flow(log_prints=True)
def my_flow(name: str = "world"):
    print(f"Hello, {name}!")


if __name__ == "__main__":
    my_flow.deploy(
        name="my-deployment",
        work_pool_name="general-work-pool",
        image="bt_cli",
        push=False # switch to True to push to your image registry
    )