import os
from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename, redirect
import pandas as pd

app = Flask(__name__, static_url_path='/static')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

UPLOAD_FOLDER = './file_uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xlsm', 'xltx', 'xltm', 'xml'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000


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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def modify_uploaded_file(filename):
    read_file = pd.read_excel(f'./file_uploads/{filename}')
    clean_filename = filename.rsplit('.', 1)[0]
    read_file.to_csv(f'./file_uploads/{clean_filename}.csv', index=None, header=False)
    os.remove(f'./file_uploads/{filename}')


@app.route('/upload/', defaults={'msg': None})
@app.route('/upload/<msg>')
def upload_file(msg):
    return render_template('upload.html', msg=msg)


@app.route('/uploader', methods=['GET', 'POST'])
def handle_upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(url_for('upload_file', msg='No file part'))
        file = request.files['file']

        if file.filename == '':
            return redirect(url_for('upload_file', msg='No selected file'))

        if not allowed_file(file.filename):
            return redirect(url_for('upload_file', msg='Invalid file format'))

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            modify_uploaded_file(filename)
            return redirect(url_for('upload_file', msg='File uploaded successfully'))


if __name__ == '__main__':
    app.run()
