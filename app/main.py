from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from telegram import Update, Bot
from app.api.v1.api import api_router
from app.core.config import settings
from app.services.chat_service import chat_service

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5000",
        "http://localhost:5001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Welcome to ChatBotVectorialDB API"}

# Initialize Telegram Bot
bot = Bot(token=settings.TELEGRAM_TOKEN)

@app.post("/telegram-webhook")
async def telegram_webhook(request: Request):
    """
    Endpoint for Telegram Webhook.
    Receives messages, searches Pinecone, and replies to the user.
    """
    try:
        data = await request.json()
        update = Update.de_json(data, bot)
        
        if update.message and update.message.text:
            chat_id = update.message.chat_id
            user_message = update.message.text
            
            # Use ChatService to get answer from Pinecone (dimension 2048)
            result = chat_service.get_answer_with_sources(user_message)
            answer = result["answer"]
            sources = result["sources"]
            
            # Format response with metadata (source filenames)
            response_text = f"{answer}\n\n"
            if sources:
                response_text += "Fuentes:\n"
                for source in sources:
                    response_text += f"- {source}\n"
            else:
                response_text += "No se encontraron fuentes específicas en los documentos."
            
            # Send message back to Telegram
            async with bot:
                await bot.send_message(chat_id=chat_id, text=response_text)
                
    except Exception as e:
        print(f"Error handling telegram webhook: {e}")
        # We return 200 to Telegram so it doesn't keep retrying the same faulty update
        return {"status": "error", "message": str(e)}
        
    return {"status": "ok"}
