"""
Import libs
"""
import os
from dotenv import load_dotenv,find_dotenv
from openai import OpenAI
from openai.types.responses import ResponseOutputMessage
from openai.types.responses import Response


messages = [{"role": "user", "content": "Write a one-sentence bedtime story about a unicorn."}]


# Function to call the OpenAI API and get a response
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

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.
def response_model_output_generated(response_model:Response) -> ResponseOutputMessage:
    """
    Function to convert the response output to a ResponseOutputMessage.
    """
    return ResponseOutputMessage(
        message_id=response_model.id,
        created_at=response_model.created_at,
        role=response_model.output[0].role,
        status=response_model.output[0].status,
        message=response_model.output[0].message
    )

def response_model_append_message(response_model:Response) -> Response:
    """
    Function to append a message to the response model.
    """
    response_model.output.append(response_model_output_generated(response_model))
    return response_model


# Carregar as variáveis de ambiente do arquivo .env
_ = load_dotenv(find_dotenv())

# Logic for get message from console input user

response_model_append_message(model_api_response_call(messages))

# Print the current messages after processing the response
print(messages)
