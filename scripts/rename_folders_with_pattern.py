import os

def renomear_pastas_com_padrao(diretorio, prefixo):
    """
    Renomeia todas as pastas dentro do diretório com um prefixo e move para uma subpasta 'renomeados'.
    """

    if not os.path.isdir(diretorio):
        print(f"O diretório '{diretorio}' não existe.")
        return

    pasta_destino = os.path.join(diretorio, "renomeados")
    os.makedirs(pasta_destino, exist_ok=True)

    for nome_pasta in os.listdir(diretorio):
        caminho_pasta = os.path.join(diretorio, nome_pasta)

        # Ignora a pasta 'renomeados' e quaisquer pastas já dentro dela
        if nome_pasta == "renomeados" or not os.path.isdir(caminho_pasta):
            continue

        novo_nome = f"{prefixo}-{nome_pasta}"
        novo_caminho = os.path.join(pasta_destino, novo_nome)

        if os.path.exists(novo_caminho):
            print(f"[⚠️] Já existe: {novo_caminho}")
            continue

        try:
            os.rename(caminho_pasta, novo_caminho)
            print(f"[✅] Renomeada: {nome_pasta} -> {novo_nome}")
        except PermissionError:
            print(f"[⛔] Sem permissão para mover: {nome_pasta}")
        except Exception as e:
            print(f"[❌] Erro ao mover {nome_pasta}: {e}")

if __name__ == "__main__":
    renomear_pastas_com_padrao("./", "reactjs")
