# all the imports
import os
from flask import Flask, request, session, jsonify, abort
from watson_developer_cloud import SpeechToTextV1
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['wav'])

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('main.cfg')

speech_to_text = SpeechToTextV1(
    username=app.config['WATSON_USERNAME'],
    password=app.config['WATSON_PASSWORD'],
    x_watson_learning_opt_out=False
)

@app.route('/')
def index():
    return jsonify('Winter is Coming.')

# can be POST /nlp - which is audio input
# or GET /nlp?text=i+have+a+dog - which is text input
@app.route('/nlp', methods=['GET', 'POST'])
def nlp():
    text_in = request.args.get('text','')

    # if text param is present and is true
    if text_in is not None:
        text_out = text_in
    else:
        if 'file' not in request.files:
            abort(400)
        audio_in = request.files['audio_wav_file']
        if audio_in and allowed_file(audio_in.filename):
            audio_filename = secure_filename(audio_in.filename)

            audio_in.save(os.path.join(app.config['UPLOAD_FOLDER'],
                          audio_filename))
        # TODO: chunk audio if needed, apply s2t on audio
        # textOut = s2t(audio_in)

    # TODO:
    # Fire off job to build entity graph - think about concurency?
    # do syncronously for now

    text_out = "I have a dog.  Its name is Lisa." # sample text

    # return 200 and audio text
    return jsonify(text=text_out)

@app.route('/graph', methods=['GET'])
def graph():
    return jsonify(nodes=['test_node'])

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
