from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from chat_api.routes.chat import router as ChatRouter
from chat_api.classifier import ClassifierSwitcher




app = FastAPI(title = "Pima diabetes API", docs_url = "/docs", version="0.1.0")

app.include_router(ChatRouter, tags=["Chat"], prefix="/chat")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Pima Diabetes API v2"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "PUT", "DELETE", "OPTION", "GET"],
    allow_headers=["*"],
)





