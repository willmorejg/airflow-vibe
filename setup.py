
from setuptools import setup, find_packages, Command
import subprocess


DAG_FILE = 'dags/csv_to_duckdb.py'

class IsortCommand(Command):
    description = 'Sort imports using isort.'
    user_options = []
    def initialize_options(self):
        # No initialization needed
        pass
    def finalize_options(self):
        # No finalization needed
        pass
    def run(self):
        subprocess.run(['isort', DAG_FILE], check=True)

class AutoflakeCommand(Command):
    description = 'Remove unused imports and variables using autoflake.'
    user_options = []
    def initialize_options(self):
        # No initialization needed
        pass
    def finalize_options(self):
        # No finalization needed
        pass
    def run(self):
        subprocess.run(['autoflake', '--in-place', '--remove-unused-variables', '--remove-all-unused-imports', DAG_FILE], check=True)

class BlackCommand(Command):
    description = 'Format code using black.'
    user_options = []
    def initialize_options(self):
        # No initialization needed
        pass
    def finalize_options(self):
        # No finalization needed
        pass
    def run(self):
        subprocess.run(['black', DAG_FILE], check=True)

# Custom command to run pytest
class PyTestCommand(Command):
    description = 'Run tests using pytest.'
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        errno = subprocess.call(['pytest', 'tests'])
        raise SystemExit(errno)

class BumpverCommand(Command):
    description = 'Bump version using bumpver.'
    user_options = []
    def initialize_options(self):
        # No initialization needed
        pass
    def finalize_options(self):
        # No finalization needed
        pass
    def run(self):
        subprocess.run(['bumpver', 'update'], check=True)

setup(
    name='airflow_vibe',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'apache-airflow',
        'duckdb',
        'pandas',
    ],
    description='Airflow DAG to consume CSV and persist to DuckDB',
    author='Your Name',
    author_email='your.email@example.com',
    entry_points={},
    cmdclass={
        'isort': IsortCommand,
        'autoflake': AutoflakeCommand,
        'black': BlackCommand,
        'bumpver': BumpverCommand,
        'test': PyTestCommand,
    },
)
