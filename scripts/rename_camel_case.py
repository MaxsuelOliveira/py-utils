import os 
import re

def converter_para_camel_case(texto):
    """
    Converte uma string para CamelCase.
    Exemplo: 'minha-pasta_teste exemplo' -> 'MinhaPastaTesteExemplo'
    """
    partes = re.split(r'[\s\-_]+', texto)  # divide por espaço, hífen ou underscore
    return ''.join(p.capitalize() for p in partes if p)

def renomear_pastas_para_camel_case(diretorio):
    """
    Renomeia todas as pastas no diretório para o padrão CamelCase.
    """
    if not os.path.isdir(diretorio):
        print(f"O diretório '{diretorio}' não existe.")
        return

    for nome_pasta in os.listdir(diretorio):
        caminho_pasta = os.path.join(diretorio, nome_pasta)

        if os.path.isdir(caminho_pasta):
            novo_nome = converter_para_camel_case(nome_pasta)

            if novo_nome == nome_pasta:
                continue  # já está em CamelCase

            novo_caminho = os.path.join(diretorio, novo_nome)

            if os.path.exists(novo_caminho):
                print(f"[⚠️] Já existe: {novo_nome}")
                continue

            try:
                os.rename(caminho_pasta, novo_caminho)
                print(f"[✅] Renomeada: {nome_pasta} -> {novo_nome}")
            except PermissionError:
                print(f"[⛔] Sem permissão para renomear: {nome_pasta}")
            except Exception as e:
                print(f"[❌] Erro ao renomear {nome_pasta}: {e}")

if __name__ == "__main__":
    renomear_pastas_para_camel_case("./")