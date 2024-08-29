import streamlit as st
from transformers import pipeline
import random
from gtts import gTTS
import io
import base64

# Contextos para cada animal
animal_contexts = {
    'Tigre': [
        "Como un tigre feroz, responde con confianza, autoridad y un toque desafiante.",
        "Eres un tigre dominante. Usa un tono fuerte y directo en tus respuestas.",
        "Como tigre valiente, tus respuestas deben ser incisivas y enérgicas."
    ],
    'Oso': [
        "Como un oso sabio, responde con calma, serenidad y reflexión.",
        "Eres un oso protector. Usa un tono tranquilo y reconfortante.",
        "Como oso sereno, tus respuestas deben ser pacientes y comprensivas."
    ],
    'Pingüino': [
        "Como un pingüino bromista, responde con humor, sarcasmo y ligereza.",
        "Eres un pingüino juguetón. Usa un tono alegre y divertido en tus respuestas.",
        "Como pingüino ingenioso, tus respuestas deben ser ingeniosas y divertidas."
    ]
}

# Función para configurar el contexto del chatbot según la personalidad del animal
def get_chatbot_prompt(animal, user_input):
    context = random.choice(animal_contexts[animal])
    prompt = f"{context}\nUsuario: {user_input}\nRespuesta:"
    return prompt

# Cargar el modelo de chatbot de Hugging Face
chatbot = pipeline("text-generation", model="microsoft/DialoGPT-medium")

# Función para generar una respuesta del chatbot
def generate_response(animal, user_input, chatbot):
    prompt = get_chatbot_prompt(animal, user_input)
    response = chatbot(prompt, max_length=100, temperature=0.9, num_return_sequences=1)
    return response[0]['generated_text'].strip()

# Función para convertir texto a voz
def text_to_speech(text):
    tts = gTTS(text=text, lang='es')
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes

# Interfaz de usuario en Streamlit
st.title('Chat con Animales')

# Selección del animal
animal = st.selectbox('Elige un animal para hablar:', ('Tigre', 'Oso', 'Pingüino'))

# Entrada del usuario
user_input = st.text_input(f'Escribe algo para el {animal}:')

if user_input:
    # Generar la respuesta personalizada del chatbot
    response = generate_response(animal, user_input, chatbot)
    
    # Mostrar la respuesta en Streamlit
    st.write("Respuesta del chatbot:", response)
    
    # Convertir la respuesta a audio
    audio_bytes = text_to_speech(response)
    
    # Mostrar el reproductor de audio en Streamlit
    st.audio(audio_bytes, format='audio/mp3')
