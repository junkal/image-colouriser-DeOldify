print("[INFO] *** Loading DeOldify model and starting Flask server..."
		  "please wait until server has fully started ***")

import io, os, base64
import flask
import torch
import time
from deoldify import device
from deoldify.device_id import DeviceId
#choices:  CPU, GPU0...GPU7
device.set(device=DeviceId.GPU0)

if not torch.cuda.is_available():
    print('[INFO]: GPU not available')

import fastai
from deoldify.visualize import *

app = flask.Flask(__name__)

## global variables
colorizer = get_image_colorizer(artistic=False)
upload_directory = './upload'
model_directory = './models'

def create_directory(path):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)

def get_model(url, output_path):
    if os.path.exists(output_path):
        print("[get_model]: Model file ColorizeStable_gen.pth exist... not downloading")
    else:
        print("[get_model]: Downloading model file from {}".format(url))
        cmd = "wget %s -O %s" % (url, output_path)
        os.system(cmd)

@app.route("/process", methods=["POST"])
def process_image():
    data = {"success": False}

    if 'filename' in flask.request.files:
        filename = flask.request.files["filename"].read().decode("utf-8")
        path = upload_directory + '/' + filename
        image = flask.request.files["file"].read()
        image = Image.open(io.BytesIO(image))
        image.save(path)

        start = time.time()
        image_path = colorizer.get_transformed_image(path=path, render_factor=35)
        end = time.time()

        colorised_image = Image.open(image_path, mode = 'r')
        byteIO = io.BytesIO()
        colorised_image.save(byteIO, format='jpeg')
        im_b64 = base64.b64encode(byteIO.getvalue()).decode('utf-8')

        data['filename'] = os.path.splitext(filename)[0] + '_colourised.jpeg'
        data['image'] = im_b64
        data["size"] = colorised_image.size
        data["success"] = True
        data["time"] = end - start

        os.remove(image_path)
        os.remove(path)

        return flask.jsonify(data)

    return flask.jsonify(data)

def main():
	create_directory(model_directory)
	create_directory(upload_directory)

	model_url = "https://www.dropbox.com/s/usf7uifrctqw9rl/ColorizeStable_gen.pth?dl=0"
	get_model(model_url, os.path.join(model_directory, "ColorizeStable_gen.pth"))

	# app.run(host="127.0.0.1", port=4000, debug=True)
	app.run(host="127.0.0.1", debug=True)

if __name__ == "__main__":
    main()
