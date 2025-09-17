"""
FarmTech Solutions - Aplicação Agricultura Digital (Versão melhorada)

Salvar como: farmtech.py
Executar: python farmtech.py

Resumo das funcionalidades:
- Inserir culturas (cada cultura pode ter múltiplas sub-áreas).
- Para cada sub-área: inserir área direta OU calcular por geometria (retângulo, triângulo, círculo).
- Calcula área total por cultura.
- Permite definir insumo com taxa de aplicação:
    * por área (ex: litro por m² ou litro por hectare)
    * por rua (ex: mL por metro de rua) -> pergunta número de ruas e comprimento médio da rua.
- Menu com inserir, mostrar, atualizar, deletar, exportar CSV para R e sair.
- Dados mantidos em lista (vetor) de dicionários. Também exporta vetores (colunas) para CSV.
"""

import csv
import math
import sys

# -----------------------------
# Estrutura de dados principal
# -----------------------------
# lista de dicionários; cada dicionário representa uma cultura/registro
culturas_data = []


# -----------------------------
# Funções utilitárias
# -----------------------------
def leia_opcao(mensagem, opcoes=None):
    """
    Lê uma opção do usuário com validação básica.
    Se opcoes for lista, força a entrada a estar nela.
    """
    while True:
        val = input(mensagem).strip()
        if opcoes:
            if val in opcoes:
                return val
            else:
                print("Opção inválida. Escolha uma das opções:", opcoes)
        else:
            if val == "":
                print("Entrada vazia. Tente novamente.")
                continue
            return val


def leia_float(mensagem, minimo=None):
    """Lê um float com validação opcional de mínimo."""
    while True:
        s = input(mensagem).strip()
        try:
            v = float(s.replace(",", "."))
            if minimo is not None and v < minimo:
                print(f"Valor deve ser >= {minimo}.")
                continue
            return v
        except ValueError:
            print("Número inválido. Digite um valor numérico (ex: 1234.5).")


def calcular_area_por_geometria():
    """
    Pede ao usuário o tipo de geometria e parâmetros,
    retorna (area_m2, descricao_tipo)
    """
    while True:
        print("\nTipos de geometria:")
        print("1 - Retângulo (comprimento × largura)")
        print("2 - Triângulo (base × altura / 2)")
        print("3 - Círculo (π × raio²)")
        print("4 - Polígono simples por inserção direta de área")
        opc = leia_opcao("Escolha (1-4): ", opcoes=["1", "2", "3", "4"])
        if opc == "1":
            c = leia_float("Comprimento (m): ", minimo=0)
            l = leia_float("Largura (m): ", minimo=0)
            area = c * l
            tipo = f"Retângulo ({c}×{l} m)"
            return area, tipo
        elif opc == "2":
            b = leia_float("Base (m): ", minimo=0)
            h = leia_float("Altura (m): ", minimo=0)
            area = (b * h) / 2
            tipo = f"Triângulo (base {b} m × altura {h} m)"
            return area, tipo
        elif opc == "3":
            r = leia_float("Raio (m): ", minimo=0)
            area = math.pi * r ** 2
            tipo = f"Círculo (raio {r} m)"
            return area, tipo
        elif opc == "4":
            area = leia_float("Digite a área total desta sub-área (m²): ", minimo=0)
            tipo = f"Área direta ({area} m²)"
            return area, tipo


def adicionar_cultura():
    """
    Insere uma nova cultura, permitndo múltiplas sub-áreas e definindo insumo.
    """
    print("\n=== Inserir nova cultura ===")
    nome = leia_opcao("Nome da cultura (ex: Milho, Soja): ")

    # inserir múltiplas sub-áreas
    sub_areas = []
    while True:
        print("\nInserindo sub-área para", nome)
        area, tipo_desc = calcular_area_por_geometria()
        sub_areas.append({"area_m2": area, "tipo": tipo_desc})
        mais = input("Deseja adicionar outra sub-área para esta cultura? (s/n): ").strip().lower()
        if mais != "s":
            break

    area_total = sum(sa["area_m2"] for sa in sub_areas)
    print(f"Área total calculada para {nome}: {area_total:.2f} m²")

    # Definição do insumo e modo de aplicação
    print("\nDefina o insumo e a forma de aplicação:")
    insumo_nome = leia_opcao("Nome do insumo (ex: Fosfato, Herbicida X): ")
    print("Modos de aplicação:")
    print("1 - Aplicação por área (ex: L por m² ou L por hectare)")
    print("2 - Aplicação por rua (ex: mL por metro de rua)")
    modo = leia_opcao("Escolha (1-2): ", opcoes=["1", "2"])

    insumo_info = {}
    if modo == "1":
        # perguntar unidade: por m² ou por ha
        unidade = leia_opcao("Unidade de aplicação: 1 - por m², 2 - por hectare (ha): ", opcoes=["1", "2"])
        if unidade == "1":
            taxa = leia_float("Taxa de aplicação (unidades por m²) — ex: 0.0005 L/m²: ", minimo=0)
            quantidade_total = taxa * area_total
            insumo_info = {
                "modo": "por_area_m2",
                "taxa": taxa,
                "unidade": "L/m² ou unidades/m² (conforme informado)",
                "quantidade_total": quantidade_total
            }
        else:
            taxa = leia_float("Taxa de aplicação (unidades por ha) — ex: 5 L/ha: ", minimo=0)
            hectares = area_total / 10000.0
            quantidade_total = taxa * hectares
            insumo_info = {
                "modo": "por_area_ha",
                "taxa": taxa,
                "unidade": "L/ha",
                "hectares": hectares,
                "quantidade_total": quantidade_total
            }

    else:  # modo == "2" -> por rua
        taxa_ml_por_m = leia_float("Taxa (mL por metro de rua): ", minimo=0)
        # perguntar número de ruas e comprimento médio por rua
        sabe_ruas = leia_opcao("Você sabe o número de ruas? (s/n): ", opcoes=["s", "n"])
        if sabe_ruas == "s":
            num_ruas = int(leia_float("Número de ruas: ", minimo=0))
            comprimento_m = leia_float("Comprimento médio de uma rua (m): ", minimo=0)
            total_metros = num_ruas * comprimento_m
        else:
            # alternativa: estimar número de ruas pela largura e espaçamento
            largura_campo = leia_float("Informe a largura aproximada do campo (m): ", minimo=0)
            espacamento_rua = leia_float("Espaçamento entre linhas/ruas (m): ", minimo=0.01)
            num_ruas = int(max(1, largura_campo // espacamento_rua))
            comprimento_m = area_total / largura_campo if largura_campo > 0 else 0
            total_metros = num_ruas * comprimento_m
            print(f"Estimativa: {num_ruas} ruas × {comprimento_m:.2f} m comprimento ≈ {total_metros:.2f} m")

        quantidade_total_ml = taxa_ml_por_m * total_metros
        quantidade_total_l = quantidade_total_ml / 1000.0  # converter para litros
        insumo_info = {
            "modo": "por_rua",
            "taxa_ml_por_m": taxa_ml_por_m,
            "num_ruas": num_ruas,
            "comprimento_medio_rua": comprimento_m,
            "total_metros": total_metros,
            "quantidade_total_ml": quantidade_total_ml,
            "quantidade_total_l": quantidade_total_l,
            "unidade": "mL/m"
        }

    # Criar registro e adicionar na lista
    registro = {
        "nome": nome,
        "sub_areas": sub_areas,
        "area_total_m2": area_total,
        "insumo_nome": insumo_nome,
        "insumo_info": insumo_info
    }
    culturas_data.append(registro)
    print(f"Cultura '{nome}' adicionada com sucesso!\n")


def mostrar_dados():
    """Imprime todos os registros com detalhes."""
    if not culturas_data:
        print("\nNenhuma cultura registrada ainda.")
        return
    print("\n=== Dados das culturas registradas ===")
    for idx, r in enumerate(culturas_data):
        print(f"\n[{idx}] Cultura: {r['nome']}")
        print(f"    Área total: {r['area_total_m2']:.2f} m² ({r['area_total_m2']/10000:.4f} ha)")
        print("    Sub-áreas:")
        for j, sa in enumerate(r["sub_areas"]):
            print(f"       - {j}: {sa['tipo']} => {sa['area_m2']:.2f} m²")
        print(f"    Insumo: {r['insumo_nome']}")
        info = r['insumo_info']
        if info["modo"] == "por_area_m2":
            print(f"       Aplicação por m²: taxa {info['taxa']} => total {info['quantidade_total']:.4f} unidades")
        elif info["modo"] == "por_area_ha":
            print(f"       Aplicação por ha: taxa {info['taxa']} L/ha => hectares {info['hectares']:.4f} ha => total {info['quantidade_total']:.4f} L")
        else:  # por_rua
            print(f"       Aplicação por rua: {info['taxa_ml_por_m']} mL/m")
            print(f"       Ruas: {info['num_ruas']}, comprimento médio: {info['comprimento_medio_rua']:.2f} m, total metros: {info['total_metros']:.2f} m")
            print(f"       Total insumo: {info['quantidade_total_ml']:.2f} mL = {info['quantidade_total_l']:.4f} L")


def atualizar_registro():
    """Atualiza um registro existente (substitui por nova entrada)."""
    if not culturas_data:
        print("\nNenhum registro para atualizar.")
        return
    mostrar_dados()
    pos = int(leia_float("Digite a posição (índice) do registro que quer atualizar: ", minimo=0))
    if not (0 <= pos < len(culturas_data)):
        print("Posição inválida.")
        return
    print(f"\nAtualizando registro [{pos}] - {culturas_data[pos]['nome']}")
    # Simplesmente chamar adicionar_cultura e substituir
    print("Insira os novos dados (substituirá os existentes).")
    # criar novos dados coletando com função auxiliar
    # para reutilizar fluxo de adicionar, vamos temporariamente mover dados
    backup = culturas_data[pos]
    culturas_data.pop(pos)
    try:
        adicionar_cultura()
        print("Substituição realizada com sucesso.")
    except Exception as e:
        print("Erro ao atualizar. Restaurando dados antigos.", e)
        culturas_data.insert(pos, backup)


def deletar_registro():
    """Remove um registro pelo índice."""
    if not culturas_data:
        print("\nNenhum registro para deletar.")
        return
    mostrar_dados()
    pos = int(leia_float("Digite a posição (índice) do registro que quer deletar: ", minimo=0))
    if not (0 <= pos < len(culturas_data)):
        print("Posição inválida.")
        return
    confirmado = leia_opcao(f"Confirma exclusão do registro [{pos}] {culturas_data[pos]['nome']}? (s/n): ", opcoes=["s", "n"])
    if confirmado == "s":
        culturas_data.pop(pos)
        print("Registro deletado.")
    else:
        print("Operação cancelada.")


def exportar_para_csv(nome_arquivo="farmtech_export.csv"):
    """
    Exporta os dados para CSV com colunas: indice, nome, area_total_m2, insumo_nome, quantidade_estimada
    Também cria colunas derivadas úteis para R: area_ha.
    """
    if not culturas_data:
        print("Nada para exportar.")
        return
    with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Cabeçalho
        writer.writerow([
            "indice", "nome", "area_total_m2", "area_ha",
            "insumo_nome", "insumo_modo", "insumo_quantidade_total_unidade"
        ])
        for i, r in enumerate(culturas_data):
            info = r["insumo_info"]
            # extrair quantidade estimada em litros quando possível (fallback para None)
            qtd = None
            if info.get("modo") == "por_area_m2":
                qtd = info.get("quantidade_total")
            elif info.get("modo") == "por_area_ha":
                qtd = info.get("quantidade_total")
            elif info.get("modo") == "por_rua":
                qtd = info.get("quantidade_total_l")
            writer.writerow([
                i,
                r["nome"],
                f"{r['area_total_m2']:.4f}",
                f"{r['area_total_m2']/10000.0:.6f}",
                r["insumo_nome"],
                info.get("modo"),
                f"{qtd:.6f}" if qtd is not None else ""
            ])
    print(f"Exportado para {nome_arquivo} (pode ser lido no R com read.csv).")


def menu_principal():
    """Loop principal do menu."""
    while True:
        print("\n=== FarmTech - Menu Principal ===")
        print("1 - Inserir nova cultura")
        print("2 - Mostrar dados")
        print("3 - Atualizar registro")
        print("4 - Deletar registro")
        print("5 - Exportar para CSV (para uso no R)")
        print("6 - Sair")
        opc = leia_opcao("Escolha (1-6): ", opcoes=[str(i) for i in range(1, 7)])
        if opc == "1":
            adicionar_cultura()
        elif opc == "2":
            mostrar_dados()
        elif opc == "3":
            atualizar_registro()
        elif opc == "4":
            deletar_registro()
        elif opc == "5":
            nome_arquivo = input("Nome do arquivo CSV (enter para 'farmtech_export.csv'): ").strip()
            if not nome_arquivo:
                nome_arquivo = "farmtech_export.csv"
            exportar_para_csv(nome_arquivo)
        elif opc == "6":
            print("Encerrando. Salve seu trabalho (exportar CSV) se precisar. Até logo!")
            break


# -----------------------------
# Entrada principal
# -----------------------------
if __name__ == "__main__":
    print("Bem-vindo ao sistema FarmTech - Agricultura Digital")
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário. Saindo...")
        sys.exit(0)
