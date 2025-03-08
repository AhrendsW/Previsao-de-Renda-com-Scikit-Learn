# Documentação da API de Previsão de Renda

Esta documentação descreve os endpoints disponíveis na API de Previsão de Renda e como utilizá-los.

## Base URL

Quando executada localmente, a API está disponível em:

```
http://localhost:8000
```

## Endpoints

### Health Check

```
GET /health
```

Verifica se a API está funcionando corretamente.

**Resposta de Sucesso:**
```json
{
  "status": "ok",
  "message": "API está funcionando corretamente"
}
```

### Previsão de Renda

```
POST /predict
```

Realiza a previsão da faixa de renda com base nas características fornecidas.

**Parâmetros de Entrada:**

| Campo           | Tipo    | Descrição                                      |
|-----------------|---------|------------------------------------------------|
| age             | integer | Idade em anos                                  |
| workclass       | integer | Classe de trabalho (codificada)                |
| education       | integer | Nível educacional (codificado)                 |
| education_num   | integer | Número de anos de educação                     |
| marital_status  | integer | Estado civil (codificado)                      |
| occupation      | integer | Ocupação (codificada)                          |
| relationship    | integer | Relacionamento (codificado)                    |
| race            | integer | Raça (codificada)                              |
| sex             | integer | Sexo (codificado)                              |
| capital_gain    | integer | Ganho de capital                               |
| capital_loss    | integer | Perda de capital                               |
| hours_per_week  | integer | Horas trabalhadas por semana                   |
| native_country  | integer | País de origem (codificado)                    |

**Exemplo de Requisição:**
```json
{
  "age": 39,
  "workclass": 4,
  "education": 11,
  "education_num": 13,
  "marital_status": 2,
  "occupation": 10,
  "relationship": 0,
  "race": 4,
  "sex": 1,
  "capital_gain": 2174,
  "capital_loss": 0,
  "hours_per_week": 40,
  "native_country": 39
}
```

**Resposta de Sucesso:**
```json
{
  "prediction": 1,
  "prediction_label": ">50K",
  "probability": 0.78,
  "model_info": {
    "model_type": "XGBoost",
    "model_version": "1.0"
  }
}
```

**Códigos de Resposta:**

| Código | Descrição                                                  |
|--------|-----------------------------------------------------------|
| 200    | Sucesso - Retorna a previsão                              |
| 400    | Erro de validação - Parâmetros inválidos ou incompletos   |
| 500    | Erro interno do servidor                                  |

### Mapeamento de Categorias

```
GET /mappings
```

Retorna o mapeamento das variáveis categóricas para seus valores codificados.

**Resposta de Sucesso:**
```json
{
  "workclass": {
    "Private": 4,
    "Self-emp-not-inc": 6,
    "Local-gov": 2,
    "?": 0,
    "State-gov": 7,
    "Self-emp-inc": 5,
    "Federal-gov": 1,
    "Without-pay": 8,
    "Never-worked": 3
  },
  "education": {
    "HS-grad": 7,
    "Some-college": 13,
    "Bachelors": 2,
    "Masters": 10,
    "Assoc-voc": 1,
    "11th": 0,
    "Assoc-acdm": 0,
    "10th": 0,
    "7th-8th": 0,
    "Prof-school": 12,
    "9th": 0,
    "12th": 0,
    "Doctorate": 5,
    "5th-6th": 0,
    "1st-4th": 0,
    "Preschool": 0
  },
  // Outros mapeamentos...
}
```

## Exemplos de Uso

### Exemplo com cURL

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
           "age": 39,
           "workclass": 4,
           "education": 11,
           "education_num": 13,
           "marital_status": 2,
           "occupation": 10,
           "relationship": 0,
           "race": 4,
           "sex": 1,
           "capital_gain": 2174,
           "capital_loss": 0,
           "hours_per_week": 40,
           "native_country": 39
         }'
```

### Exemplo com Python (requests)

```python
import requests
import json

# Dados de teste
test_data = {
    "age": 39,
    "workclass": 4,
    "education": 11,
    "education_num": 13,
    "marital_status": 2,
    "occupation": 10,
    "relationship": 0,
    "race": 4,
    "sex": 1,
    "capital_gain": 2174,
    "capital_loss": 0,
    "hours_per_week": 40,
    "native_country": 39
}

# Fazer requisição para a API
response = requests.post(
    "http://localhost:8000/predict",
    json=test_data,
    headers={"Content-Type": "application/json"}
)

# Verificar resposta
if response.status_code == 200:
    print("Previsão:", json.dumps(response.json(), indent=2))
else:
    print("Erro:", response.text)
```

## Notas Importantes

1. Todos os valores categóricos devem ser enviados já codificados conforme o mapeamento retornado pelo endpoint `/mappings`.
2. A API retorna a previsão (0 ou 1) e a probabilidade associada.
3. O valor 1 corresponde a uma renda anual ">50K" e o valor 0 corresponde a "<=50K".
4. Para obter os mapeamentos das categorias, utilize o endpoint `/mappings` antes de fazer previsões. 