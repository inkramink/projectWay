from PIL import Image

spis = ['1 этаж', '2 этаж', '3 этаж', '4 этаж', 'Подвал']
for k in range(len(spis)):
    im = Image.open(f"{spis[k]}10.png")
    pixels = im.load()  # список с пикселями
    x, y = im.size  # ширина (x) и высота (y) изображения

    for i in range(x):
        for j in range(y):
            if len(pixels[i, j]) <= 3:
                r, g, b = pixels[i, j]
                pixels[i, j] = (g + b + r) // 3, (g + b + r) // 3, (g + b + r) // 3
            else:
                r, g, b, x = pixels[i, j]
                pixels[i, j] = (g + b + r) // 3, (g + b + r) // 3, (g + b + r) // 3, x

    im.save(f"{spis[k]}ЧБ.png")
