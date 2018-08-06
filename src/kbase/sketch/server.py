import tempfile
import os
import shutil
import flask
from dotenv import load_dotenv

from .autodownload import autodownload, UnrecognizedWSType
from kbase_workspace_utils.exceptions import InvalidUser, InaccessibleWSObject, InvalidGenome
from .generate_sketch import generate_sketch
from .perform_search import perform_search

load_dotenv()

app = flask.Flask(__name__)
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', True)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


@app.route('/', methods=['GET'])
def root():
    """Root path for the entire service"""
    return "Usage: GET /search/workspace_id. Example: GET /search/1/2/3"


@app.route('/search/<ws_id>/<obj_id>/<obj_ver>', methods=['GET'])
def get_sketch(ws_id, obj_id, obj_ver):
    """Generate a sketch from a given genome."""
    ws_ref = '/'.join([ws_id, obj_id, obj_ver])
    # For each sketch, we make and remove a temporary directory
    tmp_dir = tempfile.mkdtemp()
    (path, paired_end) = autodownload(ref=ws_ref, save_dir=tmp_dir)
    sketch_result = generate_sketch(path, paired_end)
    search_result = perform_search(sketch_result)
    shutil.rmtree(tmp_dir)
    return search_result


@app.errorhandler(InvalidUser)
@app.errorhandler(UnrecognizedWSType)
@app.errorhandler(InvalidGenome)
@app.errorhandler(InaccessibleWSObject)
def invalid_user(err):
    """Generic exception catcher, returning 400."""
    return (flask.jsonify({'status': 'error', 'message': str(err)}), 400)


@app.errorhandler(404)
def page_not_found(err):
    return (flask.jsonify({'status': 'error', 'message': 'Page not found'}), 404)


@app.errorhandler(Exception)
def any_exception(err):
    """A catch-all for any exceptions we didn't handle above."""
    return (flask.jsonify({'status': 'error', 'message': 'An unknown error occurred'}), 500)
