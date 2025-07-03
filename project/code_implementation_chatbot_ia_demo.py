"""
Import libs
"""
import os
from dotenv import load_dotenv,find_dotenv
from openai import OpenAI
from openai.types.responses import Response

# Load envirement variables from .env
_ = load_dotenv(find_dotenv())

mensages = [{}]
USER_ROLE = 'User'
ASSISTANCE_ROLE = 'Assistance'

def update_chat_messages(message:str, role:str):
    """
    Function to append message.
    """
    print(f'{role}: {message}',end='')
    mensages.append({'role': role, 'content': message})


def generate_model_api_response(messages_input:list[dict],
                                 is_stream_response:bool = True) -> Response:
    """
    Function to call the OpenAI API.
    """
    client = OpenAI()
    response = client.responses.create(
        model=os.getenv("MODEL"),
        temperature=float(os.getenv("TEMPERATURE")),
        max_output_tokens=int(os.getenv("MAX_TOKENS")),
        input=messages_input,
        stream=is_stream_response
    )

    return response


def process_stream_response(stream_response:Response):
    """
    Function to process stream response and append in messages
    """
    for stream_event in stream_response:
        print(stream_event, end='')


def initialize_chat_with_model():
    """
    Function initialize chat.
    """
    print('Welcome - This chatbot is a demo for interaction with IA. Enjoy 😁')
    user_name = input('What`s your name ? : ')
    print(f'{user_name} start your conversation with bot.')
    while True:
        message = input(f'User({user_name}): ')
        update_chat_messages(message,USER_ROLE)
        break


if __name__ == '__main__':
    initialize_chat_with_model()