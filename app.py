from flask import Flask, render_template, request, send_file
from PIL import Image
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    files = request.files.getlist('images')
    image_list = []

    for file in files:
        if file.filename != '':
            img = Image.open(file).convert('RGB')
            image_list.append(img)

    if not image_list:
        return "No images uploaded", 400

    output_filename = f"{uuid.uuid4()}.pdf"
    output_path = os.path.join(UPLOAD_FOLDER, output_filename)
    image_list[0].save(output_path, save_all=True, append_images=image_list[1:])

    return send_file(output_path, as_attachment=True)

# Required for Render: run on 0.0.0.0 and get port from env
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
