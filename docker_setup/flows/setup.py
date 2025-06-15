from pathlib import Path
from prefect import flow
from prefect_dbt.cli.commands import trigger_dbt_cli_command

@flow(log_prints=True)
def my_dbt_flow():
    result = trigger_dbt_cli_command(
        command="run --select setup --target dev --profiles-dir .",
        project_dir=str(Path(__file__).parent.parent),   # Convert to string
        profiles_dir=str(Path(__file__).parent.parent),  # Convert to string
    )
    print(result)

if __name__ == "__main__":
    my_dbt_flow()
