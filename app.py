import json
import io
import config

from transformers import pipeline
from deep_translator import GoogleTranslator
from flask import Flask,render_template,request

# Initializing
app = Flask(__name__)
d2s_pipeline=pipeline('text2text-generation',model=config.model_path,tokenizer=config.model_name)

def generate_text(pipe, text, num_return_sequences=5, max_length=60):
  target_style_name = "표준어"
  text = f"{target_style_name} 말투로 변환:{text}"
  out = pipe(text, num_return_sequences=num_return_sequences, max_length=max_length)
  return [x['generated_text'] for x in out]

def get_koen_text(generated):
  target_text_ko = generated[0]
  target_text_en = GoogleTranslator(source='ko',target='en').translate(target_text_ko)
  return target_text_ko,target_text_en

@app.route('/',methods=('GET','POST'))
def type_text():
  if request.method == 'GET':  
    return render_template('./input.html')
  elif request.method == 'POST':
    input_text = request.form['input']
    target_text_ko = generate_text(d2s_pipeline,input_text,num_return_sequences=1,max_length=64)[0]
    target_text_en = GoogleTranslator(source='ko',target='en').translate(target_text_ko)
    return render_template('./translate.html',text_kor=target_text_ko,text_eng=target_text_en)

if __name__ == "__main__":
  app.run(debug=True)