# jorge
from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import time

# import our model from folder
from face_recognition_and_liveness.face_liveness_detection.face_recognition_liveness_app import recognition_liveness

app = Flask(__name__)
app.secret_key = 'web_app_for_face_recognition_and_liveness'  # something super secret
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    dni = db.Column(db.String(100))
    password = db.Column(db.String(100))
    card = db.Column(db.String(100))


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        card = request.form['card']
        dni = request.form['dni']
        password = request.form['password']
        user = Users.query.filter_by(
            card=card, dni=dni).first()

        # print(user.id)
        if user and check_password_hash(user.password, password):
            detected_name, label_name = recognition_liveness('face_recognition_and_liveness/face_liveness_detection/liveness.model',
                                                             'face_recognition_and_liveness/face_liveness_detection/label_encoder.pickle',
                                                             'face_recognition_and_liveness/face_liveness_detection/face_detector',
                                                             'face_recognition_and_liveness/face_recognition/encoded_faces.pickle',
                                                             confidence=0.5)
            if user.fullname == detected_name and label_name == 'real':
                session['id'] = user.id
                session['fullname'] = user.fullname
                return redirect(url_for('main'))
            else:
                return render_template('login_page.html', invalid_user=True, username=user.fullname)
        else:
            return render_template('login_page.html', incorrect=True)
    return render_template('login_page.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # img = request.files['image']
        card = request.form['card']
        fullname = request.form['fullname']
        email = request.form["email"]
        dni = request.form['dni']
        password = request.form['password']
        token = int(round(time.time() * 1000))
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = Users(fullname=fullname, email=email,
                         dni=dni, card=card, password=hashed_password)
        print(new_user)
        db.session.add(new_user)
        db.session.commit()
        print("registradoooo")

        os.mkdir(f'face_recognition_and_liveness/face_recognition/dataset/{fullname}')

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/main', methods=['GET'])
def main():
    try:
        id = session['id']
        fullname = session['fullname']
        print(f'Este es el iddddd {id}')
        return render_template('main_page.html', id=id, fullname=fullname)
    except Exception as e:
        return redirect(url_for('login'))


if __name__ == '__main__':
    db.create_all()

    # add users to database

    # new_user = Users(username='jom_ariya', password='123456789', name='Ariya')
    # db.session.add(new_user)

    # new_user_2 = Users(username='earth_ekaphat', password='123456789', name='Ekaphat')
    # new_user_3 = Users(username='bonus_ekkawit', password='123456789', name='Ekkawit')
    # db.session.add(new_user_2)
    # db.session.add(new_user_3)

    app.run(debug=True)
