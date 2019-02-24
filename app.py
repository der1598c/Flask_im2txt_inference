import os

from flask import Flask, request
# The `ShowAndTellInference` class
from im2txt_inference import ShowAndTellInference

# Create a Flask instance
APP = Flask(__name__)
PWD = os.path.dirname(os.path.realpath(__file__))

# Create a ShowAndTellInference instance. It loads the model into memory.
# And it's ready to run inference!
MODEL_INST = ShowAndTellInference(
    os.path.join(PWD, 'chkpt', 'model.ckpt-1000000'),
    os.path.join(PWD, 'chkpt', 'word_counts.txt'))

# Flask leverages the function decorator for the endpoint registration.
# Register a function to handle POST in '/inference' URI.
@APP.route('/inference', methods=['POST'])
def inference():
    """
    Serve the inference request
    Pass the image in multipart/form-data to the inference function
    """
    if request.method == 'POST':
        return MODEL_INST.inference(request.files['image'])
    return ''

# Start the web server
PORT = os.getenv('PORT', '5000')
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=int(PORT))
