import json
import os
import re
import fitz # PyMuPDF

def normalizar_nome(filename):
    name = re.sub(r"\s*\(\d+\)", "", filename, flags=re.IGNORECASE)     # (1) e afins
    name = re.sub(r"\s*copy(\s*\d+)?", "", name, flags=re.IGNORECASE)   # copy e afins
    return name

def carregar_pdf(folder):
    pdf_files = [folder + "/" + f for f in os.listdir(folder) if f.endswith(".pdf")]
    pdf_files = filtrar_duplicatas(pdf_files)
    pdf_files = filtrar_imagens(pdf_files)

    print("Número de arquivos PDFs carregados: ", str(len(pdf_files)))
    return pdf_files

def filtrar_duplicatas(pdf_files):
    duplicates = []
    filtered = []

    for pdf in pdf_files:
        normalized = normalizar_nome(pdf)
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

        if os.path.getsize(pdf) == 0:  # arquivo vazio
            print(f"PDF vazio: {pdf}")
            scans.append(pdf)
            continue

        doc = fitz.open(pdf)
        only_image = True

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

def criar_dataset(pdf_files): # Separação por
    dataset = []

    for pdf in pdf_files:
        doc = fitz.open(pdf)
        pages = []

        for page in doc:
            text = page.get_text("text").strip()
            if text:
                clean_text = " ".join(text.split())
                pages.append(clean_text)

        dataset.append({
            "input": "\n".join(pages),
            "target": ""  # Fazer o resultado :(
        })

        salvar_dataset(pdf, dataset)

    return dataset

def salvar_dataset(pdf, dataset):
    filename_base = os.path.splitext(os.path.basename(pdf))[0]  # remove .pdf
    path = f"output/dataset/{filename_base}.jsonl"  # extensão que desejar

    with open(path, "w", encoding="utf-8") as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"Dataset salvo em ", path)