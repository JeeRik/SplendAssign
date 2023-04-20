import io
from pathlib import Path

import cairo
import poppler
from PIL import Image

filepath = Path('test.pdf')
document = poppler.load_from_file(filepath)

renderer = poppler.PageRenderer()

# Render first page and convert to image buffer
page = document.create_page(0)
image = renderer.render_page(page, xres=72, yres=72)
buf = io.BytesIO(image.data).getbuffer()

if False: # for debugging
    pil_img = Image.frombytes('RGBA', (image.width, image.height),
                              image.data, 'raw', str(image.format))
    pil_img.save('test.png')

# Use page dimensions to create cairo surface
rect = page.page_rect()
width = int(rect.width)
height = int(rect.height)
#print(f'bytes used per pixel: {len(buf)/(width*height)}')

surface = cairo.ImageSurface.create_for_data(buf, cairo.FORMAT_ARGB32, width, height)