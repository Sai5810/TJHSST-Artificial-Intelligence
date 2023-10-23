import requests
import numpy as np
from PIL import Image



img = Image.open(requests.get("https://www.freepnglogos.com/uploads/dog-png/bow-wow-gourmet-dog-treats-are-healthy"
                              "-natural-low-4.png", stream=True).raw)
print(img.size)
img.convert('RGBA').rotate(45).show()


