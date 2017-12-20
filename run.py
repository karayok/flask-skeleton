from multiprocessing.dummy import Pool

import os

from dotenv import load_dotenv, find_dotenv
from flask.cli import with_appcontext

from myapp import app, create_app, Database
from myapp.models import User, Score


@app.cli.command(help='Calculate user\'s score and register')
@with_appcontext
def register_user_scores():
    users = User.get_users()
    p = Pool(os.cpu_count() if os.cpu_count() else 1)
    for user in users:
        p.apply_async(_calc_scores, (user['id'],), error_callback=_callback_error)
    p.close()
    p.join()


# private

def _calc_scores(user_id: int):
    with app.app_context():
        score = sum(j * user_id for j in range(10000))
        Score.create_score(user_id, score)
        Database.commit()


def _callback_error(e: Exception):
    with app.app_context():
        app.logger.error(e)


if __name__ == 'run' or __name__ == 'main':
    load_dotenv(find_dotenv())
    config_name = os.getenv('FLASK_CONFIG', 'default')
    create_app(config_name)
