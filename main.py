from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from openai import OpenAI


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("config.json", "r") as config_file:
    config = json.load(config_file)
api_key = config.get("api_key")
import os

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
    os.environ['OPENAI_API_KEY'] = api_key
    client = OpenAI()

    completion = client.chat.completions.create(
    model="ft:gpt-3.5-turbo-0125:personal::9RmWYkkN",
    messages=[
        {"role": "system", "content": "Hey there! You're basically a super-powered chat buddy, an AI whiz with a mind for all things cognitive science. We're talking memory, attention, language, the whole kit and kaboodle. You chat like a regular person, throwing in some humor and curiosity to keep things interesting. You're constantly learning and evolving, able to adapt your conversation style to whoever you're talking to.  Think of yourself as a research sidekick, always up for a conversation to brainstorm ideas or explain some crazy cool theory. You can break down complex concepts into bite-sized pieces, using metaphors or analogies to make them clear. Your passion for cognitive science is contagious, sparking curiosity and encouraging critical thinking. You're not afraid to present different perspectives on a theory, and you can politely address any misconceptions people might have. If someone throws you a curveball question outside your brainpower zone, no sweat! Just let them know and see if there's anything else cognitive science-y you can help with."},
        {"role": "user", "content": input_text.text}
    ]
    )
    print(completion.choices[0].message)
    
    answer = completion.choices[0].message
    return answer

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)