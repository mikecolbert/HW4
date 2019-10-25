from flask import Flask
from flask import render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
import secrets

conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)

app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
db = SQLAlchemy(app)

class colbert_friends(db.Model):
    friendid = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))

    def __repr__(self):
        return "id: {0} | first name: {1} | last name: {2}".format(self.id, self.first_name, self.last_name)

class FriendForm(FlaskForm):
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])


@app.route('/')
def index():
    all_friends = colbert_friends.query.all()
    return render_template('index.html', friends=all_friends, pageTitle='Mike\'s Friends')

@app.route('/add_friend', methods=['GET', 'POST'])
def add_friend():
    form = FriendForm()
    if form.validate_on_submit():
        friend = colbert_friends(first_name=form.first_name.data, last_name=form.last_name.data)
        db.session.add(friend)
        db.session.commit()
        return redirect('/')

    return render_template('add_friend.html', form=form, pageTitle='Add A New Friend')



if __name__ == '__main__':
    app.run(debug=True)
