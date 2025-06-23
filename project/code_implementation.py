"""
Import libs
"""
import os
from typing import List
from dotenv import load_dotenv,find_dotenv
from openai import OpenAI
from openai.types.responses import ResponseOutputMessage
from openai.types.responses import Response

# Class encapsulate response output message
class CustomResponseOutputMessage(ResponseOutputMessage):
    created_at: str
    message: str


output_compute_messages: List[CustomResponseOutputMessage] = []

def model_api_response_call(messages_input:list) -> Response:
    """
    Function to call the OpenAI API and get a response.
    """
    client = OpenAI()
    return client.responses.create(
        model=os.getenv("MODEL"),
        temperature=float(os.getenv("TEMPERATURE")),
        max_output_tokens=int(os.getenv("MAX_TOKENS")),
        input=messages_input
    )

def response_model_output_generated(response_model:Response) -> CustomResponseOutputMessage:
    """
    Function to convert the response output to a ResponseOutputMessage.
    """
    return CustomResponseOutputMessage(
        id=response_model.id,
        created_at=response_model.created_at,
        role=response_model.output[0].role,
        status=response_model.output[0].status,
        message=response_model.output_text
    )

def response_model_append_message(response_model:Response, chat_from_user:List[dict[str, str]]):
    """
    Function to append a message to the response model.
    """
    output_compute_messages.append(response_model_output_generated(response_model))


# Load envirement variables from .env
_ = load_dotenv(find_dotenv())


def print_messages_generated():
    # Print the current messages after processing the response
    for responses_message in output_compute_messages:
        print("\nResponse Process Data : ")
        print(f"message_id: {responses_message.id}")
        print(f"created_at: {responses_message.created_at}")
        print(f"role: {responses_message.role}")
        print(f"status: {responses_message.status}")
        print(f"message: {responses_message.message}")


# Logic for get message from console input user. This response need add in output_compute_messages if the response ia is success
messages_from_user = [{"role": "user",
                        "content": "Write a one-sentence bedtime story about a unicorn."}]

message_response_from_ia = model_api_response_call(messages_from_user)

response_model_append_message(message_response_from_ia, messages_from_user)

print_messages_generated()
