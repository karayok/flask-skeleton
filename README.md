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

License
---
```
Copyright 2018 Yoko Karasaki

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
