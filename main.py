import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# Verificar o ambiente 
def testa_gpu():
    print(torch.cuda.get_device_name(0)) 
    print(torch.cuda.is_available())

def main():
    testa_gpu()
    model_name = "google-t5/t5-base"
    
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name).to("cuda")

if __name__ == "__main__":
    main()