from flask import request, Flask, render_template, url_for, redirect, session, jsonify
from sqlalchemy import Column ,create_engine , String, ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase , sessionmaker, Mapped, mapped_column
from flask_mail import Mail, Message
from config import MAIL, MAIL_PASSWORD
import requests
from datetime import datetime
engine = create_engine("sqlite:///text6.db", echo=True )

Session = sessionmaker(bind=engine)

app = Flask(__name__)
app.config['SECRET_KEY'] = '12212112'


app.config['MAIL_SERVER'] = 'smtp.ukr.net'

app.config['MAIL_PORT'] = 465

app.config['MAIL_USERNAME'] = MAIL

app.config['MAIL_PASSWORD'] = MAIL_PASSWORD

app.config['MAIL_DEFAULT_SENDER'] = MAIL

app.config['MAIL_USE_TLS'] = False

app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

app.app_context().push()

api_key = "6ef4e7612bde555867a4a6aa9c2fe746"

class Base(DeclarativeBase):
    def create_db(self):
        Base.metadata.create_all(engine)

    def drop_db(self):
        Base.metadata.drop_all(engine)


class text(Base):
    __tablename__ = "text"
    id: Mapped[int] = mapped_column(primary_key=True)
    text1: Mapped[int] = mapped_column(String(80))
    user_id: Mapped[int] = mapped_column(ForeignKey('log.id'))

class Login(Base):
    __tablename__ = 'log'
    id:  Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]  = mapped_column(String(80))
    password: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(80))

@app.route('/')
def f_1():
    return render_template('host2.html')


@app.route('/login_pg')
def f_2():
    if session.get("user_id") :
        return redirect(url_for('f_6'))
    else:
        return render_template('login_sijax.html')

@app.route('/sign_up_pg')
def f_3():
    if session.get("user_id") :
        return redirect(url_for('f_6'))
    else:
        return render_template('sign_sijax.html')


@app.route('/login', methods=['POST'])
def f_4():
    name = request.form['name']
    password = request.form['password']

    with Session() as session1:
        user = session1.query(Login).filter_by(name=name, password=password).first()
        if user:
            session['user_id'] = user.id


            email = user.email
            email_message = Message('PogodaUkraine.com', recipients=[email])
            email_message.body = f'Ви увійшли в акаунт! Час входу: {datetime.now()}'
            mail.send(email_message)

            data = {'message': 'Ви ввійшли в акаунт!'}
            return jsonify(data), 200
        else:
            return "Ви ще не зареєстровані!"


@app.route('/signup', methods=['POST'])
def f_5():
    name = request.form['name']
    password = request.form['password']
    email = request.form['email']

    email_message = Message('PogodaUkraine.com', recipients=[email])
    email_message.body = 'Ви заєрестувалися у веб додаток PogodaUkraine.com'

    mail.send(email_message)
    with Session() as session1:
        new_user = Login(name=name, password =password ,email=email)
        session1.add(new_user)
        session1.commit()
        session['user_id'] = new_user.id
        data = {'message': 'Ви зареєструвалися у додаток!!'}
        return jsonify(data), 200


@app.route('/weather_pg')
def f_6():
    return render_template('host.html')


@app.route('/weather', methods = ['POST'])
def f_7():
    city = request.form['text']
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    res = requests.get(url)
    if res.status_code == 200:
        data1 = res.json()
        session1 = session.get('list', [])
        if city not in session1:
            session1.append(city)
            session['list'] = session1
        data = {'Тeмпература': f'{round(data1["main"]["temp"] - 273, 1)}',"Вологість" : f'{data1["main"]["humidity"]}', 'Швидкість вітру:' : f'{data1["wind"]["speed"]}'}

    else:
        data = {'Тeмпература': f'Виникла помилка('}
    return jsonify(data), 200


@app.route('/qwer')
def f_6():
    return 'qweqewr123'


if __name__ == '__main__':
    app.run(debug=True, port=8000)
# base =Base()
# base.create_db()
