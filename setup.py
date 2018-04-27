from setuptools import setup, find_packages

setup(
    name="sortinghat",
    version="0.1",
    description="Sorts wedding guests on to tables",
    py_modules=(
        "sortinghat",
    ),
    install_requires=(
        "click",
    ),
    entry_points = {
        "console_scripts": [
            "sortinghat=sortinghat:cli",
        ]
    },
)
