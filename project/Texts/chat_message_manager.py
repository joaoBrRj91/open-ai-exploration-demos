"""
ChatMessageManager

Classe reutilizável para manipular mensagens de interação com o modelo OpenAI
- mantém o histórico de mensagens
- encapsula chamadas ao Responses API em streaming
- fornece métodos para atualizar, processar, exibir e limpar mensagens
"""

import os
from typing import List, Dict
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

# carrega variáveis de ambiente (tornando a classe reutilizável em outros scripts)
_ = load_dotenv(find_dotenv())


class ChatMessageManager:
    USER_ROLE = 'user'
    ASSISTANCE_ROLE = 'assistant'
    EXIT_INTERACTION = 'exit'
    NEW_LINE_OUTPUT = '\n'
    EVENT_STREAM_RESPONSE_CHUNK = 'response.output_text.delta'
    EVENT_STREAM_RESPONSE_COMPLETED = 'response.completed'

    def __init__(self):
        self.client = OpenAI()
        self.model = os.getenv('MODEL')
        self.max_output_tokens = int(os.getenv('MAX_TOKENS', '1000'))
        self.messages: List[Dict[str, str]] = []

    def update_chat_messages(self, message: str, role: str) -> None:
        """Append a formatted message to the internal history."""
        if role == self.USER_ROLE:
            interactive_output_text = f'Question User - {message}'
        else:
            interactive_output_text = f'Answer Bot - {message}'

        self.messages.append({'role': role, 'content': interactive_output_text})

    def process_stream_response(self, stream_manager) -> str:
            """Process a streaming response, print deltas and append final text to history."""
            print(self.NEW_LINE_OUTPUT)
            response_text = ''
            with stream_manager as stream:
                for event in stream:
                    if event.type == self.EVENT_STREAM_RESPONSE_CHUNK:
                        print(event.delta, end='')
                        response_text += event.delta
                    elif event.type == self.EVENT_STREAM_RESPONSE_COMPLETED:
                        print(self.NEW_LINE_OUTPUT)
                        break

            self.update_chat_messages(response_text, self.ASSISTANCE_ROLE)
            return response_text


    def generate_model_api_response(self):
        """Returns the streaming response manager from the Responses API."""
        response_stream = self.client.responses.stream(
            model=self.model,
            max_output_tokens=self.max_output_tokens,
            input=self.messages,
        )

        self.process_stream_response(response_stream)
        

    def display_interaction_messages(self) -> None:
        """Print stored conversation history."""
        print(self.NEW_LINE_OUTPUT)
        print('This is your history conversation with chatbot.')
        for message_interaction in self.messages:
            print(message_interaction)

    def clear_chat_messages(self) -> None:
        """Clear the in-memory message history."""
        self.messages.clear()
