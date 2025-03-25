# RPG Master AI (Back-End)

**RPG Master AI** é uma aplicação desenvolvida com Django + Django REST Framework com o objetivo de **auxiliar mestres de RPG e jogadores solo** na criação de campanhas e aventuras, com suporte de **inteligência artificial (OpenAI)** para gerar histórias, enredos e interações.

## Tecnologias Utilizadas
- Python 3.12
- Django 5.x
- Django REST Framework
- PostgreSQL
- JWT Authentication (SimpleJWT)
- OpenAI API (GPT-4 / GPT-4o)
- NLTK para otimização de prompts

## Funcionalidades Principais
- Criação de personagens
- Criação e importação de campanhas por mestres
- Geração de histórias solo com IA para jogadores
- Assistente narrativo para mestres
- Armazenamento de histórico e cache de respostas da IA
- Redução automática de tokens enviados à API
- Registro de logs de uso da API
- Paginação de campanhas/personagens
- Permissões robustas para mestres e jogadores

## Estratégias de Otimização de Tokens
1. **Redução automática do prompt** com NLTK e regex.
2. **Reutilização de histórias existentes** (similaridade textual).
3. **Cache de respostas da IA por prompt + campanha + usuário.**
4. **Limitação de uso (por usuário)** — futura implementação.
5. **Controle via múltiplas chaves (load balancing)** — futura etapa.
6. **Histórias pré-geradas e armazenadas no banco.**
7. **Separação de IA + BD: IA atua como refinadora, não como geradora bruta.**

## Permissões de Acesso
- Apenas **mestres** podem importar campanhas.
- Jogadores podem jogar campanhas solo (sem interações complexas).
- Cada usuário acessa apenas suas histórias e personagens.

## Estrutura dos Principais Modelos
- `CustomUser`: mestre ou jogador
- `Campanha`: enredo criado pelo mestre
- `Personagem`: criado pelo jogador
- `SistemaRPG`: sistema base (D&D, Cthulhu...)
- `HistoricoIA`: registros das respostas da IA
- `CacheRespostaIA`: cache para evitar uso repetido de tokens
- `LogAPI`: log de ações relevantes

## Status Atual
- Back-end funcional e testado
- Integração com IA operando (com API Key válida)
- Pronto para deploy com ambiente virtual e `.env`

## Observações
- O projeto está em fase de testes e pode receber ajustes.
- Utilização real depende de chave OpenAI com saldo ativo.

## Executando o Projeto
```bash
# Crie seu ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instale os requisitos
pip install -r requirements.txt

# Realize as migrações
python manage.py makemigrations
python manage.py migrate

# Rode o servidor
python manage.py runserver
```

## Autor
Desenvolvido por Gabriel — Projeto pessoal de portfólio.
