import json
import logging
import time

from flask import Flask, jsonify, request, abort, make_response
from flask_autoindex import AutoIndex
from scipy.io import wavfile
from werkzeug.exceptions import HTTPException

from assistantapi.config import DISK_PATH, SAMPLE_RATE
from assistantapi.dash import dash, resolve_cart_id
from assistantapi.stt import transcribe_bytes
from assistantapi.utils import pre_process

app = Flask(__name__)
AutoIndex(app, browse_root=DISK_PATH)



@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    logging.error(e)
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.route('/api')
def api():
    return jsonify({"message": "OK"})


@app.route('/api/transcribe', methods=['POST'])
def process_speech():
    """Transcribes audio bit stream"""
    if request.headers['Content-Type'] == 'application/octet-stream':
        data, dtmf = pre_process(request.data)
        transcription = transcribe_bytes(data, SAMPLE_RATE)
        response = make_response(transcription, 200)
        response.mimetype = "text/plain"
        return response
    else:
        abort(400)


@app.route('/api/save', methods=['POST'])
def save():
    """Saves audio and transcription to disk"""
    if request.headers['Content-Type'] == 'application/octet-stream':
        data, dtmf = pre_process(request.data)
        fname = f"{int(time.time())}"
        wavfile.write(f"{DISK_PATH}/{fname}.wav", SAMPLE_RATE, data)
        transcription = transcribe_bytes(request.data, SAMPLE_RATE)
        with open(f"{DISK_PATH}/{fname}.txt", "w") as f:
            f.write(transcription)

        return jsonify({"message": "OK"})
    else:
        abort(400)


@app.route('/api/dash', methods=['POST'])
def process_dash():
    if request.headers['Content-Type'] == 'application/octet-stream':
        data, dtmf = pre_process(request.data)
        transcription = transcribe_bytes(data, SAMPLE_RATE)
        response = dash(transcription, dtmf)
        return jsonify({"message": str(response)})
    else:
        abort(400)


if __name__ == '__main__':
    resolve_cart_id()
    app.run()
