import os
import logging
from logging import Formatter, FileHandler
from flask import Flask, request, jsonify, render_template, Response
import jsonpickle

from ocr import process_image, process_image_data

app = Flask(__name__)
_VERSION = 1  # API version


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/v{}/ocr'.format(_VERSION), methods=["POST"])
def ocr():
    try:
        url = request.json['image_url']
        if 'jpg' in url:
            output = process_image(url)
            return jsonify({"output": output})
        else:
            return jsonify({"error": "only .jpg files, please"})
    except Exception as e:
        logging.exception(e)
        return jsonify(
            {"error": "Did you mean to send: {'image_url': 'some_jpeg_url'}"}
        )


# route http posts to this method
@app.route('/v{}/data'.format(_VERSION), methods=['POST'])
def data():
    try:
        # encode response using jsonpickle
        response_pickled = jsonpickle.encode(process_image_data(request.data))
        return Response(response=response_pickled, status=200, mimetype="application/json")
    except Exception as e:
        logging.exception(e)
        return jsonify(
            {"message": "The image could not be decoded"}
        )


@app.route('/v{}/health'.format(_VERSION), methods=["GET"])
def health():
    return "OK"


@app.errorhandler(500)
def internal_error(error):
    print str(error)  # ghetto logging


@app.errorhandler(404)
def not_found_error(error):
    print str(error)

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: \
            %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
