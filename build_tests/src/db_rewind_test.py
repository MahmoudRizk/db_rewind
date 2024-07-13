import datetime
import subprocess
import sys
import time
from typing import Callable
from collections import namedtuple

Response = namedtuple('Response', ['returncode', 'stdout', 'stderr'])

def set_db_rewinding_configurations() -> str:
    print('Running set_db_rewinding_configurations script')
    return 'python3 /opt/db_rewind/main.py setup --disable-user-interaction'

def rewind_db(date_time: str) -> str:
    print(f'Running rewind_db script at date {date_time}')
    return f"python3 /opt/db_rewind/main.py rewind --disable-user-interaction --db-rewind-date '{date_time}'"

def insert_test_record() -> str:
    print('Running insert test record')
    return f"su - postgres -c 'psql -f /opt/db_rewind/build_tests/src/insert_test_record.sql'"

def assert_successful_rewinding_by_records_count(records_count: int) -> str:
    print(f"Asserting successful rewinding by records count eq: {records_count}")

    psql_query = "psql -d test -c 'select count(*) from posts;'"
    
    return f"""su - postgres -c "{psql_query}" | head -n 3 | tail -n 1 | grep -E '^[[:space:]]*{records_count}$'"""

def execute_command(command: str) -> Response:
    try:
        res = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return Response(returncode=res.returncode, stdout=res.stdout, stderr=res.stderr)
    except subprocess.CalledProcessError as e:
        return Response(returncode=e.returncode, stdout=e.stdout, stderr=e.stderr)

def format_date_time(date_time: datetime.datetime) -> str:
    return date_time.strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    def _execute(callback: Callable) -> None:
        res: Response = callback()
        print(res)
        if res.returncode != 0:
            print('An error has occurred during db rewind testing.')
            print(res.stderr)
            sys.exit(res.returncode)
    
    _execute(lambda: execute_command(set_db_rewinding_configurations()))
    
    _execute(lambda: execute_command(insert_test_record()))
    
    # Sleep for one second to get initial time stamp after 1 second of first record insertion.
    time.sleep(1)
    initial_date_time = datetime.datetime.now(datetime.timezone.utc)
    
    _execute(lambda: execute_command(insert_test_record()))

    _execute(lambda: execute_command(rewind_db(format_date_time(initial_date_time))))

    _execute(lambda: execute_command(assert_successful_rewinding_by_records_count(1)))

    sys.exit(0)