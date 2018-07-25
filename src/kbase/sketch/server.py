import os
import shutil
import flask
from dotenv import load_dotenv

from .download_file import download_file
from .generate_sketch import generate_sketch

load_dotenv('.env')

app = flask.Flask(__name__)
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', True)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


@app.route('/', methods=['GET'])
def root():
    """Root path for the entire service"""
    return "Usage: GET /shock_id.\nFor example: GET /ce9dcf92-019c-41d2-8523-6d36c889a5ca"


@app.route('/<shock_id>', methods=['GET'])
def get_sketch(shock_id):
    """Generate a sketch from a given genome."""
    if not shock_id:
        return ("Enter a Shock ID in the request path", 422)
    download_result = download_file(shock_id, 'xyz')

    @flask.after_this_request
    def cleanup(response):
        # Remove temporary file when the request is completed.
        if download_result.downloaded_file:
            shutil.rmtree(download_result.downloaded_file.dir_path)
        return response

    if download_result.error:
        json = {'status': 'error', 'error': download_result.error}
        return (flask.jsonify(json), 400)
    downloaded_file = download_result.downloaded_file
    # path = result.downloaded_file.tmp_file.name
    # filename = result.downloaded_file.filename
    sketch_result = generate_sketch(downloaded_file)
    return flask.send_file(
        sketch_result.path,
        as_attachment=True,
        attachment_filename=sketch_result.file_name
    )
