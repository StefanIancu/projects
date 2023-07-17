import qrcode
from PIL import Image

# set a desired website 
data = "https://github.com/StefanIancu/projects/tree/main"

# generate qr
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(data)
qr.make(fit=True)

# create an image from the qr
image = qr.make_image(fill="black", back_color="white")

# save the image
image.save("/Users/stefantraianiancu/Desktop/projects/QR_generator/qr_code.png")
Image.open("/Users/stefantraianiancu/Desktop/projects/QR_generator/qr_code.png")