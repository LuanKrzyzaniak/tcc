https://aws.amazon.com/blogs/machine-learning/an-introduction-to-preparing-your-own-dataset-for-llm-training/

#### Objeto de estudo

- Documentos legais: 

#### Métricas

Primária
- Attribute-level micro-F1

Secundária
- Exact-match (exatidão do JSON)
- Attribute-level macro-F1
- TEDs

Informações acadêmicas
- Curva de erro por
    - Tamanho do documento
    - Tipo de campo (data, nome, valor)

#### Prompt

''' 
Extraia o conteúdo da Ata de Registro de Preços (ARP) e estruture-o estritamente no formato JSON fornecido abaixo. Garanta que todos os campos vazios sejam preenchidos com os dados correspondentes encontrados no texto de entrada. Para campos que se referem a quantidades, valores e percentuais, utilize o formato exato encontrado no documento.
{
  "Documento": {
    "Numero_ARP": "",
    "Numero_Processo": "",
  },
  "Orgao_Gerenciador": {
    "Razao_Social": "",
    "CNPJ": "",
    "UG": "",
    "Endereco": "",
    "Representantes_Legais": [
      {
        "Cargo": "Superintendente",
        "Nome": "",
        "Matricula": ""
      },
      {
        "Cargo": "Gerente Administrativo",
        "Nome": "",
        "Matricula": ""
      }
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
  "Objeto_e_Vigencia": {
    "Descricao_Objeto": "",
    "Instrumento_Convocatorio": "",
    "Validade_ARP": "",
    "Prorrogavel": ""
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
  "Valores_Globais": {
    "Valor_Total_Global_Itens_Registrados": "",
    "Valor_Por_Extenso": ""
  },
  "Regras_Adesao": {
    "Adesao_Admitida": "",
    "Itens_Excluidos_Adesao": [],
    "Limite_Adicional_Nao_Participante_Percentual": "",
    "Limite_Adicional_Total_Quantitativo_Multiplicador": ""
  },
  "Foro": ""
}
'''