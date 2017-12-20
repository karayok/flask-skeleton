※ [エキサイト Advent Calendar 2017](https://qiita.com/advent-calendar/2017/excite) の 12/20 の記事と同一の内容です。

はじめに
===
このエントリーは、 [エキサイト Advent Calendar 2017](https://qiita.com/advent-calendar/2017/excite) の 12/20 の記事です。

この記事は Flask + SQLAlchemy + multiprocessing を使用した際にハマった部分をまとめました。

なお、本記事内の全体のコードは [GitHub](https://github.com/KarageAgeta/Sample.Flask-Skeleton) 上に置かれています。

Pull Request 、編集リクエスト等大歓迎です。よろしくお願い致します。


環境
===
- Ubuntu 16.04.3 LTS
- Python 3.6.2
- MySQL 5.7


multiprocessing
===
コード
---
multiprocessing.Pool を使用した並行処理のサンプルです。

```python
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


def _callback_error(e: Exception):
    with app.app_context():
        app.logger.error(e)
```

解説
---
### Pool
Pool は、指定された数のプロセスをプーリングし、適宜空いているプロセスにタスクを割り振ってくれます。

```python
Pool(os.cpu_count())
```

と指定することで、システムの CPU の数だけプロセスをプーリングしてくれます。

`os.cpu_count()` は CPU の数がカウントできなかった場合に `None` が返るため、注意が必要です。

また、似たような関数で `multiprocessing.cpu_count()` があり、こちらを使っているサンプルコードも多いのですが、
 Python 3.4 以降は `os.cpu_count()` を使うほうが良さそうです。

### ワーカーの実行
ワーカーを実行するためのメソッドはいくつかありますが、よく使われるものを挙げます。

| Method | Detail |
|--------|--------|
| apply() | 複数の引数を伴って与えられたメソッドを呼び出す。結果が出るまでブロックする|
| apply_async() | 複数の引数を伴って与えられたメソッドを非同期で呼び出す。 `AsyncResult` オブジェクトを返す |
| map() | 組み込み関数 `map()` の並列版。単一引数のみ |
| map_async() | `map()` の非同期版。 `AsyncResult` オブジェクトを返す|


上のサンプルでは `apply_async()` を使用しています。

`apply_async()` 、 `map_async()` などは `AsyncResult.get()` でワーカーの結果を受け取る事ができます。

ただし、ワーカーで発生した例外を受け取って処理をしたい場合は `error_callback` を指定してあげる方が扱いやすいです。


Session
===
sessionmaker() と scoped_session()
---
SQLAlchemy でセッションを生成する方法は `scoped_session()` と `sessionmaker()` の2種類があります。

| Type | Detail |
|------|--------|
| scoped_session() | 複数回呼び出しても1つの共通のセッションを返す。セッションが明示的に破棄されるまで、同じセッションのレジストリを保持し続ける |
| sessionmaker() | 呼び出す度に新しいセッションを生成する |

並列で処理する場合は `scoped_session()` は使えないため、 `sessionmaker()`  を使う必要があります。

```python
session = sessionmaker(autocommit=False,
                       autoflush=True,
                       expire_on_commit=False,
                       bind=engine)
```

Flask-SQLAlchemy-Session を使用する
---
`sessionmaker()` を使用する場合、適切にセッションの管理を行う必要があります。

Flask を使用する場合は Flask-SQLAlchemy-Session を使うと適切に処理してくれます。

init 時に `flask_scoped_session()` を設定します。

```python
app = Flask(__name__)
engine = create_engine(
    'mysql+pymysql://user:pass@localhost/test?charset=utf8mb4', encoding='utf-8')

flask_scoped_session(sessionmaker(
            autocommit=False,
            autoflush=True,
            expire_on_commit=False,
            bind=engine), app)
```

add や commit するときは `current_session` を使用します。

```python
user = User(1, 'Scott')

current_session.add(user)
current_session.commit()
```

その他
===
Python3 + MySQL
---
SQLAlchemy のデフォルトのドライバが [MySQL-Python](https://github.com/farcepest/MySQLdb1) のようなのですが、
こちらは Python3 に対応していないため、 Python3 で実装する場合は別のドライバをインストールする必要があります。

候補としては以下のものがあります。

| Dialect | Detail |
|---------|--------|
| [mysqlclient-python](https://github.com/PyMySQL/mysqlclient-python) | MySQL-Python から fork された Python3 対応版 |
| [PyMySQL](https://github.com/PyMySQL/PyMySQL) | Python のみで実装。MySQL-Python と完全互換 |
| [mysql-connector-python](https://pypi.python.org/pypi/mysql-connector-python/) | MySQL 公式 |

また、 MySQL の encoding を `utf8mb4` にする場合は PyMySQL のみが対応しています。

特にこだわりがなければ PyMySQL がオススメです。

ちなみに、 SQLAlchemy の `extras_require` に PyMySQL が含まれているので、 
setup.py 内で以下のように指定すると、一緒に PyMySQL もインストールできます。

**setup.py**

```python
setup(
    install_requires=[
        'SQLAlchemy[pymysql]'
    ]
)
```

**Connection String**

```python
engine = create_engine(
    'mysql+pymysql://user:pass@localhost/test?charset=utf8mb4', encoding='utf-8')
```

まとめ
---
- Python 3.4 以降は `os.cpu_count()` の使用を推奨
- 複数の引数を使う際は `multiprocessing.Pool.apply_async()` を使用する
- `apply_async()` 使用時にワーカープロセスの Exception を取得したい場合は `AsyncResult.get()` を使用するか、 `error_callback` を指定
- multiprocessing を使用する場合は `sessionmaker()` を使用する

全体のコードは [GitHub](https://github.com/KarageAgeta/Sample.Flask-Skeleton) にて。

参考
---
- [\[Python\] SQLAlchemyを頑張って高速化](https://qiita.com/yukiB/items/d6a70da802cb5731dc01)
- [17.2.2.9. Process Pools](https://docs.python.org/3.6/library/multiprocessing.html#module-multiprocessing.pool)
- [Python 3.3 までの multiprocessing.cpu_count() が「ぎょえ」で 3.4 以降も継承されてるハナシ](http://hhsprings.pinoko.jp/site-hhs/2016/03/python-3-3-%E3%81%BE%E3%81%A7%E3%81%AE-multiprocessing-cpu_count-%E3%81%8C%E3%80%8C%E3%81%8E%E3%82%87%E3%81%88%E3%80%8D%E3%81%A7-3-4-%E4%BB%A5%E9%99%8D%E3%82%82%E7%B6%99%E6%89%BF%E3%81%95%E3%82%8C/)
- [Contextual/Thread-local Sessions](http://docs.sqlalchemy.org/en/latest/orm/contextual.html)
- [Understanding Python SQLAlchemy’s Session](https://www.pythoncentral.io/understanding-python-sqlalchemy-session/)
- [Flask-SQLAlchemy-Session](http://flask-sqlalchemy-session.readthedocs.io/en/v1.1/)
