from pathlib import Path
from setuptools import setup, find_packages

# The directory containing this file
ROOT_DIR = Path(__file__).parent

with open(ROOT_DIR / "README.md", "r") as readme_file:
    long_description = readme_file.read()

with open(ROOT_DIR / "requirements.txt", "r") as requirements_file:
    all_reqs = requirements_file.readlines()


setup(
    name="gcal_notifier",
    description="A simple and lightweight GoogleCalendar notifier for Linux",
    version="1.0.4",
    packages=find_packages(),
    install_requires=all_reqs,
    package_data={'gcal_notifier': ['resources/pop.wav']},
    python_requires=">=3.6",
    entry_points={
        'console_scripts': ['gcal_notifier=gcal_notifier.main:gcal_notifier']
    },
    author="Thales Nunes",
    keyword="google-calendar, notification, linux",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/thalesnunes/SimpleGCalendarNotifier",
    author_email="thalesaknunes22@gmail.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
