import os
import psycopg2
import urlparse
from flask import Flask, render_template

app = Flask(__name__)
url = urlparse.urlparse(os.environ.get('DATABASE_URL'))
db = 'dbname={} user={} password={} host={}'.format(url.path[1:], url.username,
                                                    url.password, url.hostname)
conn = psycopg2.connect(db)


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/accounts')
def accounts():
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM salesforce.account;")
        accounts = cur.fetchall()
        cur.close()

        return render_template('accounts.html', accounts=accounts)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
