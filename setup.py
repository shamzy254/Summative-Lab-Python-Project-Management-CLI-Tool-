from setuptools import find_packages, setup

setup(
    name="project-tracker",
    version="0.1.0",
    description="A command-line project tracker for users, projects, and tasks",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["rich>=13.7.0"],
    entry_points={
        "console_scripts": [
            "project-tracker=src.app:main",
        ],
    },
)
