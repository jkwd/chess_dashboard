from setuptools import find_packages, setup

setup(
    name="chess",
    packages=find_packages(exclude=["chess_tests"]),
    install_requires=[
        "dagster",
        "duckdb",
        "dagster-embedded-elt",
        "dagster-duckdb-pandas",
        "dagster-duckdb",
        "dlt[duckdb]",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest", "jupyter"]},
)
