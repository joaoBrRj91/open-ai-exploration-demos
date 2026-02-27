import base64
import os
from dotenv import load_dotenv,find_dotenv
from openai import OpenAI

client: OpenAI

def setup_program_vision_base64() -> str:
    _ = load_dotenv(find_dotenv())
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "assets/analise_furto_loja_vision.jpg")
    base64_image = encode_image(image_path)
    return base64_image

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def analizeImageBase64(image_base64: str):

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": "Atue como um especialista em segurança. \
                 Analise a imagem que é representada por um frame de vide \f Focando em detecção de furtos em tempo real e traga uma conclusao se há eminencia de furtos na iamgem"},
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{image_base64}",
                },
            ],
        }],
        )
    
    print(response.output_text)


if __name__ == '__main__':
    base64_image = setup_program_vision_base64()
    client = OpenAI()
    analizeImageBase64(base64_image)
