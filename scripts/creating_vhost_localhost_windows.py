import os
import subprocess
import textwrap

# Caminhos comuns
APACHE_BIN = r'C:\xampp\apache\bin'
VHOSTS_CONF = r'C:\xampp\apache\conf\extra\httpd-vhosts.conf'
HOSTS_PATH = r'C:\Windows\System32\drivers\etc\hosts'

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Erro ao executar comando: {e}")
        return ""

def check_apache_running():
    result = run_cmd('tasklist /FI "IMAGENAME eq httpd.exe"')
    if 'httpd.exe' in result:
        print('[🟢] Apache está rodando!')
        return True
    else:
        print('[🔴] Apache não está rodando!')
        return False

def start_apache():
    if not check_apache_running():
        run_cmd(f'cd {APACHE_BIN} && httpd -k start')
        print('[✅] Apache iniciado com sucesso!')
    else:
        print('[ℹ️] Apache já está rodando.')

def stop_apache():
    if check_apache_running():
        run_cmd(f'cd {APACHE_BIN} && httpd -k stop')
        print('[🛑] Apache parado com sucesso!')
    else:
        print('[ℹ️] Apache já está parado.')

def restart_apache():
    if check_apache_running():
        run_cmd(f'cd {APACHE_BIN} && httpd -k restart')
        print('[🔄] Apache reiniciado com sucesso!')
    else:
        print('[ℹ️] Apache estava parado. Iniciando...')
        start_apache()

def add_to_hosts(ip, hostname):
    with open(HOSTS_PATH, 'r') as f:
        content = f.read()
        entry = f"{ip}    {hostname}.localhost"
        if entry in content:
            print('[ℹ️] Entrada já existe no hosts.')
            return
    with open(HOSTS_PATH, 'a') as f:
        f.write(f'\n{entry}')
    print('[✅] Entrada adicionada ao arquivo hosts.')

def create_vhost(name, servername, documentroot):
    try:
        add_to_hosts("127.0.0.1", name)

        vhost_entry = textwrap.dedent(f"""
            ## {name}
            <VirtualHost *:80>
                ServerAdmin webmaster@dummy-host2.example.com
                ServerName {servername}.localhost
                DocumentRoot "{documentroot}"

                <Directory "{documentroot}">
                    Options Indexes FollowSymLinks Includes ExecCGI
                    AllowOverride All
                    Require all granted
                </Directory>

                ErrorLog "logs/{servername}-error.log"
                CustomLog "logs/{servername}-access.log" common
            </VirtualHost>
        """)
        with open(VHOSTS_CONF, 'a') as f:
            f.write("\n\n" + vhost_entry)
        print('[✅] VHost criado com sucesso!')

        run_cmd("ipconfig /flushdns")
        print('[🧠] Cache DNS limpo.')

        restart_apache()
        print(f'[🌐] Acesse: http://{servername}.localhost')
    except Exception as e:
        print(f"[❌] Erro ao criar VHost: {e}")

def init():
    name = input('Digite o nome do host (ex: meuapp): ').strip()
    servername = input('Digite o nome do servidor (ex: meuapp): ').strip()
    documentroot = input('Digite o caminho da pasta do site (ex: C:/meus-sites/meuapp): ').strip()
    
    if not os.path.exists(documentroot):
        print('[❌] Caminho inválido para o DocumentRoot.')
        return

    create_vhost(name, servername, documentroot)

if __name__ == "__main__":
    try:
        init()
    except Exception as e:
        print(f"[❌] Erro geral: {e}")
