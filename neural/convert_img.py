from sys import argv
from PIL import Image
import numpy as np
import csv

try:
    csvpath = argv[1]
except:
    exit(1)

with open(csvpath) as fp:
    reader = csv.reader(fp)

    for label, *pxs in reader:
        pxs = np.array(pxs).astype(np.float)
        break

img = Image.new('L', (28, 28))
for j, pixel in enumerate(pxs):
    xy = j % 28, j // 28
    img.putpixel(xy, int(pixel))
img.save(f'{csvpath[0:-4]}.png')