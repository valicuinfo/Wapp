import mysql.connector
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

def get_db_connection():
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='blog'
    )
    return mydb

def get_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sqlstmt = 'SELECT * FROM posts WHERE id = ' + str(post_id)
    cursor.execute(sqlstmt)
    post = cursor.fetchone()
    if post is None:
        abort(404)
    return post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'valicu'

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM posts')
    posts = cursor.fetchall()
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = "INSERT INTO posts (title, content) VALUES (%s, %s)"
            val = (title, content)
            cursor.execute(sql,val)
            conn.commit()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            sqlstmt = 'UPDATE posts SET title = "' + title + '", content = "'+ content +'" WHERE id = '+str(id);
            cursor.execute(sqlstmt)
            conn.commit()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    cursor = conn.cursor()
    sqlstmt = 'DELETE FROM posts WHERE id = ' + str(id)
    cursor.execute(sqlstmt)
    conn.commit()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))