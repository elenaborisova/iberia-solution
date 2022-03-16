import os
from flask import Flask, render_template, request, url_for
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename, redirect
import pandas as pd
import requests
import cx_Oracle

app = Flask(__name__, static_url_path='/static', template_folder='templates')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

UPLOAD_FOLDER = './file_uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xlsm', 'xltx', 'xltm', 'xml'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

os.environ['TNS_ADMIN'] = '/Users/elenaborisova/Documents/GitHub/iberia-solution/wallet'
lib_dir = os.path.join(os.environ.get("HOME"), "Downloads", "instantclient_19_8")
cx_Oracle.init_oracle_client(lib_dir=lib_dir)
connection = cx_Oracle.connect("tip", "AaZZ0r_cle#1", "iberiadb_medium")
cursor = connection.cursor()
# cursor.execute("select * from MONTHLY_INCIDENTS_RAISED where inc_code = 'INC000001470894'")
# r = cursor.fetchone()
# print(r)


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
    return f'{clean_filename}.csv'


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
            filename_csv = modify_uploaded_file(filename)
            process_incraised_data(filename_csv)
            return redirect(url_for('upload_file', msg='File uploaded successfully'))


def process_incraised_data(filename):
    # headers = CaseInsensitiveDict()
    # headers["Accept"] = "application/json"
    url = 'https://g5cb9edca1cffa5-iberiadb.adb.eu-milan-1.oraclecloudapps.com/ords/tip/monthly_incidents_raised/incraised/'
    data = requests.get(url)


if __name__ == '__main__':
    app.run()
