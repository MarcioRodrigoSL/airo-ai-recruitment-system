import json

CONFIG_FILE = 'backend/keywords_config.json'

DEFAULT_DESCRIPTIONS = {
    'dev_backend': 'Focado na lógica do servidor, bancos de dados e APIs. Constrói o que acontece "por trás das cortinas".',
    'dev_frontend': 'Focado na interface do usuário e na experiência visual. Constrói o que o usuário vê e interage no navegador.',
    'dev_fullstack': 'Profissional versátil que atua tanto no backend quanto no frontend, conectando as duas pontas.',
    'dba': 'Especialista em gerenciar, otimizar e garantir a segurança e a performance dos bancos de dados.',
    'data_scientist': 'Usa dados para encontrar padrões, criar modelos preditivos e extrair insights de negócio através de estatística e machine learning.',
    'data_engineer': 'Constrói e mantém os "encanamentos" de dados (pipelines, ETLs) que coletam e preparam grandes volumes de dados para análise.',
    'software_engineer': 'Focado nos fundamentos da engenharia de software, como arquitetura, algoritmos e qualidade de código, para construir sistemas robustos.',
    'devops': 'Une desenvolvimento (Dev) e operações (Ops), focando em automação, infraestrutura como código e pipelines de CI/CD.',
    'qa_analyst': 'Garante a qualidade do software através da criação e execução de testes, sejam eles manuais ou automatizados.'
}

DEFAULT_KEYWORDS = {
    'dev_backend': { 'python': 10, 'java': 10, 'node.js': 10, 'c#': 10, '.net': 10, 'php': 8, 'go': 9, 'ruby': 8, 'api': 8, 'rest': 8, 'graphql': 9, 'microserviços': 12, 'sql': 7, 'postgresql': 7, 'mongodb': 7, 'docker': 8, 'kubernetes': 9, 'aws': 9, 'azure': 9, 'gcp': 9, 'ci/cd': 8 },
    'dev_frontend': { 'javascript': 10, 'typescript': 10, 'react': 12, 'angular': 12, 'vue': 12, 'html': 8, 'css': 8, 'sass': 8, 'next.js': 10, 'jest': 7, 'responsivo': 9, 'acessibilidade': 9 },
    'dev_fullstack': { 'python': 7, 'node.js': 8, 'javascript': 7, 'typescript': 8, 'react': 9, 'angular': 9, 'sql': 5, 'api': 6, 'docker': 6, 'aws': 6 },
    'dba': { 'sql': 12, 'oracle': 12, 'sql server': 12, 'mysql': 10, 'postgresql': 10, 'performance tuning': 15, 'backup': 10, 'modelagem de dados': 12, 'nosql': 8 },
    'data_scientist': { 'python': 12, 'r': 12, 'machine learning': 15, 'deep learning': 12, 'tensorflow': 10, 'pytorch': 10, 'scikit-learn': 12, 'pandas': 10, 'estatística': 12, 'sql': 8 },
    'data_engineer': { 'python': 10, 'sql': 12, 'etl': 15, 'apache spark': 12, 'apache hadoop': 10, 'apache kafka': 10, 'data warehouse': 12, 'aws': 9, 'gcp': 9, 'airflow': 10 },
    'software_engineer': { 'algoritmos': 12, 'estrutura de dados': 12, 'design patterns': 12, 'arquitetura de software': 15, 'solid': 10, 'clean code': 10, 'java': 9, 'python': 9, 'c++': 9, 'sistemas distribuídos': 10 },
    'devops': { 'ci/cd': 15, 'docker': 12, 'kubernetes': 12, 'terraform': 12, 'iac': 12, 'aws': 10, 'azure': 10, 'gcp': 10, 'prometheus': 8, 'grafana': 8, 'linux': 9 },
    'qa_analyst': { 'testes automatizados': 12, 'selenium': 10, 'cypress': 10, 'jest': 8, 'plano de testes': 10, 'casos de teste': 10, 'bdd': 9, 'teste de api': 9, 'postman': 8, 'sql': 7 }
}

def carregar_configuracoes_completas():
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            keywords = json.load(f)
    except FileNotFoundError:
        salvar_keywords(DEFAULT_KEYWORDS)
        keywords = DEFAULT_KEYWORDS
    
    return {
        'keywords': keywords,
        'descriptions': DEFAULT_DESCRIPTIONS
    }

def carregar_keywords():
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        salvar_keywords(DEFAULT_KEYWORDS)
        return DEFAULT_KEYWORDS

def salvar_keywords(keywords_data):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(keywords_data, f, indent=4, ensure_ascii=False)
