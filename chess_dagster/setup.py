from setuptools import find_packages, setup

setup(
    name="chess",
    packages=find_packages(exclude=["chess_tests"]),
    install_requires=[
        "dagster==1.8.0",
        "dagster-webserver==1.8.0",
        "dagster-postgres==0.24.0",
        "dagster-embedded-elt==0.24.0",
        "dagster-duckdb-pandas==0.24.0",
        "dagster-duckdb==0.24.0",
        "duckdb==0.10.3",
        "dlt[duckdb]==0.5.3",
        "python-chess==1.2.0",
    ],
    extras_require={
        "dev": ["pytest==8.3.2", "jupyter==1.0.0", "flake8==7.1.1"]
    },
)
