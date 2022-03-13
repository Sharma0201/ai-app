from flask import (Blueprint, flash, g, redirect, render_template, url_for, request)

from app.db import get_db

bp = Blueprint('task', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():
    from app.ai.summary import summarize
    if request.method == 'POST':
        passage = request.form['passage']
        error = None
        userid = -1
        if g.user is not None:
            userid = g.user['id']
        if not passage:
            error = 'Write some content in it'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            summary = summarize(passage)
            db.execute('INSERT INTO summary (summary_text, passage, author_id) VALUES (?,?,?)',
                       (summary, passage, userid))
            db.commit()
            return render_template('task/summary.html', summary=summary, issummary=True)
    return render_template('task/summary.html', issummary=False)


# list all the history of user summary task after login
@bp.route('/show')
def show():
    user = -1
    if g.user is not None:
        user = g.user['id']
    error = None
    db = get_db()
    if user == -1:
        error = "user not logged in"

    if error is not None:
        flash(error)
    else:
        # allsummary = db.execute('SELECT * from summary where author_id = ?', (user,)).fetchall()
        allsummary = db.execute('SELECT * FROM summary s JOIN user u ON s.author_id = u.id WHERE u.id = ? ORDER BY created DESC', (user,)) \
            .fetchall()
        return render_template('task/showall.html', allsummary=allsummary)
    return redirect(url_for('task.index'))
