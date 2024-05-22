from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()
# Define input data model
class InputText(BaseModel):
    text: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.post("/chat")
def chat_with_bot(input_text: InputText):
    return {"your message": input_text.text}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)