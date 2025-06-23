"""
Import libs
"""
import os
from dotenv import load_dotenv,find_dotenv
from openai import OpenAI
from openai.types.responses import ResponseOutputMessage
from openai.types.responses import Response


messages = [{"role": "user", "content": "Write a one-sentence bedtime story about a unicorn."}]

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


# Carregar as variáveis de ambiente do arquivo .env
_ = load_dotenv(find_dotenv())

client = OpenAI()

response = client.responses.create(
    model=os.getenv("MODEL"),
    temperature= os.getenv("TEMPERATURE"),
    max_output_tokens= os.getenv("MAX_TOKENS"),
    input=messages
)

# Print the response object
print(response_model_output_generated(response))
