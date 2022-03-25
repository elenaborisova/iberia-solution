import pandas as pd
import os


def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def modify_uploaded_file(filename):
    read_file = pd.read_excel(f'./file_uploads/{filename}')
    clean_filename = filename.rsplit('.', 1)[0]
    read_file.to_csv(f'./file_uploads/{clean_filename}.csv', index=None, header=False)
    os.remove(f'./file_uploads/{filename}')
    return f'{clean_filename}.csv'
