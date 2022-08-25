from PIL import Image
import time

image1 = Image.open('.\\data\\dummy.png')
im1 = image1.convert('RGB')
im1.save(f'.\\{time.strftime("%Y%m%d",time.localtime())}.pdf')