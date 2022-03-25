import os
from flask import Flask, render_template, request, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename, redirect
# import cx_Oracle

import kpi_data
from helpers import allowed_file, modify_uploaded_file

# Configuration
app = Flask(__name__, static_url_path='/static', template_folder='templates')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

UPLOAD_FOLDER = './file_uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xlsm', 'xltx', 'xltm', 'xml'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000


# # Oracle Client config
# os.environ['TNS_ADMIN'] = '/Users/elenaborisova/Documents/GitHub/iberia-solution/wallet'
# lib_dir = os.path.join(os.environ.get('HOME'), 'Downloads', 'instantclient_19_8')
# cx_Oracle.init_oracle_client(lib_dir=lib_dir)
# connection = cx_Oracle.connect('tip', 'AaZZ0r_cle#1', 'iberiadb_medium')
# cursor = connection.cursor()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register/', defaults={'msg': ' '})
@app.route('/register/<msg>', methods=['GET'])
# @app.route('/register', methods=['GET'])
def register(msg):
    return render_template('register.html', msg=msg)


@app.route('/register', methods=['POST'])
def handle_register():
    # username = request.form['username']
    # email = request.form['email']
    # password = request.form['password']
    # hashed_password = generate_password_hash(password)
    #
    # insert_query = f'''
    #             INSERT INTO registered_users(username, email, password)
    #             VALUES ('{username}', '{email}', '{hashed_password}')
    #             '''
    # cursor.execute(insert_query)
    # connection.commit()

    return redirect(url_for('register', msg='Thank you for registering! Your credentials are being reviewed!'))


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form['username']
    password = request.form['password']

    if username == 'elena' and password == 'elena':
        session['username'] = username
        return redirect(url_for('index'))
    else:
        return render_template('403.html'), 403

    # login_query = f'''
    # SELECT user_id, password
    # FROM authorized_users
    # WHERE username='{username}'
    # '''
    # cursor.execute(login_query)
    # connection.commit()
    # user = cursor.fetchone()
    #
    # if user and check_password_hash(user[1], password):
    #     session['user_id'] = user[1]
    #     session['username'] = username
    #     return redirect(url_for('index'))
    # else:
    #     return render_template('403.html'), 403


@app.route('/logout')
def logout():
    session.pop('username')
    # session.pop('user_id')

    return redirect(url_for('index'))


@app.route('/upload/', defaults={'msg': ' '})
@app.route('/upload/<msg>')
def upload_file(msg):
    if 'username' not in session:
        return render_template('403.html'), 403
    return render_template('upload.html', msg=msg)


@app.route('/uploader', methods=['GET', 'POST'])
def handle_upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(url_for('upload_file', msg='No file part'))
        file = request.files['file']

        if file.filename == '':
            return redirect(url_for('upload_file', msg='No selected file'))

        if not allowed_file(file.filename, ALLOWED_EXTENSIONS):
            return redirect(url_for('upload_file', msg='Invalid file format'))

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            modify_uploaded_file(filename)
            return redirect(url_for('upload_file', msg='File uploaded successfully!'))


@app.route('/dash')
def dashboard():
    if 'username' not in session:
        return render_template('403.html'), 403

    data = {
        'kpi1': kpi_data.get_total_number_of_critical_incidents(),
        'kpi2': kpi_data.get_total_number_of_incidents_per_priority(),
        'kpi3': kpi_data.get_total_number_of_incidents(),
        'kpi4': kpi_data.get_number_of_incidents_backlog_per_priority(),
        'kpi5': kpi_data.get_number_of_incidents_per_cause(),
        'kpi6': kpi_data.get_number_of_incidents_per_status(),
        'kpi7': kpi_data.get_number_of_incidents_per_company_group(),
        'kpi8': kpi_data.get_percentage_of_incidents_meeting_sla(),
    }

    return render_template('dashboard.html', data=data)


if __name__ == '__main__':
    app.run()
