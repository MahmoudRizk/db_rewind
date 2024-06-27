import datetime
import subprocess
import sys
from typing import Callable
from collections import namedtuple

Response = namedtuple('Response', ['returncode', 'stdout', 'stderr'])

def set_db_rewinding_configurations() -> str:
    print('Running set_db_rewinding_configurations script')
    return 'python3 /opt/db_rewind/main.py setup --disable-user-interaction'

def rewind_db(date_time: str) -> str:
    print('Running rewind_db script')
    return f"python3 /opt/db_rewind/main.py rewind --disable-user-interaction --db-rewind-date '{date_time}'"

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
    
    initial_date_time = datetime.datetime.now(datetime.timezone.utc)
    _execute(lambda: execute_command(set_db_rewinding_configurations()))
    _execute(lambda: execute_command(rewind_db(format_date_time(initial_date_time))))

    sys.exit(0)