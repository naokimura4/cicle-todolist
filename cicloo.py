
materias_lista = []
diff_lista = []
c = 0
# Inputando dias e horas para criar a carga horária
dias = int(input("Quantos dias pretende estudar?"))
horas = int(input("Quantas horas pretende estudar?"))
ch = dias*horas
while True:
    # Inputando Matéria para adicionar a lista
    materia = str(input("Digite uma matéria: ")).strip().upper()
    materias_lista.append(materia)
    # Definindo loop caso o valor seja maior que 5
    while True:
        print('''NÍVEIS DE DIFICULDADE:
[1] PÉSSIMO
[2] RUIM
[3] MEDIANO
[4] BOM
[5] ÓTIMO''')
        diff = int(input("Digite o nível de dificuldade: "))
        match diff:
            case 1:
                diff = 5
            case 2:
                diff = 4
            case 3:
                diff = 3
            case 4:
                diff = 2
            case 5:
                diff = 1
            case _:
                print("Você deve escolher um dos números válodos...Tente Novamente")
                continue        
        diff_lista.append(diff)
        c += diff
        break
    # Calcula o Valor Base
    ask = str(input("Deseja Adicionar mais matérias? [S/N]"))[0].strip()
    if ask in 'sS':
        continue
    else:
        break
    
v_base = ch/c

for materia, diff in zip(materias_lista,diff_lista):
    print(f"{materia} = {diff*v_base:.0f}")
