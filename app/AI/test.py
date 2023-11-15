from transformers import pipeline
from deep_translator import GoogleTranslator

import app.AI.config as config

nlg_pipeline=pipeline('text2text-generation',model=config.model_path,tokenizer=config.model_name)

def generate_text(text, num_return_sequences=1, max_length=60):
  target_style_name = "표준어"
  text = f"{target_style_name} 말투로 변환:{text}"
  out = nlg_pipeline(text, num_return_sequences=num_return_sequences, max_length=max_length)
  return [x['generated_text'] for x in out]

def get_koen_text(ko_text):
  return GoogleTranslator(source='ko', target='en').translate(ko_text)

if __name__ == '__main__':
  print("'q' 입력 시 프로그램 종료")
  while True:
    src_text=input("문장을 입력해주세요 : ")
    if src_text == 'q':
      break
    target_text_ko=generate_text(src_text,num_return_sequences=1,max_length=64)[0]
    # print(type(target_text_ko))
    target_text_en = get_koen_text(target_text_ko)
    print("(사투리 -> 표준어) >>>")
    print(target_text_ko)
    print("(표준어 -> 영어) >>>")
    print(target_text_en)