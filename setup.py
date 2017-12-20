import sys

from setuptools import setup, find_packages

if sys.version_info < (3, 5):
    sys.exit('Oops! Python < 3.5 is not supported')

setup(
    name='Sample.flask-skelton',
    version=0.1,
    url='git@github.com:KarageAgeta/flask-skeleton.git',
    author='Yoko Karasaki',
    author_email='yoko.karasaki@gmail.com',
    description='A skeleton for CLI tools using Flask + SQLAlchemy + multiprocessing',
    packages=find_packages(),
    install_requires=[
        'Flask>=0.12.2',
        'Flask-SQLAlchemy',
        'Flask-SQLAlchemy-Session',
        'python-dotenv',
        'SQLAlchemy[pymysql]'
    ],
    tests_require=[
        'pytest>=3',
        'flake8'
    ],
    extras_require={
        'debug': [
            'pytest>=3',
            'flake8'
        ]
    },
)
