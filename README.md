# AIRO.AI - Assistente de Recrutamento com Inteligência Artificial

![Logo do Projeto](frontend/images/logo.png)

## 📖 Sobre o Projeto

AIRO.AI é uma aplicação web full-stack desenvolvida para otimizar e automatizar o processo de triagem de candidatos. A ferramenta utiliza análise de complexidade de código e processamento de texto para pontuar currículos e desafios técnicos, fornecendo aos recrutadores uma classificação clara e baseada em dados para identificar os talentos mais promissores.

Este projeto foi construído como uma demonstração de habilidades em desenvolvimento de software ponta a ponta, desde o backend e banco de dados até o frontend e a experiência do usuário.

---

## ✨ Funcionalidades Principais

*   **Autenticação Segura:** Sistema de login e logout para recrutadores com gerenciamento de sessão.
*   **Análise de Currículo:** Pontuação baseada em palavras-chave customizáveis por área de atuação.
*   **Análise de Código:** Avaliação da complexidade ciclomática de trechos de código em Python.
*   **Dashboard Interativo:** Painel central para realizar análises e visualizar resultados imediatos.
*   **Ranking de Candidatos:** Tabela classificatória com filtros dinâmicos por profissão.
*   **Gerenciamento de Vagas (CRUD):** Funcionalidade completa para Criar, Ler, Atualizar e Excluir vagas.
*   **Configuração da IA:** Interface para que o recrutador possa ajustar os pesos das palavras-chave, personalizando o critério de análise.

---

## 🛠️ Tecnologias Utilizadas

*   **Backend:**
    *   **Python 3**
    *   **Flask:** Micro-framework para a construção da API RESTful.
    *   **SQLite 3:** Banco de dados relacional para armazenamento de vagas e candidatos.
    *   **Radon:** Biblioteca para análise de complexidade de código.
*   **Frontend:**
    *   **HTML5**
    *   **CSS3:** Estilização moderna e responsiva.
    *   **JavaScript (Vanilla):** Manipulação do DOM e comunicação com a API (Fetch API).
*   **Ambiente:**
    *   **WSL (Ubuntu):** Desenvolvimento em um ambiente que simula um servidor Linux.
    *   **Git & GitHub:** Controle de versão e hospedagem do código.

---

## 🚀 Como Executar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone [URL_DO_SEU_REPOSITORIO_AQUI]
    cd airo-ai-2
    ```

2.  **Crie e ative o ambiente virtual:**
    ```bash
    python3 -m venv backend/venv
    source backend/venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install Flask Flask-Cors radon
    ```

4.  **Inicie os servidores:**
    *   Abra dois terminais.
    *   No **Terminal 1**, inicie o backend: `./start.sh`
    *   No **Terminal 2**, inicie o frontend: `cd frontend && python3 -m http.server 8000`

5.  **Acesse a aplicação:**
    *   Abra seu navegador e acesse `http://127.0.0.1:8000/login.html`.
    *   Use as credenciais: `usuário: recrutador`, `senha: 1234`.

---

## 👨‍💻 Desenvolvedor

*   **Desenvolvido por:** [Márcio Rodrigo Souza Lima](https://www.linkedin.com/in/marcio-lima-b1105627b/ )
*   **GitHub:** [MarcioRodrigoSL](https://github.com/MarcioRodrigoSL )


