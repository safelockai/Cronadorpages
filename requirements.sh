#!/bin/bash

# Atualiza os pacotes existentes
pkg update && pkg upgrade -y

# Instala o Python e o pip
pkg install python -y
pkg install python-pip -y

# Instala as bibliotecas Python necessárias
pip install requests beautifulsoup4

# Configura o armazenamento externo para garantir permissão de escrita
termux-setup-storage

echo "Instalação completa. As ferramentas e pacotes necessários foram instalados."
