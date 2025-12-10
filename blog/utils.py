import secrets
import string
import json

def generate_code(length: int = 7) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def read_dados_json():
    try:
        with open('dados.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}
