import json
import os
import datetime

FILE_PATH = "App/assets/storage/dados.json"

def debug_json(): # Analizar questão do "with"
    with open("dados.json", "r", encoding="utf-8") as file:
        dados = json.load(file)
        print("Dados Salvos no JSON:", json.dumps(dados, indent=4))


def salvar_dados(carga_horaria, materias, ultima_data=None):
    """Salva a carga horária, matérias e última data em um arquivo JSON."""
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
        ],
        "ultima_data": ultima_data or datetime.date.today().isoformat()
        
    }
    
    with open(FILE_PATH, "w") as f:
        json.dump(dados, f, indent=4)


def carregar_dados():
    """Carrega a carga horária, matérias e a última data do ciclo."""
    if not os.path.exists(FILE_PATH):
        return 0, [], None  # Retorna valores padrão se o arquivo não existir

    try:
        with open(FILE_PATH, "r") as file:
            dados = json.load(file)
            return (
                dados.get("carga_horaria", 0),
                dados.get("materias", []),
                dados.get("ultima_data", None)  # Pode ser None se não existir no JSON
            )
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return 0, [], None  # Retorno seguro em caso de erro
