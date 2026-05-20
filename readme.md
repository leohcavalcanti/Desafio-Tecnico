# 📚 Smart Planner Pedagógico

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)
![Gemini AI](https://img.shields.io/badge/AI-Google_Gemini-orange?logo=google&logoColor=white)

Este é um sistema de gerenciamento de planos de aula desenvolvido para apoiar o planejamento pedagógico. O grande diferencial da plataforma é a integração com Inteligência Artificial (**Smart Assist**), que atua como um assistente para o professor, sugerindo conteúdos complementares e tags para enriquecer as aulas.

---

## 🎥 Apresentação do Projeto
> **Assista ao vídeo de apresentação:** https://youtu.be/FvV4wmzQi3Q

No vídeo acima, apresento as escolhas técnicas, a arquitetura do projeto e a demonstração do sistema (incluindo o uso do Docker e da IA) rodando em tempo real.

---

## ✨ Funcionalidades

- **CRUD Completo:** Listagem (com paginação e filtros dinâmicos), cadastro, edição e exclusão de planos de aula.
- **Smart Assist (IA):** Ao informar Título, Disciplina e Ementa, o sistema consome a API do Google Gemini para gerar automaticamente Conteúdos Complementares, Recursos de Apoio e Tags recomendadas.
- **Single Page Application (SPA):** Interface fluida usando HTML, CSS e Vanilla JavaScript, com estados de *loading* para melhorar a experiência do usuário durante o processamento da IA.
- **Observabilidade:** Logs estruturados no console exibindo o tempo de latência (em segundos) e o consumo total de tokens em cada chamada para a IA.
- **Health Check:** Endpoint nativo (`/health`) para validação de integridade da API.

---

## 🏗️ Arquitetura e Padrões de Projeto

O backend foi estruturado utilizando o padrão de **Arquitetura em Camadas (Layered Architecture)** para garantir separação de responsabilidades, facilidade de manutenção e escalabilidade:

1. **Controllers (`/controllers`):** Recebem as requisições HTTP do frontend, validam a presença dos campos obrigatórios e delegam o trabalho pesado.
2. **Services (`/services`):** O "cérebro" da aplicação. Contêm todas as regras de negócio, manipulação de dados, logs de observabilidade e a integração isolada com a API do Gemini.
3. **Repositories (`/repositories`):** Camada exclusiva para comunicação com o Banco de Dados via SQLAlchemy.

---

## 🚀 Como Executar o Projeto (Localmente)

O ambiente foi totalmente containerizado. Para rodar a aplicação e o banco de dados simultaneamente com um único comando, siga os passos abaixo:

### 1. Pré-requisitos
- [Git](https://git-scm.com/) instalado.
- [Docker](https://www.docker.com/) e Docker Compose instalados e rodando na sua máquina.
- Uma chave de API válida do Google AI Studio (Gemini).

### 2. Clone o Repositório
- git clone [https://github.com/leohcavalcanti/Desafio-Tecnico.git](https://github.com/leohcavalcanti/Desafio-Tecnico.git)

### 3. Configuração das Variáveis de Ambiente
altere as informações do arquivo chamado `.env.example` na raiz do projeto

```bash
# Configurações do Banco de Dados PostgreSQL
DB_HOST=database
DB_PORT=5432
DB_NAME=plano_aula_db
DB_USER=postgres
DB_PASSWORD=sua_senha_segura

# Chave da API de IA (Google Gemini)
GEMINI_API_KEY=sua_chave_api_aqui
```

### 4. Subindo os Containers
Com o Docker aberto, execute o comando abaixo na raiz do projeto:
```docker compose up --build -d```

### 5. Acessando o Sistema
Após o terminal indicar que os containers estão rodando, acesse no seu navegador:
http://localhost:5000

