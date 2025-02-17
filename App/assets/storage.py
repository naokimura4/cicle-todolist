import json
import os

FILE_PATH = "App/assets/storage/dados.json"

def debug_json(): # Analizar questão do "with"
    with open("dados.json", "r", encoding="utf-8") as file:
        dados = json.load(file)
        print("Dados Salvos no JSON:", json.dumps(dados, indent=4))

def salvar_dados(carga_horaria, materias):
    """Salva a carga horária e as matérias em um arquivo JSON."""
    dados = {
        "carga_horaria": carga_horaria,
        "materias": [
            {
                "nome": m["nome"],
                "dificuldade": m["dificuldade"],
                "checkboxes": m["checkboxes"],
                "checkbox_states": m["checkbox_states"]
            }
            for m in materias
        ]
    }
    with open(FILE_PATH, "w") as f:
        json.dump(dados, f, indent=4)

def carregar_dados():
    """Carrega a carga horária e as matérias do JSON, se o arquivo existir."""
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            dados = json.load(f)
            return dados["carga_horaria"], dados["materias"]
    return 0, []  # Retorna valores padrão caso o arquivo não exista
