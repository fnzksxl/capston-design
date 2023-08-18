import json
import io
import app.config as config

from pydantic import BaseModel
from deep_translator import GoogleTranslator

from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

class inputText(BaseModel):
   text: str = None

# Initializing
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"),name="static")

def generate_text(pipe, text, num_return_sequences=5, max_length=60):
  target_style_name = "표준어"
  text = f"{target_style_name} 말투로 변환:{text}"
  out = pipe(text, num_return_sequences=num_return_sequences, max_length=max_length)
  return [x['generated_text'] for x in out]

def get_koen_text(generated):
  target_text_ko = generated[0]
  target_text_en = GoogleTranslator(source='ko',target='en').translate(target_text_ko)
  return target_text_ko,target_text_en


@app.get('/', response_class=HTMLResponse)
def type_text(request: Request):
  return templates.TemplateResponse("input.html",{"request":request})

@app.post('/result', response_class=HTMLResponse)
async def show_result(request: Request):
    form_data = await request.form()
    input = form_data['input']
    if input == '':
      raise HTTPException(status_code=404, detail='번역할 사투리를 입력하고 번역 버튼을 클릭해주세요!')
    target_text_ko = generate_text(config._pipeline,input,num_return_sequences=1,max_length=64)[0]
    target_text_en = GoogleTranslator(source='ko',target='en').translate(target_text_ko)
    return templates.TemplateResponse("translate.html",{"request" : request, "text_kor" : target_text_ko, "text_eng" : target_text_en})
