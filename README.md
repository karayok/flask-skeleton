Sample.Flask-Skeleton
===

A sample project for CLI tool using Flask + SQLAlchemy + multiprocessing

Requirements for development
---
- Python>=3.5
- virtualenv

Getting Started
---
### Clone this repository
```
$ pip3 install virtualenv
$ git clone git@github.com:KarageAgeta/Sample.Flask-Skeleton.git
$ cd flask-skeleton
```

### Edit `.env.copy`
```
$ cp .env.copy .env
$ vi .env
```

### Activate virtualenv and install requirements
```
$ virtualenv venv
$ . venv/bin/activate
$ pip3 install -e ".[debug]"
```

### Set Flasak App path
```
$ export FLASK_APP=run.py
```

Sample Commands
---
Simple calculation and insert scores into DB.
```
$ flask register_user_scores
```

flake8
---
```
$ flake8 run.py myapp
```
