from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Cargar variables de entorno
load_dotenv()

# Inicializar la API
app = FastAPI()

# Configurar CORS para permitir peticiones desde el frontend en Hostinger
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes especificar el dominio de Hostinger en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Clave API de OpenAI desde el archivo .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Validación de mensajes del usuario
class UserMessage(BaseModel):
    message: str

# Ruta principal de prueba
@app.get("/")
def read_root():
    return {"message": "Chatbot API is running 🚀"}

# Ruta para procesar mensajes del chatbot
@app.post("/chat")
async def chat_with_agent(user_message: UserMessage):
    try:
        if not OPENAI_API_KEY:
            raise HTTPException(status_code=500, detail="OpenAI API key not found.")

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un asistente australiano amigable, relajado y profesional. Responde con humor ligero y fomenta la conversación natural."},
                {"role": "user", "content": user_message.message},
            ]
        )

        return {"response": response["choices"][0]["message"]["content"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
