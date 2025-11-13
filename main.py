import csv

# Funções para cálculo
def calcular_aluguel(tipo, quartos=1, garagem=False, criancas=True, vagas_extra=0):
    if tipo == "Apartamento":
        valor = 700
        if quartos == 2:
            valor += 200
        if garagem:
            valor += 300
        if not criancas:
            valor *= 0.95  # desconto 5%
    elif tipo == "Casa":
        valor = 900
        if quartos == 2:
            valor += 250
        if garagem:
            valor += 300
    elif tipo == "Estudio":
        valor = 1200
        valor += 250  # duas vagas padrão
        if vagas_extra > 0:
            valor += vagas_extra * 60
    else:
        raise ValueError("Tipo inválido")
    return round(valor, 2)

def gerar_parcelas(valor_contrato=2000, parcelas=5):
    return [round(valor_contrato / parcelas, 2) for _ in range(parcelas)]

def gerar_parcelas_aluguel(valor_aluguel, meses=12):
    return [round(valor_aluguel, 2) for _ in range(meses)]

def salvar_csv(parcelas_contrato, parcelas_aluguel, filename="orcamento.csv"):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Parcela", "Valor Contrato", "Valor Aluguel"])
        for i in range(max(len(parcelas_contrato), len(parcelas_aluguel))):
            contrato_valor = parcelas_contrato[i] if i < len(parcelas_contrato) else ""
            aluguel_valor = parcelas_aluguel[i] if i < len(parcelas_aluguel) else ""
            writer.writerow([i + 1, contrato_valor, aluguel_valor])

# Funções de validação
def validar_opcao(mensagem, opcoes_validas):
    while True:
        valor = input(mensagem).strip()
        if valor in opcoes_validas:
            return valor
        print(f"Opção inválida! Escolha uma das opções: {', '.join(opcoes_validas)}")

def validar_inteiro(mensagem, valores_validos):
    while True:
        try:
            valor = int(input(mensagem))
            if valor in valores_validos:
                return valor
            else:
                print(f"Valor inválido! Escolha entre {valores_validos}")
        except ValueError:
            print("Digite um número válido!")

def solicitar_vagas_extra():
    while True:
        try:
            vagas_extra = int(input("Quantas vagas extras além das 2 padrão? (0 a 2): "))
            if 0 <= vagas_extra <= 2:
                return vagas_extra
            else:
                print("Valor inválido! Digite um número entre 0 e 2.")
        except ValueError:
            print("Entrada inválida! Digite um número inteiro.")

# Interface no terminal
print("Escolha o tipo de imóvel:")
print("1 - Apartamento")
print("2 - Casa")
print("3 - Estudio")
opcao = validar_opcao("Digite a opção: ", ["1", "2", "3"])

tipo = "Apartamento" if opcao == "1" else "Casa" if opcao == "2" else "Estudio"

quartos = validar_inteiro("Quantos quartos? (1 ou 2): ", [1, 2])
garagem = validar_opcao("Deseja garagem? (s/n): ", ["s", "n"]) == "s"
criancas = True
vagas_extra = 0

if tipo == "Apartamento":
    criancas = validar_opcao("Possui crianças? (s/n): ", ["s", "n"]) == "s"
elif tipo == "Estudio":
    vagas_extra = solicitar_vagas_extra()

# Calcular valores
valor_aluguel = calcular_aluguel(tipo, quartos, garagem, criancas, vagas_extra)
parcelas_contrato = gerar_parcelas()
parcelas_aluguel = gerar_parcelas_aluguel(valor_aluguel)

# Exibir resumo
print(f"\nResumo do Orçamento:")
print(f"Tipo: {tipo}")
print(f"Aluguel mensal: R$ {valor_aluguel}")
print(f"Parcelas do contrato: {parcelas_contrato}")
print(f"Parcelas do aluguel (12 meses): {parcelas_aluguel}\n")

# Salvar CSV
salvar_csv(parcelas_contrato, parcelas_aluguel)
print("Arquivo orcamento.csv gerado com sucesso!\n")