from sqlalchemy import text

def execute_psql_script(path_to_script, conn):
    with open(path_to_script) as file:
        query = text(file.read())
        conn.execute(query)
        conn.commit()