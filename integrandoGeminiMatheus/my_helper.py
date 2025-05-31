import base64

# um código curto que permite abrir uma imagem, dado um caminho passado como parâmetro para a função encode_image().

def encode_image(image):
    with open(image, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

