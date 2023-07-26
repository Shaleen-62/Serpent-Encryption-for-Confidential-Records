import os
from flask import Flask,render_template,request, send_file
from flask_cors import CORS
import pandas as pd
import serpentcipherv1

app=Flask(__name__)

CORS(app)

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route("/encryp",methods=["POST","GET"])
def encryp():
    return render_template("encryption.html") 

@app.route("/decryp",methods=["POST","GET"])
def decryp():
    return render_template("decryption.html") 

@app.route("/handle",methods=["POST"])
def handle():
    file = request.files["csv"]
    key=request.form.get('key')
    column_name = request.form.get('column_name');
    file.save(os.path.join('uploads', file.filename))
    df = pd.read_csv(os.path.join('uploads', file.filename))
    column = list(df[column_name])
    encrypted_column = serpentcipherv1.list_enc(column,key)
    df[column_name]=encrypted_column
    df.to_csv(os.path.join('uploads', file.filename))
    return {"file":file.filename}

@app.route("/handled",methods=["POST"])
def handled():
    file = request.files["csv"]
    key=request.form.get('key')
    column_name = request.form.get('column_name');
    file.save(os.path.join('uploads', file.filename))
    df = pd.read_csv(os.path.join('uploads', file.filename))
    column = list(df[column_name])
    decrypted_column = serpentcipherv1.list_dec(column,key)
    df[column_name]=decrypted_column
    df.to_csv(os.path.join('uploads', file.filename),index=False)
    return {"file":file.filename}

@app.route("/download")
def download():
    file = request.args.get('file', type = str)
    return send_file(os.path.join('uploads', file), mimetype='text/csv', download_name='output.csv', as_attachment=True)

if __name__=='__main__':
    app.run(debug=True)