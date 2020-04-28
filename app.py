import pymysql
from flask import Flask, render_template, g

app = Flask(__name__)
app.secret_key = 'This is my key'

#返回一个新的数据库连接
def connect_db():
    return pymysql.connect(host='127.0.0.1',
            user='root',
            passwd='will',
            db='saidb',
            charset='utf8')

#每次请求，都专门创建一个新的数据库连接
@app.before_request
def before_request():
    g.db = connect_db()

#每次请求执行后，都关闭为本次请求创建的数据库连接
@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def show_todo_list():
    sql = 'select id, user_id, title, status, create_time from todolist'
    with g.db as cur:
        cur.execute(sql)
        data = cur.fetchall()
        todo_list = [ dict(id=row[0], user_id=row[1], title=row[2], status=bool(row[3]), create_time=row[4]) for row in data]
    return render_template('index.html', todo_list=todo_list)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)