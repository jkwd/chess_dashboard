from setuptools import find_packages, setup

setup(
    name="chess",
    packages=find_packages(exclude=["chess_tests"]),
    install_requires=[
        "pydantic==2.9.1",
        "pydantic_core==2.23.3",
        "duckdb==1.1.3",
        "dagster==1.8.0",
        "dagster-webserver==1.8.0",
        "dagster-postgres==0.24.0",
        "dagster-embedded-elt==0.24.0",
        "dagster-duckdb-pandas==0.24.0",
        "dagster-duckdb==0.24.0",
        "dlt[duckdb]==1.3.0",
        "python-chess==1.2.0",
    ],
    extras_require={
        "dev": ["pytest==8.3.2", "jupyter==1.0.0", "flake8==7.1.1"]
    },
)
