from PIL import Image as img
import requests
from io import BytesIO
import tempfile
import pathlib

path = pathlib.Path(r"C:\Users\ryanl\temp")


r = requests.get('https://media.valorant-api.com/weaponskins/30388628-42f0-606c-82c0-73ad43de997f/displayicon.png')
imgs = img.open(BytesIO(r.content))


for item in items:
    img.SAVE(skinsfolder, 'JPEG')
    skinsfolder2.seek(0)
    skinsfolder2.read()