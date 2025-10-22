import json
import os
import fitz # PyMuPDF
import re

import utils as ut

PROMPT = """Extraia o conteúdo da Ata de Registro de Preços (ARP) e estruture-o estritamente no formato JSON fornecido abaixo. 
Garanta que todos os campos vazios sejam preenchidos com os dados correspondentes encontrados no texto de entrada. 
O campo "Itens_Registrados" é uma lista JSON e pode conter um ou mais itens, e todo item deve conter todos os campos do modelo fornecido.
Para campos que se referem a quantidades, valores e percentuais, utilize o formato exato encontrado no documento.

{
  "Documento": {
    "Numero_ARP": "",
    "Numero_Processo": ""
  },
  "Orgao_Gerenciador": {
    "Razao_Social": "",
    "CNPJ": "",
    "UG": "",
    "Endereco": "",
    "Representantes_Legais": [
      {"Cargo": "", "Nome": "", "Matricula": ""},
      {"Cargo": "", "Nome": "", "Matricula": ""}
    ]
  },
  "Fornecedor": {
    "Razao_Social": "",
    "CNPJ": "",
    "Endereco": "",
    "Telefone": "",
    "Email": "",
    "Representante_Legal": ""
  },
  "Itens_Registrados": [
    {
      "Item_TR": "",
      "Descricao_Especificacao": "",
      "Marca_Modelo": "",
      "Codigo": "",
      "Unidade_Medida": "",
      "Quantidade_Registrada": "",
      "Valor_Unitario": "",
      "Valor_Total_Item": ""
    }
  ],
  "Valor_Total": ""
}
"""

def carregar_pdf(folder):
    pdf_files = [folder + "/" + f for f in os.listdir(folder) if f.endswith(".pdf")]
    pdf_files = filtrar_duplicatas(pdf_files)
    pdf_files = filtrar_imagens(pdf_files)

    print("Número de arquivos PDFs carregados: ", str(len(pdf_files)))
    return pdf_files

def filtrar_duplicatas(pdf_files): # depreciated
    duplicates = []
    filtered = []

    for pdf in pdf_files:
        normalized = ut.normalizar_nome(pdf)
        if normalized == pdf:
            filtered.append(pdf)
        else:
            duplicates.append(pdf)

    print("Número de duplicatas encontradas: ", str(len(duplicates)))
    for dup in duplicates:
        os.remove(dup)
        print("Removido: ", dup)

    return [f for f in filtered]

def filtrar_imagens(pdf_files):
    scans = []
    filtered = []

    for pdf in pdf_files:

        # arquivos vazios
        if os.path.getsize(pdf) == 0:  
            print(f"PDF vazio: {pdf}")
            scans.append(pdf)
            continue

        doc = fitz.open(pdf)
        only_image = True

        # Se qualquer página for somente imagem (um scan)
        for page in doc:
            text = page.get_text().strip()
            if text:
              only_image = False
        if only_image == True:
            scans.append(pdf)
        else :
            filtered.append(pdf)

    print("Número de arquivos só com imagens: ", str(len(scans)))
    for scan in scans:
        os.remove(scan)
        print("Removido: ", scan)

    return [f for f in filtered]

def tratar_arquivos(pdf_files):
    resultados = {}

    for pdf in pdf_files:
        print(f"=== [ARQUIVO] Processando: {os.path.basename(pdf)}")
        doc = fitz.open(pdf)
        pages = []

        for page in doc:
            text = page.get_text("text").strip()
            if text:
                clean_text = ut.limpar_texto(text)
                normalized_text = normalizar_texto(clean_text)
                pages.append(normalized_text)

        resultados[pdf] = pages  # salva o texto limpo por PDF
        doc.close()

    return resultados

def normalizar_texto(texto):
    
    # Normaliza datas
    padrao_datas = r'\b\d{1,4}[-/]\d{1,2}[-/]\d{2,4}\b'
    for match in re.finditer(padrao_datas, texto):
        resultado = ut.substituir_data(match)
        print(f"[DATA] Encontrada: {match.group()} -> {resultado}")
    texto = re.sub(padrao_datas, ut.substituir_data, texto)

    # Normaliza valores
    #padrao_valores = r'R?\$?\s*(\d{1,3}(?:[\.,]\d{3})*[\.,]\d{2})'
    #for match in re.finditer(padrao_valores, texto):
    #    resultado = ut.normalizar_valor(match)
    #    print(f"[VALOR] Encontrado: {match.group()} -> {resultado}")
    #texto = re.sub(padrao_valores, ut.normalizar_valor, texto)

    # Normaliza abreviações
    substituicoes = {
        r'\bv\.?\s*total\b': 'valor total',
        r'\bv\.?\s*unit[aá]rio\b': 'valor unitário',
        r'\bobs\.?\b': 'observações',
        r'\bun\.?\b': 'unidade',
        r'\bunidades\b': 'unidades',
    }
    for regex, padrao in substituicoes.items():
        matches = list(re.finditer(regex, texto, flags=re.IGNORECASE))
        for match in matches:
            print(f"[ABREV] Encontrada: {match.group()} -> {padrao}")
        texto = re.sub(regex, padrao, texto, flags=re.IGNORECASE)

    return texto

def criar_dataset(pdf_textos):
    dataset = []

    for pdf, pages in pdf_textos.items():
        texto_documento = "\n".join(pages).strip()
        entrada = f"{PROMPT}\n\nDocumento:\n{texto_documento}"

        dataset_pdf = {
            "input": entrada,
            "target": ""
        }

        dataset.append(dataset_pdf)
        salvar_dataset(pdf, [dataset_pdf])

    return dataset


def salvar_dataset(pdf, dataset):
    filename_base = os.path.splitext(os.path.basename(pdf))[0]
    path = f"output/dataset/{filename_base}.jsonl"
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"Dataset salvo em {path}")

