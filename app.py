import pymysql
from flask import Flask, render_template, g, session, redirect, url_for, request, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ThisIsTheKey'
app.config['USERNAME'] = 'admin'
app.config['PASSWORD'] = 'admin'

#返回一个新的数据库连接
def connect_db():
    return pymysql.connect(host='127.0.0.1',
            user='root',
            passwd='will',
            db='saidb',
            charset='utf8')

#每次请求，都专门创建一个新的数据库连接
@app.before_request
def Sai_b_r():
    g.db = connect_db()

#每次请求执行后，都关闭为本次请求创建的数据库连接
@app.after_request
def Sai_a_r(response):
    g.db.close()
    return response


@app.route('/')
def show_todo_list():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        sql = 'select id, user_id, title, status, create_time from todolist'
        with g.db as cur:
            cur.execute(sql)
            data = cur.fetchall()
            todo_list = [ dict(id=row[0], user_id=row[1], title=row[2], status=bool(row[3]), create_time=row[4]) for row in data]
        return render_template('index.html', todo_list=todo_list)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            flash('Invalid username')
        elif request.form['password'] != app.config['PASSWORD']:
            flash('Invalid password')
        else:
            session['logged_in'] = True
            flash('you have logged in!')
            return redirect(url_for('show_todo_list'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('you have logout!')
    return redirect(url_for('login'))

if __name__ == '__main__':
	# app.run(host='0.0.0.0', port=5000, debug=False)
	app.run(host='0.0.0.0', port=5000, debug=True)