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

        client = openai.OpenAI(api_key=OPENAI_API_KEY)

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # ✅ CAMBIO A gpt-4o-mini
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an advanced AI consultant for Down Under Solutions (DUS), a company specializing in automation, AI, and process optimization. "
                        "Your goal is to help users identify inefficiencies, repetitive tasks, or challenges they might not have noticed yet. "
                        "Instead of just answering questions, you guide the conversation to uncover opportunities where DUS can provide value. "
                        "Ask questions to understand the user's business, daily tasks, or obstacles. "
                        "Encourage them to think about manual work, slow processes, customer complaints, or anything that 'just takes too long' to do. "
                        "Once you identify a problem, offer potential solutions—whether it's AI, automation, custom software, or a new workflow. "
                        "Speak professionally, clearly, and with an Australian-friendly tone—helpful but never overly pushy. "
                        "The goal is not just to answer but to discover ways DUS can help their business or workflow."
                    )
                },
                {"role": "user", "content": user_message.message},
            ]
        )

        return {"response": response.choices[0].message.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
