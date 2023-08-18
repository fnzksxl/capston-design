from transformers import pipeline
import app.config as config
from deep_translator import GoogleTranslator

nlg_pipeline=pipeline('text2text-generation',model=config.model_path,tokenizer=config.model_name)

def generate_text(pipe, text, num_return_sequences=5, max_length=60):
  target_style_name = "표준어"
  text = f"{target_style_name} 말투로 변환:{text}"
  out = pipe(text, num_return_sequences=num_return_sequences, max_length=max_length)
  return [x['generated_text'] for x in out]

print("'q' 입력 시 프로그램 종료")
while True:
  src_text=input("문장을 입력해주세요 : ")
  if src_text == 'q':
    break
  target_text_ko=generate_text(nlg_pipeline,src_text,num_return_sequences=1,max_length=64)[0]
  # print(type(target_text_ko))
  target_text_en = GoogleTranslator(source='ko',target='en').translate(target_text_ko)
  print("(사투리 -> 표준어) >>>")
  print(target_text_ko)
  print("(표준어 -> 영어) >>>")
  print(target_text_en)