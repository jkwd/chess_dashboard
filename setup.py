from setuptools import find_packages, setup

setup(
    name="chess",
    packages=find_packages(exclude=["chess_tests"]),
    install_requires=[
        "duckdb==0.10.3",
        "dagster==1.8.0",
        "dagster-embedded-elt==0.24.0",
        "dagster-duckdb-pandas==0.24.0",
        "dagster-duckdb==0.24.0",
        "dlt[duckdb]==0.5.3",
        "python-chess==1.2.0",
    ],
    extras_require={"dev": ["dagster-webserver==1.8.0", "pytest==8.3.2", "jupyter==1.0.0"]},
)
