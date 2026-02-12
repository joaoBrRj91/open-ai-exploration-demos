"""
Import libs
"""
import os
import json
from dotenv import load_dotenv,find_dotenv
from openai import OpenAI
from openai.types.responses import Response

messages = [{"role": "user", "content": "What is the weather like in Rio de Janeiro today?"}]

tools = [{
    "type": "function",
    "name": "get_weather",
    "description": "Get current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City and country e.g. Rio de Janeiro, Brazil"
            }
        },
        "required": [
            "location"
        ],
        "additionalProperties": False
    }
}]

# Load envirement variables from .env
_ = load_dotenv(find_dotenv())

def get_weather(location:str):
    """
    Mock for get weather of the location - For final version connect and call api whether 
    """
    return f'{location} - 24°C (67.2°F).'

def call_model_api(mensages: list[dict[str, str]])-> Response:
    """
    Function to call model api
    """
    client = OpenAI()
    return client.responses.create(
        model=os.getenv("MODEL"),
        temperature=float(os.getenv("TEMPERATURE")),
        max_output_tokens=int(os.getenv("MAX_TOKENS")),
        input=mensages,
        tools=tools
    )

first_response = call_model_api(messages)

print(first_response.output)

for tool_call in first_response.output:
    messages.append(tool_call)
    args = json.loads(tool_call.arguments)
    result = get_weather(args['location'])
    messages.append({
    'type': 'function_call_output',
    'call_id': tool_call.call_id,
    'output': str(result)
    })

final_response = call_model_api(messages)

print(f'Final Answer - {final_response.output_text}')
