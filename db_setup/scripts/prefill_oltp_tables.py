from db_setup.utils.execute_psql_script import execute_psql_script
from pathlib import Path

def prefill_oltp_tables(conn):
    """
    Pre-fill tables in oltp_online_store schemas
    """
    print('Filling oltp_online_store tables with initial data...')
    sql_scripts_dir = Path(__file__).parent.parent / "sql_scripts"
    execute_psql_script(sql_scripts_dir / 'prefill_oltp_countries.psql', conn)
    execute_psql_script(sql_scripts_dir / 'prefill_oltp_customers.psql', conn)
    execute_psql_script(sql_scripts_dir / 'prefill_oltp_products.psql', conn)
    execute_psql_script(sql_scripts_dir / 'prefill_oltp_status.psql', conn)
    print('Finished filling oltp_online_store tables with initial data')