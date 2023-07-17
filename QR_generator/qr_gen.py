import qrcode
from PIL import Image

CODE_PATH = "/Users/stefantraianiancu/Desktop/projects/QR_generator/codes"

# set a desired website 
# data = "https://github.com/StefanIancu/projects"

# generate qr
qr = qrcode.QRCode(version=1, box_size=10, border=5)
# qr.add_data(data)
# qr.make(fit=True)

# create an image from the qr
# image = qr.make_image(fill="black", back_color="white")

# save the image
# image.save("/Users/stefantraianiancu/Desktop/projects/QR_generator/qr_code.png")
# Image.open("/Users/stefantraianiancu/Desktop/projects/QR_generator/qr_code.png")

def make_qr():
    while True:
        link = input("Please enter your link: ")
        if not link.startswith("www."):
            print("Please use correct a correct format like -> www.link.com")
        else:
            qr.add_data(link)
            qr.make(fit=True)
            image = qr.make_image(fill = "black", back_color = "white")
            image.save(f"{CODE_PATH}/{link.split('.')[1]}.png")
            print("QR Code successfully generated.")
            break

make_qr()