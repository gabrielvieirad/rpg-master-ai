# 🧙‍♂️ RPG Master AI

🚀 **RPG Master AI** é um assistente para mestres de RPG que auxilia na criação e improvisação de campanhas, fornecendo roteiros, NPCs, eventos e adaptações dinâmicas baseadas nas interações dos jogadores.

## 📌 **Sobre o Projeto**
O **RPG Master AI** foi desenvolvido para ajudar mestres a narrar campanhas de RPG de mesa, utilizando a **API da OpenAI** para gerar histórias dinâmicas e improvisar eventos. A IA complementa a criatividade do mestre, oferecendo descrições, desafios e personagens para enriquecer a experiência dos jogadores.

> **⚠️ O projeto está em fase de testes e desenvolvimento. Algumas funcionalidades podem mudar até o lançamento oficial.**

---

## 📂 **Estrutura do Projeto**
```sh
projeto_django/
│── api/                     # Aplicação principal da API
│   ├── migrations/           # Migrations do banco de dados
│   ├── models.py             # Modelos do banco de dados
│   ├── serializers.py        # Serializadores da API
│   ├── views.py              # Lógica das Views da API
│   ├── permissions.py        # Configuração de permissões e acessos
│   ├── urls.py               # Rotas/endpoints da API
│   ├── services.py           # Serviços auxiliares, como geração de história
│── backend/                  # Configuração principal do Django
│   ├── settings.py           # Configurações do projeto Django
│   ├── urls.py               # Rotas principais
│── venv/                     # Ambiente virtual do projeto
│── manage.py                 # Arquivo de gerenciamento do Django
│── requirements.txt          # Dependências do projeto
│── README.md                 # Documentação do projeto
---
```
## 🔧 Como Instalar e Rodar o Projeto  

### **1️⃣ Clonar o Repositório**  
```sh
git clone https://github.com/seu-usuario/rpg-master-ai.git
cd rpg-master-ai

---
```
### **2️⃣ Criar e Ativar um Ambiente Virtual** 
```sh
python -m venv venv
venv\Scripts\activate  # No Windows
source venv/bin/activate  # No Mac/Linux
```
---
### **3️⃣ Instalar Dependências** 
pip install -r requirements.txt
---
```sh
OPENAI_API_KEY=SUA_CHAVE_DA_OPENAI
SECRET_KEY=SUA_SECRET_KEY_DJANGO
DATABASE_URL=postgres://usuario:senha@localhost:5432/rpg_master_ai
---
```
### **5️⃣ Rodar as Migrações do Banco de Dados**
```sh
python manage.py makemigrations
python manage.py migrate
---
```
### **6️⃣ Criar um Superusuário (para acessar o admin do Django)**
```sh
python manage.py createsuperuser
```
### **7️⃣ Rodar o Servidor**
```sh
python manage.py runserver
---
```
---
## **🛡️ Autenticação & Permissões**
- O sistema utiliza JWT Authentication para autenticação dos usuários.
- Mestres podem criar e gerenciar campanhas.
- Jogadores podem apenas acessar campanhas solo e visualizar conteúdos públicos.
---
## **🚀 Principais Funcionalidades**
- ✅ Criação de Campanhas: Mestres podem criar roteiros baseados em sistemas de RPG.
- ✅ Assistente de IA: A IA auxilia na construção de histórias e improvisação.
- ✅ Histórico de Geração: Todas as interações com a IA são armazenadas.
- ✅ API Segura: Com autenticação JWT e permissões ajustáveis.
- ✅ Sistema de Logs: Para rastrear ações dos usuários.
---

## **🛠️ Como Contribuir?**
### Se quiser contribuir com o projeto, siga estes passos:
- Faça um fork do repositório
- Crie uma branch com sua feature (git checkout -b minha-feature)
- Faça commit das mudanças (git commit -m 'Adicionando uma nova funcionalidade')
- Faça push para a branch (git push origin minha-feature)
- Abra um Pull Request
---
## **📌 Status do Projeto**
🟡 Fase de testes: A API está finalizada, mas o projeto ainda passa por otimizações e ajustes antes do lançamento oficial.

