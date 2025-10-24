🖥️ Loja de Informática
🍇 Grape Tech - CRUD Web 
Este é um projeto de site para uma loja de informática, desenvolvido com foco em operações CRUD (Criar, Ler, Atualizar e Deletar) de produtos.

📌 Objetivo
Criar uma aplicação web funcional que permita o gerenciamento completo de produtos de informática, como computadores, periféricos, acessórios e componentes, por meio de uma interface amigável e intuitiva.

⚙️ Funcionalidades
🔍 Listagem de produtos: Exibe todos os produtos cadastrados com detalhes.

➕ Cadastro de produto: Permite adicionar novos produtos ao banco de dados.

✏️ Edição de produto: Atualiza informações de produtos existentes.

🗑️ Exclusão de produto: Remove produtos do sistema.

👤 Cadastro de usuários: Qualquer visitante pode se registrar com nome, e-mail e senha.

🔑 Login de usuários: Acesso ao sistema com verificação de credenciais.

🔐 Sistema de autenticação: Login para acesso administrativo.

🎨 Interface responsiva: Desenvolvida com HTML e CSS para boa experiência em diferentes dispositivos.

🛠️ Tecnologias Utilizadas
🐍 Python 3.10+

🔧 Flask

🌐 HTML5

🎨 CSS3

🛢️ MySQL

🧩 Passo a passo para executar

1. Clone o repositório

bash
git clone https://github.com/nicolas-vmaria/Loja-de-informatica.git
cd Loja-de-informatica

2. Crie um ambiente virtual (recomendado)

bash
python -m venv venv

3. Ative o ambiente virtual

Windows:

bash
venv\Scripts\activate
Linux/Mac:

bash
source venv/bin/activate
4. Instale as dependências

bash
pip install -r requirements.txt

5. Configure o banco de dados MySQL
Crie um banco chamado loja_informatica

Execute os scripts SQL para criar as tabelas Usuarios, Produtos, Carrinho

Verifique se os dados de conexão no app.py estão corretos:

python
host="localhost"
user="root"
password="12345678"
database="loja_informatica"

6. Execute a aplicação

bash
python app.py

7. Acesse no navegador

Code
http://localhost:5000