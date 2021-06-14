import os
from app import app
from util.page_classifier import execute

from flask import flash, request, redirect, render_template, jsonify
from werkzeug.utils import secure_filename
from redis import Redis

redis = Redis(host="0.0.0.0", port=6379)

ALLOWED_EXTENSIONS = ['html']

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
	visits = redis.incr('counter')
	return render_template('upload.html', visits=visits)

@app.route('/refresh')
def refresh():
	# empty directory
	cwd = app.config['UPLOAD_FOLDER']
	if os.listdir(cwd):
		for f in os.listdir(cwd):
			os.remove(os.path.join(cwd, f))
	return redirect('/')

@app.route('/', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)

	file = request.files['file']

	if file.filename == '':
		flash('No file selected for upload')
		return redirect(request.url)

	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		file.save(filepath)
		resp = jsonify(execute(filepath))
		resp.status_code = 201
		return resp
	else:
		flash('Receives only .html file extension')
		return redirect(request.url)
