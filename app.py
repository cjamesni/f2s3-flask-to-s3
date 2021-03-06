import os
from flask import Flask, render_template, request, redirect, send_file
from s3_functions import list_files, upload_file, show_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
BUCKET = "f2s3-media-data"


@app.route("/")
def home():
    contents = list_files(BUCKET)
    return render_template('index.html')


@app.route("/files.html")
def list():
    contents = show_file(BUCKET)
    return render_template('collection.html', contents=contents)


@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
        upload_file(f"uploads/{f.filename}", BUCKET)
        return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
