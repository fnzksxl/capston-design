from torch.utils.data import Dataset
from tokenizers import Tokenizer

import pandas as pd

import app.AI.config as config

tokenizer=config.tokenizer
class TextStyleTransferDataset(Dataset):
    def __init__(self, df,tokenizer):
      self.df = df
      self.tokenizer = tokenizer
    
    def __len__(self):
        return len(self.df)

    def __getitem__(self, index):
        row=self.df.iloc[index]
        text1=row[0]
        text2=row[1]
        target_style_name = '표준어'

        encoder_text = f"{target_style_name} 말투로 변환:{text1}"
        decoder_text = f"{text2}{self.tokenizer.eos_token}"
        model_inputs = self.tokenizer(encoder_text, max_length=64, truncation=True)

        with self.tokenizer.as_target_tokenizer():
          labels = tokenizer(decoder_text, max_length=64, truncation=True)
        model_inputs['labels'] = labels['input_ids']
        del model_inputs['token_type_ids']

        return model_inputs
    
def make_df(data_root):
    df = pd.read_csv(f'{data_root}/data.tsv',sep='\t')
    idx=int(len(df)*0.1)
    df_train,df_test = df[idx:],df[:idx]

    print(f'Train DataFrame length : {len(df_train)},Test DataFrame length : {len(df_test)}')
    return df_train,df_test

def make_dataset(df):
    df_train,df_test = df

    train_dataset = TextStyleTransferDataset(df_train,tokenizer)
    test_dataset = TextStyleTransferDataset(df_test,tokenizer)

    return train_dataset,test_dataset