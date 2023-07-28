from transformers import AutoModelForSeq2SeqLM,AutoTokenizer
from tokenizers import Tokenizer

import os


# Model Config
model_path='./saved_model'
model_name = "gogamza/kobart-base-v2"

model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
if os.path.exists('./saved_model/pytorch_model.bin'):
  print("Use Customized Model")
  model = AutoModelForSeq2SeqLM.from_pretrained('./saved_model')
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Dataset
# Tsv file name must be data.tsv
data_root='./dataset'

# Training Arguments
epoch=3
train_batch_size=32
eval_batch_size=32
eval_steps=3000
save_steps=6000
warmup_steps=300
strategy="steps"
save_limits=3