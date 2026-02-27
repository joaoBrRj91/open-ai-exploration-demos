from dotenv import load_dotenv,find_dotenv
from openai import OpenAI

client: OpenAI

def analizeImage(image_url: str = '', image_base64: str = ''):

    if not image_url and not image_base64:
        print('Enter image url or image base 64 valid!')
        return

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": "O que tem na imagem?"},
                {
                    "type": "input_image",
                    "image_url": image_url,
                },
            ],
        }],
        )
    
    print(response.output_text)


if __name__ == '__main__':
    _ = load_dotenv(find_dotenv())
    client = OpenAI()
    analizeImage(image_url='https://api.nga.gov/iiif/a2e6da57-3cd1-4235-b20e-95dcaefed6c8/full/!800,800/0/default.jpg')
