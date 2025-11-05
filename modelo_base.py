import json
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

jsonl_path = "output/dataset/253233.jsonl"

def main():
    # Carregando tokenizer e modelo
    model_name = "t5-base"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name).to("cuda")

    # Lendo arquivo
    with open(jsonl_path, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    primeira_linha = json.loads(linhas[0])
    entrada = primeira_linha["input"]

    # Tokenizando
    inputs = tokenizer(entrada, return_tensors="pt", truncation=True, max_length=1024).to("cuda")

    # Gerando saída
    outputs = model.generate(
        **inputs,
        max_length=512,
        num_beams=4,
        early_stopping=True
    )

    # Decodificando
    resultado = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print("\nResultado gerado pelo T5:\n")
    print(resultado)

if __name__ == "__main__":
    main()