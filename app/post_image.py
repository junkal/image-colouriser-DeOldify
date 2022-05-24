import io, os, base64
import argparse
import requests
from PIL import Image

def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", type = str, required = True, default=None, help="path to image to send processing")
    parser.add_argument("-o", "--output", type= str, default='post_responses', help="output folder to store return images")
    parser.add_argument("-ip", type = str, default='127.0.0.1:4000', help="ip address:port of service")

    return parser

def process_image(image, url, output_folder):
    filename = os.path.basename(image)
    file_ext = os.path.splitext(filename)[1]

    if file_ext in ['.jpg', '.png', '.jpeg']:
        image = Image.open(image, mode = 'r')
        byteIO = io.BytesIO()
        image.save(byteIO, format=file_ext[1:])
        image = byteIO.getvalue()

        payload = {"filename": filename, "file": image}
        response = requests.post(url+"process", files=payload)

        data = response.json()

        print("[INFO] POST successful, success: {}, filename: {}, time taken: {}s"
                .format(data["success"], data['filename'], data["time"]))

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        with open(os.path.join(output_folder, data['filename']), "wb") as fh:
            fh.write(base64.b64decode(data['image']))

        print("[INFO] Returned {} saved at {}".format(data['filename'], os.path.abspath(output_folder)))

def main(args = None):
    parser = parse_opt()
    args = parser.parse_args(args)

    URL = "http://" + args.ip + "//"

    if args.image != None:
        process_image(args.image, URL, args.output)
    else:
        print("[ERROR] No input image defined")

if __name__ == '__main__':
    main()
