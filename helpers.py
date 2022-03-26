import pandas as pd
import os
import sqlalchemy as sa


def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def modify_uploaded_file(filename):
    read_file = pd.read_excel(f'./file_uploads/{filename}')
    clean_filename = filename.rsplit('.', 1)[0]
    read_file.to_csv(f'./file_uploads/{clean_filename}.csv', index=None, header=False)
    os.remove(f'./file_uploads/{filename}')
    return f'{clean_filename}.csv'


def upload_to_db(filename):
    data = pd.read_csv(f'./file_uploads/{filename}')
    oracle_db = sa.create_engine('oracle+cx_oracle://tip:AaZZ0r_cle#1@iberiadb_medium')
    connection = oracle_db.connect()
    data.to_sql('monthly_incidents_raised', con=connection, if_exists='append', chunksize=1000, index=False)
    print("Record inserted successfully")
