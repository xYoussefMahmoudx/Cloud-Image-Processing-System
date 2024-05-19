import base64
import cv2
import numpy as np
from flask import Flask, request, jsonify
from worker_thread import processImage
def log_message():
    with open("log.txt", "a") as log_file:
        log_file.write("I am here\n")

processing_app = Flask(__name__)

@processing_app.route("/processImage", methods=['POST'])
def image_process():
    log_message()
    data = request.json
    image_data = data.get("image_data")
    selected_option = data.get("selected_option")

    if not image_data or not selected_option:
        return jsonify({"error": "Invalid input"}), 400

    # Decode the base64 image
    nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Process the image
    processed_image = processImage(image, selected_option)

    # Encode the processed image to base64
    _, buffer = cv2.imencode('.jpeg', processed_image)
    processed_image_data = base64.b64encode(buffer).decode('utf-8')

    return jsonify({"processed_image_data": processed_image_data, "message": "I am in vm2"})

if __name__ == "__main__":
    processing_app.run(debug=True, host='0.0.0.0', port=5001)