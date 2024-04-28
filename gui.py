from flask import Flask, render_template,request


main_window = Flask(__name__)

@main_window.route("/")
def HomePage():
    return render_template("homepage.html")



@main_window.route("/addImage",methods=['POST'],)
def image_process():
    image=request.files["uploaded_image"]




if __name__ == "__main__":
    main_window.run(debug=True,port=5000)

