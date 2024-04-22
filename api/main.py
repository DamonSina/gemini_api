import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import json
import time

app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_credentials=True,
                   allow_origins=["*"],
                   allow_methods=["*"],
                   allow_headers=["*"]
                   )


@app.post("/gemini/chat", tags=["API"], summary="GEMINI")
def gemini_chat(data: dict):
    prompt = data.get('prompt')
    api_key= data.get('api_key')
    history=data.get('history')
    if history is None:
        history=[]
    try:
        # genai.configure(api_key=api_key,transport='rest')
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        chat = model.start_chat(history=history)
        response = chat.send_message(prompt)
        text=response.text
        response = {"content": text}
        return response
    except Exception as e:
        print("gemini_chat:",e)
        return None

@app.post("/gemini/chat_v2", tags=["API"], summary="GEMINI")
def gemini_chat_v2(data: dict):
    api_key= data.get('api_key')
    prompt_1 = data.get('prompt_1')
    prompt_2 = data.get('prompt_2')
    try:
        # genai.configure(api_key=api_key,transport='rest')
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        chat = model.start_chat(history=[])
        response_1 =chat.send_message(prompt_1)
        text_1=response_1.text

        response_2 =chat.send_message(prompt_2)
        text_2=response_2.text

        response = {"content_1": text_1,"content_2": text_2}
        return response
    except Exception as e:
        print("gemini_chat:",e)
        return None
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1",workers=1)