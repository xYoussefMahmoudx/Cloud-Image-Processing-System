import base64

from flask import Flask, render_template,request
import os

from matplotlib import pyplot as plt
from worker_thread import processImage
import cv2
import shutil
# import rpyc

# conn = rpyc.connect("localhost", 18861)  # Connect to the RPyC server running on localhost




main_window = Flask(__name__)
main_window.config["upload-path"]="static/uploadFolder"
main_window.config["download-path"]="static/downloadFolder"


@main_window.route("/")
def HomePage():
    return render_template("homepage.html")



@main_window.route("/addImage",methods=['POST'],)
def image_upload():
    image=request.files["uploaded_image"]

    if image:
        image.save(os.path.join(main_window.config["upload-path"], image.filename))
        # Get the path of the saved image
        image_path = os.path.join(main_window.config["upload-path"], image.filename)
        print(image_path)
        return render_template('homepage.html', image_path=image_path)
    else:
        return render_template('homepage.html', image_path=None)


def get_latest_uploaded_file():
    # Get a list of all files in the upload folder
    files = os.listdir(main_window.config["upload-path"])

    if not files:
        # Return None if the upload folder is empty
        return None

    # Filter out directories and get the most recently modified file
    latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join(main_window.config["upload-path"], x)))

    # Return the path to the latest file
    return os.path.join(main_window.config["upload-path"], latest_file)


@main_window.route("/processImage",methods=['POST'],)
def image_process():
    selected_option = request.form.get("selected_option")
    print(selected_option)
    image_path = get_latest_uploaded_file()
    

    image_path= shutil.copy(image_path,"static\downloadFolder")
    result=cv2.imread(image_path, cv2.IMREAD_COLOR )


    result = processImage(result ,selected_option)
    # result = cv2.Canny(image_path, 100, 200)
    # cv2.imwrite(image_path, result)
    succ,encoded_image = cv2.imencode('.jpeg', result)
    
    print(encoded_image)

    
    encoded_image = base64.b64encode(encoded_image).decode('utf-8')
    return render_template('homepage.html', encoded_image=encoded_image)
    # return render_template('homepage.html', image_path)





if __name__ == "__main__":
    main_window.run(debug=True, host='192.168.1.6', port=5000)


