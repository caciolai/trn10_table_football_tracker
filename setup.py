from setuptools import find_packages, setup

setup(
    name="trn10_table_football",
    version="1.0",
    packages=find_packages(where="src", exclude=("test",)),
    package_dir={"": "src"},
    package_data={},
    requires=[
        "pandas",
        "streamlit",
        "st_files_connection",
        "s3fs"
    ]
)
