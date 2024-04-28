from flask import Flask, render_template,request
import os
from worker_thread import uploadImage



main_window = Flask(__name__)
main_window.config["upload-path"]="static/uploadFolder"

@main_window.route("/")
def HomePage():
    return render_template("homepage.html")



@main_window.route("/addImage",methods=['POST'],)
def image_process():
    image=request.files["uploaded_image"]

    if image:
        image.save(os.path.join(main_window.config["upload-path"], image.filename))
        # Get the path of the saved image
        image_path = os.path.join(main_window.config["upload-path"], image.filename)
        print(image_path)
        return render_template('homepage.html', image_path=image_path)
    else:
        return render_template('homepage.html', image_path=None)



if __name__ == "__main__":
    main_window.run(debug=True,port=5000)

