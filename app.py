import streamlit as st
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import random

# Crear chatbots con diferentes personalidades
class ChatBotWithPersonality(ChatBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.personality = kwargs.get('personality', 'neutral')

    def get_response(self, *args, **kwargs):
        response = super().get_response(*args, **kwargs)
        return f"[{self.personality}] {response.text}"

# Configurar chatbots con personalidades
chatbots = {
    'Tigre': ChatBotWithPersonality('Tigre', personality='Feroz'),
    'Oso': ChatBotWithPersonality('Oso', personality='Calmado'),
    'Pingüino': ChatBotWithPersonality('Pingüino', personality='Bromista')
}

# Entrenadores de chatbot
def train_chatbot(chatbot):
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train('chatterbot.corpus.spanish')

# Entrenar todos los chatbots
for chatbot in chatbots.values():
    train_chatbot(chatbot)

# Interfaz de usuario en Streamlit
st.title('Chat con Animales')

# Selección del animal
animal = st.selectbox('Elige un animal para hablar:', ('Tigre', 'Oso', 'Pingüino'))

# Entrada del usuario
user_input = st.text_input(f'Escribe algo para el {animal}:')

if user_input:
    # Generar la respuesta del chatbot
    chatbot = chatbots[animal]
    response = chatbot.get_response(user_input)
    
    # Mostrar la respuesta en Streamlit
    st.write("Respuesta del chatbot:", response)
