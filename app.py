import os
from flask import Flask, render_template

app = Flask(__name__, static_url_path='/static')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def handle_register():
    pass


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def handle_login():
    pass


@app.route('/logout')
def logout():
    pass


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run()
