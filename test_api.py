import requests
import json

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

print("Dados de teste:", json.dumps(test_data, indent=2))

try:
    health_response = requests.get("http://localhost:8000/health")
    print("\nHealth check:")
    print("Status Code:", health_response.status_code)
    print("Response:", health_response.json())
except Exception as e:
    print("\nErro no health check:", str(e))

try:
    print("\nFazendo requisição para /predict...")
    response = requests.post(
        "http://localhost:8000/predict",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    print("Status Code:", response.status_code)
    if response.status_code == 200:
        print("Response:", json.dumps(response.json(), indent=2))
    else:
        print("Erro Response:", response.text)
except Exception as e:
    print("Erro na requisição:", str(e))
    raise