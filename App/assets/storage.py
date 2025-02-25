import json
import os
import datetime

FILE_PATH = "App/assets/storage/dados.json"

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

def salvar_dados(carga_horaria, materias, ultima_data=None, dias_para_reset=None):
    _,_,_,dia_salvo = carregar_dados()
    dias_para_reset = dias_para_reset if dias_para_reset is not None else dia_salvo
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
        return 0, [], None, 0 

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
