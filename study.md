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
Extraia o conteúdo das Atas de Registro de Preços (ARP) fornecidos nesse único prompt e estruture-o estritamente no formato JSON fornecido abaixo. Garanta que todos os campos vazios sejam preenchidos com os dados correspondentes encontrados no texto de entrada. Para campos que se referem a quantidades, valores e percentuais, utilize o formato exato encontrado no documento. Use o esquema baixo como exemplo, e adicione novos campos se encontrar. Retorne um JSON para cada arquivo e não insira cites. Campos com valores não encontrados devem estar vazios. Respeite o formato monetário do real nos campos monetários. Atenção especial  aos itens registrados.

{
  "Documento": {
    "Numero_ARP": "",
    "Numero_Processo": "",
  },
  "Orgao_Gerenciador": 
    "Razao_Social": "",
    "CNPJ": "",
    "UG": "",
    "Endereco": "",
    "Representantes_Legais": [
      {
        "Cargo": "",
        "Nome": ""
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
  ]
  "Valor_Total": ""
}
'''