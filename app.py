from flask import Flask, redirect, request, render_template, url_for, send_from_directory
from werkzeug import secure_filename
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'Files/'
ALLOWED_EXTENSION = set(['txt'])

def if_defined(filename) :
	return '.' in filename and \
		filename.rsplit('.',1)[1] in ALLOWED_EXTENSION

@app.route('/')
def index():
	return render_template('home.html')

@app.route('/upload', methods=['POST'])
def uploadFile():
	file = request.files['file']
	if file and if_defined(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
		return redirect(url_for('uploaded_file', filename=filename))

@app.route('/upload/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/downloads/<filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)

if __name__ == '__main__':
	app.run(debug=True)


