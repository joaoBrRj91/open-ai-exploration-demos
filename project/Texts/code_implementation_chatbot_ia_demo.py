"""
Wrapper mínimo — delega toda a lógica de mensagens para `ChatMessageManager`.
O arquivo agora só expõe `initialize_chat_with_model` para reutilização.
"""

from chat_message_manager import ChatMessageManager


def initialize_chat_with_model():
    """Inicia a interação com o chatbot (delegando ações ao ChatMessageManager)."""
    manager = ChatMessageManager()

    print('Welcome - This chatbot is a demo for interaction with IA. Enjoy 😁', manager.NEW_LINE_OUTPUT)

    user_name = input('What`s your name ? : ')

    print(f'{user_name} start your conversation with bot (Enter "exit" text finish and display interactions).', manager.NEW_LINE_OUTPUT)

    while True:
        print(manager.NEW_LINE_OUTPUT)
        message = input(f'({user_name}) - Enter your question to bot: ')
        if message != manager.EXIT_INTERACTION:
            manager.update_chat_messages(message, manager.USER_ROLE)
            manager.generate_model_api_response()
        else:
            manager.display_interaction_messages()
            manager.clear_chat_messages()
            break


if __name__ == '__main__':
    initialize_chat_with_model()
