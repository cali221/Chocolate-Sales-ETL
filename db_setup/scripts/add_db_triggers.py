from db_setup.utils.execute_psql_script import execute_psql_script
from pathlib import Path

def add_oltp_db_triggers(conn):
    """
    Add triggers for the oltp_online_store schema
    """
    sql_scripts_dir = Path(__file__).parent.parent / "sql_scripts"
    print('Adding triggers for oltp_online_store...')
    execute_psql_script(sql_scripts_dir / 'setup_db_triggers.psql', conn)
    print('Finished adding triggers to oltp_online_store')