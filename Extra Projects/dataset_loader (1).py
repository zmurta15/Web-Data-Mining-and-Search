import torch
from torch.utils.data import Dataset

import json
import os
import collections

class IntentDataset(Dataset):
    def __init__(self, loc, tokenizer, mode, toy=False, max_length=180):
        '''
        You can fine-tune a model with your own data!! Feel free to create (or collect!) your own utterances
            and give it a shot!        

        loc: relative directory where the data lies
        tokenizer: huggingface tokenizer to preprocess utterances
        mode: one of train, val, test (should match the respective *.json files)
        toy: load a very small amount of data (for debugging purposes)
        max_length:max length of tokenized input
        '''
        self.tokenizer = tokenizer
        self.mode = mode
        self.max_length=max_length
        
        with open(os.path.join(loc, 'all_intents.json'), 'r') as all_intents_json:
            self.all_intents = json.load(all_intents_json) # contains the written out names of intents. also implicitly
            # defines how many intents your chatbot's neural intent detection will support
        
        with open(os.path.join(loc, mode + '.json'), 'r') as json_data:
            self.all_data = json.load(json_data)
            
        if toy:
            self.all_data = self.all_data[:10]
            
        print(f"Loaded Intent detection dataset. {len(self.all_data)} examples. ({mode}). {'Toy example' if toy else ''}")
        
    def __len__(self): # torch Datasets need a __len__ method and __getitem__, with len as the total amount of examples...
        return len(self.all_data)
    
    def __getitem__(self, index): #... and __getitem__ as a way to get an example given an index >= 0 and < __len__ 
        data_item = self.all_data[index]
        
        if len(data_item) == 3:
            tokenized_input = self.tokenizer(data_item[0], data_item[1], return_tensors='pt', padding='max_length', truncation=True, max_length=self.max_length)
        else:
            tokenized_input = self.tokenizer(data_item[0], return_tensors='pt', padding='max_length', truncation=True, max_length=self.max_length)

        output_item = {
            'input_ids': tokenized_input['input_ids'].squeeze(0),
            'attention_mask': tokenized_input['attention_mask'].squeeze(0),
            'label': torch.tensor(self.all_intents.index(data_item[-1]))
        }
        if 'token_type_ids' in tokenized_input:
            output_item['token_type_ids'] = tokenized_input['token_type_ids'].squeeze(0),
        return output_item
        
        
