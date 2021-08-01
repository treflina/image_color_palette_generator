from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory
import os
from werkzeug.utils import secure_filename
from colorthief import ColorThief


UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])



app = Flask(__name__)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024


def rgb2hex(triplet):
    return f"#{''.join(f'{hex(c)[2:].upper():0>2}' for c in triplet)}"


exemplary_palette = []
img = ColorThief(f"static/images/obraz.jpg")
palette = img.get_palette(color_count=11, quality=10)
for x in palette:
    color = rgb2hex(x)
    exemplary_palette.append(color)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return redirect(url_for("palette", filename=filename))
    return render_template("index.html", exemplary_palette=exemplary_palette)

@app.route('/display/<filename>')
def display_image(filename=""):
	#print('display_image filename: ' + filename)
	return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route("/palette/<filename>")
def palette(filename):
    colors=[]
    img = ColorThief(f"static/images/{filename}")
    palette = img.get_palette(color_count=11, quality=30)
    for x in palette:
        color=rgb2hex(x)
        colors.append(color)
    return render_template("index.html", filename=filename, palette=palette, colors=colors)

if __name__ == '__main__':
    app.run()


# @app.route('/read_file', methods=['GET'])
# def read_uploaded_file():
#     filename = secure_filename(request.args.get('filename'))
#     try:
#         if filename and allowed_filename(filename):
#             with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as f:
#                 return f.read()
#     except IOError:
#         pass
#     return "Unable to read file"

