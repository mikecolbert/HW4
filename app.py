from flask import Flask
from flask import render_template, redirect, request, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
import secrets

dbUser = os.environ.get('dbuser')
dbPass = os.environ.get('dbpass')
dbHost = os.environ.get('dbhost')
dbName = os.environ.get('dbName')

#conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(dbUser, dbPass, dbHost, dbName)


app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)

class colbert_friends(db.Model):
    #__tablename__ = 'results'
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

@app.route('/friend/new', methods=['GET', 'POST'])
def add_friend():
    form = FriendForm()
    if form.validate_on_submit():
        friend = colbert_friends(first_name=form.first_name.data, last_name=form.last_name.data)
        db.session.add(friend)
        db.session.commit()
        return redirect('/')

    return render_template('add_friend.html', form=form, pageTitle='Add A New Friend',
                            legend="Add A New Friend")


@app.route('/friend/<int:friend_id>', methods=['GET','POST'])
def friend(friend_id):
    friend = colbert_friends.query.get_or_404(friend_id)
    return render_template('friend.html', form=friend, pageTitle='Friend Details')

@app.route('/friend/<int:friend_id>/update', methods=['GET','POST'])
def update_friend(friend_id):
    friend = colbert_friends.query.get_or_404(friend_id)
    form = FriendForm()
    if form.validate_on_submit():
        friend.first_name = form.first_name.data
        friend.last_name = form.last_name.data
        db.session.commit()
        flash('Your friend has been updated.')
        return redirect(url_for('friend', friend_id=friend.friendid))
    #elif request.method == 'GET':
    form.first_name.data = friend.first_name
    form.last_name.data = friend.last_name
    return render_template('add_friend.html', form=form, pageTitle='Update Post',
                            legend="Update A Friend")

@app.route('/friend/<int:friend_id>/delete', methods=['POST'])
def delete_friend(friend_id):
    if request.method == 'POST': #if it's a POST request, delete the friend from the database
        friend = colbert_friends.query.get_or_404(friend_id)
        db.session.delete(friend)
        db.session.commit()
        flash('Friend was successfully deleted!')
        return redirect("/")
    else: #if it's a GET request, send them to the home page
        return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
