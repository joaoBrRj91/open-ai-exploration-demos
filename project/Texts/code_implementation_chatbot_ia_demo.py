"""
Import libs
"""
import os
from dotenv import load_dotenv,find_dotenv
from openai import OpenAI

# Load envirement variables from .env
_ = load_dotenv(find_dotenv())

messages: list[dict] = []
client = OpenAI()

USER_ROLE = 'user'
ASSISTANCE_ROLE = 'assistant'
EXIT_INTERACTION = 'exit'
NEW_LINE_OUTPUT = '\n'
EVENT_STREAM_RESPONSE_CHUNK = 'response.output_text.delta'
EVENT_STREAM_RESPONSE_COMPLETED = 'response.completed'

def update_chat_messages(message:str, role:str):
    """
    Function to append message.
    """
    interactive_output_text: str
    if role == USER_ROLE:
        interactive_output_text = f'Question User - {message}'
    else:
        interactive_output_text = f'Answer Bot - {message}'

    messages.append({'role': role, 'content': interactive_output_text})


def generate_model_api_response():
    """
    Function to call the OpenAI API.
    """
    return client.responses.stream(
        model=os.getenv("MODEL"),
        max_output_tokens=int(os.getenv("MAX_TOKENS")),
        input=messages
    )


def process_stream_response(stream_manager):
    """
    Function to process stream response and append in messages
    """
    print(NEW_LINE_OUTPUT)
    response_text = ''
    with stream_manager as stream:
        for event in stream:
            if event.type == EVENT_STREAM_RESPONSE_CHUNK:
                print(event.delta, end= '')
                response_text += event.delta
            elif event.type == EVENT_STREAM_RESPONSE_COMPLETED:
                print(NEW_LINE_OUTPUT)
                break

    update_chat_messages(response_text, ASSISTANCE_ROLE)


def display_interaction_messages():
    """
    Function to display interaction messages
    """
    print(NEW_LINE_OUTPUT)
    print('This is your history conversation with chatbot.')
    for message_interaction in messages:
        print(message_interaction)

def initialize_chat_with_model():
    """
    Function initialize chat.
    """
    print('Welcome - This chatbot is a demo for interaction with IA. Enjoy 😁', NEW_LINE_OUTPUT)

    user_name = input('What`s your name ? : ')

    print(f'{user_name} start your conversation with bot (Enter "exit" text finish and display interactions).', NEW_LINE_OUTPUT)

    while True:
        print(NEW_LINE_OUTPUT)
        message = input(f'({user_name}) - Enter your question to bot: ')
        if message != EXIT_INTERACTION:
            update_chat_messages(message,USER_ROLE)
            process_stream_response(generate_model_api_response())
        else:
            display_interaction_messages()
            clear_chat_messages()
            break


def clear_chat_messages():
    """
    Function to delete messages.
    """
    messages.clear()


if __name__ == '__main__':
    initialize_chat_with_model()
