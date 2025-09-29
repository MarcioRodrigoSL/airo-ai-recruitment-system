from flask import Flask, request, jsonify, session
from flask_cors import CORS
from radon.complexity import cc_visit
from radon.visitors import ComplexityVisitor
import datetime
import sqlite3
import config_manager 
from functools import wraps

app = Flask(__name__)
app.secret_key = 'uma-chave-secreta-muito-segura-e-dificil-de-adivinhar'
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
DATABASE_FILE = 'backend/airo.db'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'erro': 'Acesso não autorizado. Por favor, faça o login.'}), 401
        return f(*args, **kwargs)
    return decorated_function

def inicializar_banco():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, profissao TEXT, nivel TEXT,
            nota_curriculo INTEGER, nota_codigo INTEGER, nota_final INTEGER, data_analise TEXT,
            vaga_id INTEGER, FOREIGN KEY (vaga_id) REFERENCES vagas (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vagas (
            id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT NOT NULL, descricao TEXT,
            requisitos TEXT, status TEXT DEFAULT 'Aberta', data_criacao TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    username = dados.get('username')
    password = dados.get('password')
    if username == 'recrutador' and password == '1234':
        session['user_id'] = 1
        session['username'] = 'recrutador'
        return jsonify({'mensagem': 'Login realizado com sucesso!'})
    return jsonify({'erro': 'Usuário ou senha inválidos.'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'mensagem': 'Logout realizado com sucesso!'})

@app.route('/status', methods=['GET'])
@login_required
def status():
    return jsonify({'status': 'logado', 'username': session.get('username')})

@app.route('/analisar', methods=['POST'])
@login_required
def analisar_candidato():
    PALAVRAS_CHAVE = config_manager.carregar_keywords()
    dados = request.get_json()
    nome_candidato = dados.get('nome', 'Candidato Anônimo')
    curriculo = dados.get('curriculo', '')
    codigo = dados.get('codigo', '')
    profissao = dados.get('profissao', 'dev_backend')
    nivel = dados.get('nivel', 'pleno')
    vaga_id = dados.get('vaga_id')
    nota_curriculo = 0
    palavras_encontradas = []
    texto_curriculo = curriculo.lower()
    keywords_da_profissao = PALAVRAS_CHAVE.get(profissao, {})
    for palavra, pontos in keywords_da_profissao.items():
        if palavra in texto_curriculo:
            nota_curriculo += pontos
            palavras_encontradas.append(palavra)
    if nivel == 'junior': nota_curriculo = int(nota_curriculo * 1.25)
    elif nivel == 'senior' or nivel == 'especialista': nota_curriculo = int(nota_curriculo * 0.90)
    if nota_curriculo > 100: nota_curriculo = 100
    nota_codigo = 0
    detalhes_codigo = []
    if codigo.strip():
        try:
            visitor = ComplexityVisitor.from_code(codigo)
            complexidade_total = 0
            num_funcoes = 0
            for func in visitor.functions:
                complexidade_total += func.complexity
                num_funcoes += 1
                detalhes_codigo.append({'nome': func.name, 'complexidade': func.complexity})
            complexidade_media = complexidade_total / num_funcoes if num_funcoes > 0 else 0
            if complexidade_media <= 5: nota_codigo = 100
            elif complexidade_media <= 10: nota_codigo = 85
            elif complexidade_media <= 15: nota_codigo = 60
            elif complexidade_media <= 20: nota_codigo = 40
            else: nota_codigo = 20
        except Exception:
            nota_codigo = 10
            detalhes_codigo.append({'nome': 'Erro de Sintaxe', 'complexidade': 'N/A'})
    nota_final = int((nota_curriculo * 0.6) + (nota_codigo * 0.4))
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO candidatos (nome, profissao, nivel, nota_curriculo, nota_codigo, nota_final, data_analise, vaga_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nome_candidato, dict(app.config['PROFissoes']).get(profissao, profissao), nivel.capitalize(), nota_curriculo, nota_codigo, nota_final, datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), vaga_id))
    conn.commit()
    conn.close()
    return jsonify({'nota_curriculo': nota_curriculo, 'nota_codigo': nota_codigo, 'palavras_encontradas': palavras_encontradas, 'detalhes_codigo': detalhes_codigo})

@app.route('/ranking', methods=['GET'])
@login_required
def get_ranking():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT c.*, v.titulo as vaga_titulo FROM candidatos c LEFT JOIN vagas v ON c.vaga_id = v.id ORDER BY c.nota_final DESC''')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/vagas', methods=['POST'])
@login_required
def cadastrar_vaga():
    dados = request.get_json()
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO vagas (titulo, descricao, requisitos, data_criacao) VALUES (?, ?, ?, ?)', (dados['titulo'], dados['descricao'], dados['requisitos'], datetime.datetime.now().strftime("%d/%m/%Y %H:%M")))
    conn.commit()
    id_nova_vaga = cursor.lastrowid
    conn.close()
    return jsonify({'id': id_nova_vaga, 'mensagem': f'Vaga "{dados["titulo"]}" cadastrada com sucesso!'}), 201

@app.route('/vagas', methods=['GET'])
@login_required
def get_vagas():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vagas ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/vagas/abertas', methods=['GET'])
@login_required
def get_vagas_abertas():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vagas WHERE status = 'Aberta' ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/vagas/<int:id_vaga>', methods=['DELETE'])
@login_required
def excluir_vaga(id_vaga):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vagas WHERE id = ?", (id_vaga,))
    conn.commit()
    mensagem = f'Vaga com ID {id_vaga} foi excluída.' if cursor.rowcount > 0 else f'Nenhuma vaga encontrada com o ID {id_vaga}.'
    conn.close()
    return jsonify({'mensagem': mensagem})

@app.route('/vagas/<int:id_vaga>', methods=['GET'])
@login_required
def get_vaga_por_id(id_vaga):
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vagas WHERE id = ?", (id_vaga,))
    vaga = cursor.fetchone()
    conn.close()
    if vaga:
        return jsonify(dict(vaga))
    return jsonify({'erro': 'Vaga não encontrada'}), 404

@app.route('/vagas/<int:id_vaga>', methods=['PUT'])
@login_required
def atualizar_vaga(id_vaga):
    dados = request.get_json()
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('UPDATE vagas SET titulo = ?, descricao = ?, requisitos = ?, status = ? WHERE id = ?', (dados['titulo'], dados['descricao'], dados['requisitos'], dados['status'], id_vaga))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Vaga atualizada com sucesso!'})

@app.route('/configuracoes', methods=['GET'])
@login_required
def get_configuracoes():
    config_completa = config_manager.carregar_configuracoes_completas()
    return jsonify(config_completa)

@app.route('/configuracoes', methods=['POST'])
@login_required
def salvar_configuracoes():
    novas_keywords = request.get_json()
    config_manager.salvar_keywords(novas_keywords)
    return jsonify({'mensagem': 'Configurações salvas com sucesso!'})

@app.route('/configuracoes/padrao', methods=['GET'])
@login_required
def get_configuracoes_padrao():
    return jsonify({
        'keywords': config_manager.DEFAULT_KEYWORDS,
        'descriptions': config_manager.DEFAULT_DESCRIPTIONS
    })

if __name__ == '__main__':
    app.config['PROFissoes'] = {
        'dev_backend': 'Dev. Backend', 'dev_frontend': 'Dev. Frontend', 'dev_fullstack': 'Dev. Full-Stack',
        'dba': 'DBA', 'data_scientist': 'Cientista de Dados', 'data_engineer': 'Engenheiro de Dados',
        'software_engineer': 'Eng. de Software', 'devops': 'Eng. DevOps', 'qa_analyst': 'Analista de QA'
    }
    inicializar_banco()
    config_manager.carregar_keywords()
    app.run(debug=True)
