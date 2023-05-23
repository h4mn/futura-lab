# pip install pillow potrace

import potrace
import numpy as np
from PIL import Image

def jpg_to_svg(input_path, output_path, threshold=128):
    # Carregar imagem JPG e converter para escala de cinza
    image = Image.open(input_path).convert("L")
    
    # Binarizar a imagem com base no limite (threshold)
    image = image.point(lambda x: 0 if x < threshold else 255)
    
    # Converter a imagem em um array numpy e criar um bitmap potrace
    bitmap = potrace.Bitmap(np.array(image) == 0)
    
    # Criar um path com base no bitmap
    path = potrace.Path(bitmap)
    
    # Escrever o arquivo SVG
    with open(output_path, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<svg xmlns="http://www.w3.org/2000/svg" width="{}" height="{}">\n'.format(*image.size))
        f.write('<g transform="scale(1,-1) translate(0,-{})" fill="black">\n'.format(image.size[1]))
        for curve in path.to_curves():
            f.write('<path d="{}"/>\n'.format(curve.to_svg()))
        f.write('</g>\n')
        f.write('</svg>\n')

# Exemplo de uso
input_path = "input.jpg"
output_path = "output.svg"
jpg_to_svg(input_path, output_path)
