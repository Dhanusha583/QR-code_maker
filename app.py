from flask import Flask, render_template, request, send_from_directory, jsonify
import qrcode
import qrcode.image.styledpil
from qrcode.image.styles.moduledrawers import (
    SquareModuleDrawer, CircleModuleDrawer, RoundedModuleDrawer, GappedSquareModuleDrawer
)
import os
from PIL import Image

app = Flask(__name__)

# Ensure directories exist
UPLOAD_FOLDER = "static/uploads"
QR_FOLDER = "static/qrcodes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.form.get('data')
    fg_color = request.form.get('fg_color', '#000000')
    bg_color = request.form.get('bg_color', '#FFFFFF')
    shape = request.form.get('shape', 'square')
    logo = request.files.get('logo')

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    module_drawers = {
        "square": SquareModuleDrawer(),
        "dots": CircleModuleDrawer(),
        "rounded": RoundedModuleDrawer(),
        "gapped_square": GappedSquareModuleDrawer(),
    }
    
    module_drawer = module_drawers.get(shape, SquareModuleDrawer())

    image = qr.make_image(fill_color=fg_color, back_color=bg_color, module_drawer=module_drawer)

    # If logo is uploaded, add it to the QR code
    if logo:
        logo_path = os.path.join(UPLOAD_FOLDER, logo.filename)
        logo.save(logo_path)
        logo_img = Image.open(logo_path).convert("RGBA")

        logo_size = (image.size[0] // 4, image.size[1] // 4)
        logo_img = logo_img.resize(logo_size)

        pos = ((image.size[0] - logo_size[0]) // 2, (image.size[1] - logo_size[1]) // 2)
        image.paste(logo_img, pos, mask=logo_img)

    # Save the QR code
    qr_filename = "qr_code.png"
    qr_path = os.path.join(QR_FOLDER, qr_filename)
    image.save(qr_path, format='PNG')

    return jsonify({'filename': qr_filename})

@app.route('/qrcode/<filename>')
def get_qrcode(filename):
    return send_from_directory(QR_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)  