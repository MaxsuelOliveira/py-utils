import ctypes
import os
import sys

HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
DEFAULT_DOMAIN = "seo.localhost"
DEFAULT_IP = "127.0.0.1"

"""Script para adicionar uma entrada ao arquivo hosts do Windows.
Este script permite que o usuário adicione uma entrada personalizada."""

def is_admin():
    """Verifica se o script está rodando como administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def add_host_entry(domain: str, ip_address: str):
    """Adiciona uma entrada ao arquivo hosts, se ainda não existir."""
    if not os.path.exists(HOSTS_PATH):
        print("[ERRO] O arquivo hosts não foi encontrado.")
        return

    entry = f"{ip_address} {domain}\n"
    print(f"[INFO] Iniciando a adição de '{domain}' ao arquivo hosts...")

    try:
        with open(HOSTS_PATH, "r+", encoding="utf-8") as file:
            content = file.readlines()
            if any(domain in line for line in content):
                print(f"[INFO] O domínio '{domain}' já está presente.")
                return

            file.write("\n" + entry)
            print(f"[SUCESSO] Entrada adicionada: {entry.strip()}")
    except PermissionError:
        print("[ERRO] Permissão negada. Execute este script como administrador.")
    except Exception as e:
        print(f"[ERRO] Erro ao modificar o arquivo hosts: {e}")

def solicitar_elevacao():
    """Reexecuta o script com permissões de administrador."""
    print("[INFO] Requisitando permissões de administrador...")
    script = os.path.abspath(sys.argv[0])
    params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, f'"{script}" {params}', None, 1
    )
    sys.exit()

if __name__ == "__main__":
    try:
        if not is_admin():
            solicitar_elevacao()
        else:
            domain = input(f"Digite o domínio (padrão: {DEFAULT_DOMAIN}): ").strip() or DEFAULT_DOMAIN
            ip_address = input(f"Digite o IP (padrão: {DEFAULT_IP}): ").strip() or DEFAULT_IP

            if " " in domain or "." not in domain:
                print("[ERRO] Domínio inválido.")
                sys.exit(1)
            if not ip_address.count(".") == 3:
                print("[ERRO] Endereço IP inválido.")
                sys.exit(1)
            
            add_host_entry(domain, ip_address)

    except KeyboardInterrupt:
        print("\n[INFO] Operação cancelada pelo usuário.")
    except Exception as e:
        print(f"[ERRO] Ocorreu um erro inesperado: {e}")
    finally:
        print("[INFO] Finalizando o script.")
        input("Pressione Enter para sair...")
