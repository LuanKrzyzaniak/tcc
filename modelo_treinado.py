import os
import torch
import pipeline as pipe
from transformers import T5Tokenizer, T5ForConditionalGeneration

PROMPT = """Extraia as informações relevantes desta Ata de Registro de Preços (ARP) e as estruture estritamente no formato JSON. 
As informações relevantes podem ser o número da ata, número do processo, data de emissão, identificação do fornecedor ou uma lista de múltiplos
produtos com seus preços, descrições e quantias e valor total.
Garanta que todos os campos vazios sejam preenchidos com os dados correspondentes encontrados no texto de entrada. 
O campo "Itens_Registrados" é uma lista JSON e pode conter um ou mais itens.
Para campos que se referem a quantidades, valores e percentuais, utilize o formato exato encontrado no documento.
Retorne somente o esquema JSON.
"""

MODEL_DIR = "output/t5_finetuned/checkpoint-1107"


def main():
    # Carregar modelo
    tokenizer = T5Tokenizer.from_pretrained(MODEL_DIR)
    model = T5ForConditionalGeneration.from_pretrained(MODEL_DIR).to("cuda")

    # Carregar PDFs
    folder = "input/teste"
    pdf_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".pdf")]

    # Tratar textos
    pdf_textos = pipe.tratar_arquivos(pdf_files)

    # Rodar inferência em cada arquivo
    for pdf, texto in pdf_textos.items():
        entrada = f"{PROMPT}\n\nDocumento:\n{texto}"
        inputs = tokenizer(entrada, return_tensors="pt", truncation=True, max_length=1024).to("cuda")

        outputs = model.generate(
            **inputs,
            max_length=512,
            num_beams=4,
            early_stopping=True
        )

        resultado = tokenizer.decode(outputs[0], skip_special_tokens=True)

        print(f"\n=== RESULTADO: {os.path.basename(pdf)} ===\n")
        print(resultado)
        print("\n-------------------------------------------\n")

if __name__ == "__main__":
    main()