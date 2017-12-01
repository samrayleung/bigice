import os
from datetime import datetime

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager, Shell
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'eynPB0JVh5hAhz9cTWiFmetQIQ1qdcLOArWw1q40vvhZ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'bigice.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
manager = Manager(app)


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    from_user_name = db.Column(db.String(100))
    to_user_name = db.Column(db.String(100))
    content = db.Column(db.Text)
    msg_type = db.Column(db.Integer)
    file_name = db.Column(db.String(100))
    status = db.Column(db.Integer)
    url = db.Column(db.String(100))
    recommend_info = db.Column(db.String(100))
    timestamp = db.Column(db.String(100))


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


@app.route("/<int:page>", methods=['GET', 'POST'])
def index(page=1):
    per_page = 10
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name = ''
    messages = Message.query.paginate(page, per_page, error_out=False)
    return render_template('index.html',
                           form=form, name=name, messages=messages)


def unixtime_to_datetime(value):
    if value:
        return datetime.fromtimestamp(int(value)).strftime('%Y-%m-%d %H:%M:%S')


app.jinja_env.filters['datetime'] = unixtime_to_datetime


def make_shell_context():
    return dict(app=app, db=db, Message=Message)


manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == "__main__":
    # app.run(debug=True)
    manager.run()
