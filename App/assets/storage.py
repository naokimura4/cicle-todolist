import json
import os
import datetime

FILE_PATH = "App/assets/storage/dados.json"

def debug_json():
    """Analisa o conteúdo do JSON e imprime formatado."""
    if not os.path.exists(FILE_PATH):
        print("Arquivo JSON não encontrado.")
        return
    
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        dados = json.load(file)
        print("Dados Salvos no JSON:", json.dumps(dados, indent=4, ensure_ascii=False))

def inciar_storage():
    if not os.path.exists(FILE_PATH):
        dados_iniciais = {
            "carga_horaria": 0,
            "materias": [],
            "ultima_data": datetime.date.today().isoformat(),
            "dias_para_reset": 1
        }
        try:
            with open(FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(dados_iniciais, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error("Erro ao inicializar storage: %s", e)

def salvar_dados(carga_horaria, materias, ultima_data=None, dias_para_reset=1):
    """Salva a carga horária, matérias, última data e dias para reset no JSON."""
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
        "ultima_data": ultima_data or datetime.date.today().isoformat(),
        "dias_para_reset": dias_para_reset  
    }

    try:
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")


def carregar_dados():
    if not os.path.exists(FILE_PATH):
        return 0, [], None, 1  # 🔥 Agora retorna 4 valores corretamente

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            dados = json.load(file)
            return (
                dados.get("carga_horaria", 0),
                dados.get("materias", []),
                dados.get("ultima_data", None),
                dados.get("dias_para_reset", 1)  
            )
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return 0, [], None, 1  
