import base64
from flask import Flask, render_template, request, jsonify, redirect
import os
import requests
import uuid

main_window = Flask(__name__)
main_window.config["upload-path"] = "static/uploadFolder"
main_window.config["download-path"] = "static/downloadFolder"

def list_images_in_folder(folder_path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']  # Add more if needed
    image_paths = []

    # List all files in the folder
    files = os.listdir(folder_path)

    # Filter out only the image files
    for file in files:
        _, extension = os.path.splitext(file)
        if extension.lower() in image_extensions:
            image_paths.append(os.path.join(folder_path, file))

    return image_paths

@main_window.route("/")
def HomePage():
    return render_template("homepage.html")

@main_window.route("/addImage", methods=['POST'])
def image_upload():
    image = request.files["uploaded_image"]

    if image:
        image_path = os.path.join(main_window.config["upload-path"], image.filename)
        image.save(image_path)
        print(image_path)
        image_paths = list_images_in_folder(main_window.config["upload-path"])

        if len(image_paths) > 0:
            return render_template('homepage.html', image_paths=image_paths)
        
    else:
        return render_template('homepage.html', image_paths=None)

def get_latest_uploaded_file():
    files = os.listdir(main_window.config["upload-path"])
    if not files:
        return None
    latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join(main_window.config["upload-path"], x)))
    return os.path.join(main_window.config["upload-path"], latest_file)

@main_window.route("/processImage", methods=['POST'])
def image_process():
    selected_option = request.form.get("selected_option")
    print(f"Selected option: {selected_option}")

    image_paths = list_images_in_folder(main_window.config["upload-path"])

    processed_image_paths = []
    messages = []
    for image_path in image_paths:
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')

        try:
            print("sent raw img")
            response = requests.post("http://172.205.13.237:5001/processImage", json={
                "image_data": image_data,
                "selected_option": selected_option
            })

            response.raise_for_status()  # Raise an HTTPError for bad responses

            processed_image_data = response.json().get("processed_image_data")
            message = response.json().get("message")
            print("recived processed image")
            if message:
                messages.append(message)
            if processed_image_data:
                print("recived img not none")
                processed_image_path = save_processed_image(processed_image_data)
                processed_image_paths.append(processed_image_path)
            else:
                print(f"No processed image data received for {image_path}")

        except requests.exceptions.RequestException as e:
            print(f"Request to processing server failed for {image_path}: {e}")
            return render_template('homepage.html', error="Failed to process images")

    return render_template('homepage.html', processed_image_paths=processed_image_paths,messages=messages)

def save_processed_image(encoded_image):
    if not os.path.exists(main_window.config["download-path"]):
        os.makedirs(main_window.config["download-path"])

    image_data = base64.b64decode(encoded_image)
    unique_filename = f"processed_image_{uuid.uuid4().hex}.jpeg"
    processed_image_path = os.path.join(main_window.config["download-path"], unique_filename)
    with open(processed_image_path, "wb") as image_file:
        image_file.write(image_data)
    return processed_image_path

@main_window.route("/delete", methods=['POST'])
def deleteFiles():
    files = os.listdir(main_window.config["upload-path"])

    # Delete each file in the folder
    for file in files:
        file_path = os.path.join(main_window.config["upload-path"], file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    files = os.listdir(main_window.config["download-path"])
    # Delete each file in the folder
    for file in files:
        file_path = os.path.join(main_window.config["download-path"], file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    return redirect("/")

if __name__ == "__main__":
    main_window.run(debug=True, host='0.0.0.0', port=8080)

