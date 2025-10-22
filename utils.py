import re
from datetime import datetime

def normalizar_nome(filename):
    name = re.sub(r"\s*\(\d+\)", "", filename, flags=re.IGNORECASE)     # (1) e afins
    name = re.sub(r"\s*copy(\s*\d+)?", "", name, flags=re.IGNORECASE)   # copy e afins
    return name

def limpar_texto(texto):
    # Remove possíveis cabeçalhos/rodapés repetidos por página (ex: "Página X de Y")
    texto = re.sub(r'(?i)p[aá]gina\s*\d+(\s*de\s*\d+)?', '', texto)

    # Remove links (http, https, www)
    texto = re.sub(r'http\S+|www\.\S+', '', texto)

    # Remove caracteres especiais indesejados (mantém letras, números e pontuação básica)
    texto = re.sub(r'[^a-zA-Z0-9À-ÿ\s.,;:!?()\-\']', '', texto)

    # Remove múltiplos espaços, tabs e quebras de linha
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    return texto
    
def substituir_data(match):
    data_str = match.group()
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d", "%Y-%m-%d"):
        try:
            data = datetime.strptime(data_str, fmt)
            return data.strftime("%Y-%d-%m")  
        except ValueError:
            continue
    return data_str  

def normalizar_valor(match):
    valor = match.group().strip()  # remove espaços

    # Remove prefixos R, R$, espaços extras
    valor = re.sub(r'^[Rr]\s*\$?\s*', '', valor)
    
    # Virgula -> ponto
    if "," in valor and valor.count(",") == 1 and valor.count(".") == 0:
        valor = valor.replace(",", ".")
    # Ponto e virgula -> nada e ponto
    elif "," in valor and "." in valor:
        valor = valor.replace(".", "").replace(",", ".")
    # Ponto -> ponto
    else:
        valor = valor

    return "R$" + valor