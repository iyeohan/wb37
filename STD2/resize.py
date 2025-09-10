from PIL import Image

image=Image.open('resize.jpeg')

quality=100

image.save('resize.jpeg', format='JPEG', quality=quality)