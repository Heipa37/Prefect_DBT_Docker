input_sql_path = "stg_schema_setup.sql"
output_macro_path = "makro_stg_schema_setup.sql"
macro_name = "stg_schema_setup"

with open(input_sql_path, "r") as f:
    sql_lines = [line.strip() for line in f if line.strip()]
    sql_lines_no_comments = []
    for line in sql_lines:
        sql_lines_no_comments.append(line.split("--", 1)[0].strip())
    sql_lines_no_comments = [line for line in sql_lines_no_comments if len(line) > 0]  # Remove empty lines
    script = "\n                    ".join(sql_lines_no_comments)
    statements = script.split(";")


with open(output_macro_path, "w") as f:
    f.write(f"{{% macro {macro_name}() %}}\n")
    for line in statements:
        if line.endswith(";"):
            line = line[:-1]
        f.write(f"    {{% do run_query(\"{line}\") %}}\n")
    f.write("{% endmacro %}\n")