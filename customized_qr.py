from PIL import Image, ImageColor
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.moduledrawers import (SquareModuleDrawer, 
                                               CircleModuleDrawer, 
                                               RoundedModuleDrawer, 
                                               VerticalBarsDrawer, 
                                               HorizontalBarsDrawer)

def generate_custom_qr(data, filename="custom_qr.png", color_fg="black", color_bg="white", 
                       module_style="circle", with_logo=False, logo_path=None):
    """
    Generates a custom QR Code with different design options.
    """
    # Convert color names to RGB inside the function
    color_fg = ImageColor.getrgb(color_fg)
    color_bg = ImageColor.getrgb(color_bg)

    # Set module drawer styles
    styles = {
        "square": SquareModuleDrawer(),
        "circle": CircleModuleDrawer(),
        "rounded": RoundedModuleDrawer(),
        "vertical_bars": VerticalBarsDrawer(),
        "horizontal_bars": HorizontalBarsDrawer()
    }
    module_drawer = styles.get(module_style, SquareModuleDrawer())

    # Create QR Code
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    # Generate QR code with colors and styles
    qr_img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=module_drawer,
        color_mask=SolidFillColorMask(front_color=color_fg, back_color=color_bg)
    )

    # Add logo if specified
    if with_logo and logo_path:
        try:
            logo = Image.open(logo_path)
            logo = logo.resize((qr_img.size[0] // 5, qr_img.size[1] // 5))  # Resize logo
            pos = ((qr_img.size[0] - logo.size[0]) // 2, (qr_img.size[1] - logo.size[1]) // 2)
            qr_img.paste(logo, pos, mask=logo.convert("RGBA"))  # Overlay logo
        except Exception as e:
            print(f"Error loading logo: {e}")

    # Save QR Code
    qr_img.save(filename)
    print(f"✅ QR Code saved as {filename}")

# Example usage
generate_custom_qr(
    data="https://www.youtube.com/@freecodecamp",
    filename="styled_qr.png",
    color_fg="blue",  # Now supports color names
    color_bg="white",
    module_style="rounded",
    with_logo=True,
    logo_path="logo.jpg"
)
