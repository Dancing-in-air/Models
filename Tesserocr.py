import tesserocr
from PIL import Image

image = Image.open("/home/tarena/图片/Code2.jpg")
# 展示图片
image.show()
# 自定义二值化
image = image.convert("L")
# 展示转换成"L"模式的图片
image.show()
# 设置阀值
threshold = 80
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
image = image.point(table, "1")
# 展示转换成"1"模式的图片
image.show()
# 提取图片中的验证码
result = tesserocr.image_to_text(image)
print(result)
