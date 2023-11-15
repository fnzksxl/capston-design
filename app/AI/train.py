from transformers import Seq2SeqTrainingArguments,Seq2SeqTrainer,\
                         DataCollatorForSeq2Seq

import app.AI.config as config
import app.AI.dataset as dataset


model_path=config.model_path
model_name=config.model_name
model=config.model
tokenizer=config.tokenizer

df = dataset.make_df(config.data_root)
train_dataset,test_dataset=dataset.make_dataset(df)


data_collator = DataCollatorForSeq2Seq(
    tokenizer=tokenizer, model=model
)

training_args = Seq2SeqTrainingArguments(
    output_dir=model_path, #The output directory
    overwrite_output_dir=True, #overwrite the content of the output directory
    num_train_epochs=config.epoch, # number of training epochs
    per_device_train_batch_size=config.train_batch_size, # batch size for training
    per_device_eval_batch_size=config.eval_batch_size,  # batch size for evaluation
    eval_steps=config.eval_steps, # Number of update steps between two evaluations.
    save_steps=config.save_steps, # after # steps model is saved 
    warmup_steps=config.warmup_steps,# number of warmup steps for learning rate scheduler
    prediction_loss_only=True,
    evaluation_strategy=config.strategy,
    save_total_limit=config.save_limits
    )

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

trainer.train()

try:
  trainer.save_model("./saved_model")
  print("Model saved successfully.")
except Exception as e:
  print(f"Failed to save model caused by {e}")  
