from flask import Flask, render_template, request, send_file
import qrcode
import qrcode.image.styledpil
from qrcode.image.styles.moduledrawers import (
    SquareModuleDrawer, CircleModuleDrawer, RoundedModuleDrawer, GappedSquareModuleDrawer
)
from io import BytesIO
import os
from PIL import Image

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

    # QR Code Configuration
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Correct shape selection logic
    module_drawers = {
        "square": SquareModuleDrawer(),
        "dots": CircleModuleDrawer(),
        "rounded": RoundedModuleDrawer(),
        "gapped_square": GappedSquareModuleDrawer(),
    }

    module_drawer = module_drawers.get(shape, SquareModuleDrawer())  # Default to square if invalid

    # Generate QR Code with chosen style
    image = qr.make_image(fill_color=fg_color, back_color=bg_color, module_drawer=module_drawer)

    # Add Logo if provided
    if logo:
        logo_path = os.path.join(UPLOAD_FOLDER, logo.filename)
        logo.save(logo_path)
        logo_img = Image.open(logo_path)

        image = image.convert("RGBA")

        # Resize logo
        logo_size = (image.size[0] // 4, image.size[1] // 4)
        logo_img = logo_img.resize(logo_size)

        # Position logo at center
        pos = ((image.size[0] - logo_size[0]) // 2, (image.size[1] - logo_size[1]) // 2)
        image.paste(logo_img, pos, mask=logo_img)

    # Save QR Code as a file
    qr_io = BytesIO()
    image.save(qr_io, format='PNG')
    qr_io.seek(0)
    
    return send_file(qr_io, mimetype='image/png', as_attachment=True, download_name="qr_code.png")

if __name__ == '__main__':
    app.run(debug=True)
