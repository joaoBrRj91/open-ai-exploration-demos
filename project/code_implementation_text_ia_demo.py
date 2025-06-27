"""
Import libs
"""
import os
from typing import List
from dotenv import load_dotenv,find_dotenv
from openai import OpenAI
from openai.types.responses import ResponseOutputMessage
from openai.types.responses import Response

class CustomResponseOutputMessage(ResponseOutputMessage):
    """
    Class encapsulate response output message.
    """
    created_at: str
    message: str


output_compute_messages: List[CustomResponseOutputMessage] = []

def model_api_response_call(messages_input:list, stream_response:bool = False) -> Response:
    """
    Function to call the OpenAI API.
    """
    client = OpenAI()
    response = client.responses.create(
        model=os.getenv("MODEL"),
        temperature=float(os.getenv("TEMPERATURE")),
        max_output_tokens=int(os.getenv("MAX_TOKENS")),
        input=messages_input,
        stream=stream_response
    )

    return response


def create_custom_output_response(id_:str,
                                created_at:str,
                                role:str,
                                status:str,
                                message:str) -> CustomResponseOutputMessage:
    """
    Function to create the response output
    """
    return CustomResponseOutputMessage(
        id=id_,
        created_at=created_at,
        role=role,
        status=status,
        message=message
    )

def append_response_model_message(response_model:Response):
    """
    Function to append a message to the response model.
    """
    data = response_model.model_dump()
    id_, created_at, output = (data['id'], data['created_at'], data['output'])

    output_compute_messages.append(
        create_custom_output_response(id_,created_at,output[0].role,
                                       output[0].status, output[0].output_text))


# Load envirement variables from .env
_ = load_dotenv(find_dotenv())


def print_messages_generated():
    """
    Function to append a message to the response model.
    """
    for responses_message in output_compute_messages:
        print("\nResponse Process Data : ")
        print(f"message_id: {responses_message.id}")
        print(f"created_at: {responses_message.created_at}")
        print(f"role: {responses_message.role}")
        print(f"status: {responses_message.status}")
        print(f"message: {responses_message.message}")


#TODO - Improviment code
# Logic for get message from console input user.
# This response need add in output_compute_messages with status in progress
# and complete if the response ia is success or imcomplete in case failed.
# In case sucess or failed
# Find last message of user and change status for correcty
# Choice from user if is stream data or not
messages_from_user = [{"role": "user",
                        "content": "Write a one-sentence bedtime story about a unicorn."}]

#From User
isStreamProcessing = False

message_response_from_ia = model_api_response_call(messages_from_user,isStreamProcessing)

if isStreamProcessing:
   #TODO : In final version is not iteration here but call
   # a method called processed stream message
   # And in the final loop event is add a new object inCustomResponseOutputMessage
    for stream_event in message_response_from_ia:
        print(stream_event, end='')

else:
    append_response_model_message(message_response_from_ia)

    print_messages_generated()
