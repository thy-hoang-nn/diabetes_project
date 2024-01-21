import uvicorn
from chat_api.classifier import ClassifierSwitcher


def run():
    uvicorn.run(
        "chat_api.app:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
    )


if __name__ == "__main__":
    run()
