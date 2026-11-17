# 📚 Livraria Web

Sistema web de gestão de uma livraria, desenvolvido com Django e Python. O projeto tem como objetivo facilitar a organização e o controlo das principais operações de uma livraria, incluindo livros, autores, editoras, clientes, fornecedores, compras e vendas.

## 🎯 Objetivo do Projeto

Desenvolver uma aplicação web que permita gerir as informações e operações de uma livraria de forma organizada, centralizando os dados e facilitando o acompanhamento do stock e das movimentações de livros.

## ⚙️ Tecnologias Utilizadas

- **Python** — linguagem de programação.
- **Django** — framework para desenvolvimento web.
- **SQLite** — base de dados presente no projeto.
- **PostgreSQL** — backup SQL disponibilizado no repositório.
- **HTML e CSS** — estrutura e apresentação das páginas.

## ✨ Principais Módulos

O sistema contempla a gestão das seguintes entidades:

- 📖 **Livros:** registo de títulos, edições, preços, quantidades e capas.
- ✍️ **Autores:** organização dos autores das obras.
- 🏢 **Editoras:** registo das editoras responsáveis pelas publicações.
- 👥 **Clientes:** gestão dos clientes da livraria.
- 🚚 **Fornecedores:** registo de fornecedores.
- 📥 **Compras:** registo de aquisições de livros.
- 📤 **Vendas:** registo das vendas realizadas.

## 📁 Estrutura do Projeto

```text
livraria-web/
│
├── config/              # Configurações do Django
│
├── livraria/            # Aplicação principal
│
├── media/
│   └── capas/           # Capas dos livros
│
├── db.sqlite3           # Base de dados SQLite
├── livraria_backup.sql  # Backup da base de dados PostgreSQL
├── manage.py            # Ficheiro de gestão do Django
└── README.md            # Documentação do projeto
```

## 🚀 Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/manuelmtidi-lab/livraria-web.git
```

### 2. Entrar na pasta

```bash
cd livraria-web
```

### 3. Criar um ambiente virtual

```bash
python -m venv venv
```

### 4. Ativar o ambiente virtual

**Linux:**

```bash
source venv/bin/activate
```

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Instalar o Django

```bash
pip install django
```

Caso o projeto esteja configurado para utilizar PostgreSQL, instala também o respetivo adaptador:

```bash
pip install "psycopg[binary]"
```

### 6. Aplicar as migrações

```bash
python manage.py migrate
```

### 7. Executar o servidor

```bash
python manage.py runserver
```

### 8. Aceder à aplicação

Abre o navegador e acede ao endereço:

```text
http://127.0.0.1:8000/
```

> **Nota:** A instalação pode exigir outras dependências e configurações de base de dados, dependendo da configuração atual do projeto.

## 🗄️ Base de Dados

O repositório disponibiliza dois ficheiros relacionados com a persistência de dados:

- `db.sqlite3` — base de dados SQLite.
- `livraria_backup.sql` — cópia de segurança SQL em formato PostgreSQL.

## 👨‍💻 Autor

**Manuel Mavitidi da Cunha**

GitHub: [@manuelmtidi-lab](https://github.com/manuelmtidi-lab)

## 📄 Licença

Este projeto é disponibilizado para fins de estudo e desenvolvimento. Não foi especificada uma licença de utilização.
