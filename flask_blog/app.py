# import statements
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

# get database connection
def get_db_connection():
# connects to database.db
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    # get correct post by the id
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    # if none is found go to 404 page
    if post is None:
        abort(404)
    return post

app = Flask(__name__)
# secret key used to secure sessions
app.config['SECRET_KEY'] = '12345'


@app.route('/')
def index():
# open database connection
    conn = get_db_connection()
    # select all entries form table and get query result
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close() # close connection
    return render_template('index.html', posts=posts)

# part after slash is a positive integer and pass post_id value
@app.route('/<int:post_id>')
def post(post_id):
    # get post associated with id
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
    # get title and content from form
        title = request.form['title']
        content = request.form['content']
        if not title:
        # if there is no title, flash error message
            flash('Title is required!')
        else:
        # otherwise insert post to database
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                        (title, content))
            conn.commit()
            conn.close()
            # return to index page
            return redirect(url_for('index'))
    return render_template('create.html')

# route to edit post
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
# get post id
    post = get_post(id)
    if request.method == 'POST':
    # get title and content of post
        title = request.form['title']
        content = request.form['content']
        if not title:
        # if there is no title, flash message
           flash('Title is required!')
        else:
            conn = get_db_connection()
            # update posts table where the id is equal to the id of post selected
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
            # render edit page
    return render_template('edit.html', post=post)

# route to delete page
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
# get id of selected post
    post = get_post(id)
    # connect to datbase
    conn = get_db_connection()
    # delete selected post from the database
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close() # close connection
    # flash message that post was successfully deleted
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

#404 error route
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404