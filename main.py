import os
from flask import Flask, request
from ocrmac import ocrmac
import uuid
import json

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'jpg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)

@app.route("/", methods=['POST'])
def ocr():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"
    
    if file and allowed_file(file.filename):
        filename = "/tmp/" + str(uuid.uuid4())
        file.save(filename)
    else:
        return "Missing or invalid filetype"

    # OCR that image
    annotations = ocrmac.OCR(filename, language_preference=['en-US'], recognition_level="accurate").recognize()

    # Remove that image
    os.remove(filename)

    # Return OCR'd text
    response = app.response_class(
        response=json.dumps(annotations, indent=4),
        status=200,
        mimetype='application/json'
    )
    return response
