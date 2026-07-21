from flask import Flask, render_template, jsonify, request
from datetime import date
from urllib.parse import unquote
from SistemaAgendamentos import Sistema

app = Flask(__name__)

# Inicializa o sistema de agendamentos na memória do servidor
sistema = Sistema()

@app.route('/')
def index():
    # Renderiza a página principal
    return render_template('index.html')

@app.route('/api/tarefas', methods=['GET'])
def listar_tarefas():
    # Simplificado usando List Comprehension
    resultado = [{
        'nome': t.nome,
        'categoria': t.categoria,
        'prioridade': t.prioridade,
        'data': t.data.strftime('%Y-%m-%d')
    } for t in sistema.listarTarefa()]

    return jsonify(resultado)

@app.route('/api/tarefas', methods=['POST'])
def adicionar_tarefa():
    dados = request.json
    nome = dados.get('nome')
    data_html = dados.get('data')  # Formato do HTML: YYYY-MM-DD
    prioridade = int(dados.get('prioridade', 0))

    if not nome or not data_html:
        return jsonify({'erro': 'Nome e data são obrigatórios!'}), 400

    # Inversão limpa de YYYY-MM-DD para DD/MM/YYYY em uma única linha
    data_texto = '/'.join(reversed(data_html.split('-')))

    # Define 'Outro' caso a categoria venha vazia ou apenas com espaços
    categoria = dados.get('categoria', '').strip() or 'Outro'

    mensagem = sistema.adicionarTarefa(nome, data_texto, prioridade, categoria)
    return jsonify({'mensagem': mensagem})

@app.route('/api/tarefas/<path:nome>', methods=['DELETE'])
def remover_tarefa(nome):
    nome_decodificado = unquote(nome)
    mensagem = sistema.removerTarefa(nome_decodificado)
    return jsonify(mensagem)

@app.route('/api/tarefas/urgentes', methods=['GET'])
def ver_urgentes():
    return jsonify(sistema.verUrgencia())

@app.route('/api/resumo', methods=['GET'])
def obter_resumo():
    hoje = date.today()
    tarefas = sistema.tarefas
    total = len(tarefas)

    # Cálculos otimizados para o Dashboard
    atrasadas = sum(1 for t in tarefas if t.data < hoje)
    no_prazo_hoje = sum(1 for t in tarefas if t.data == hoje)
    futuras = sum(1 for t in tarefas if t.data > hoje)
    urgentes = sum(1 for t in tarefas if t.prioridade in [1, 2])

    # Redução do If/Else longo usando um dicionário dinâmico
    categorias = {'escola': 0, 'trabalho': 0, 'pessoal': 0, 'outro': 0}

    for t in tarefas:
        cat_lower = t.categoria.lower().strip()
        if cat_lower in categorias:
            categorias[cat_lower] += 1
        else:
            categorias['outro'] += 1

    taxa_atraso = (atrasadas / total * 100) if total > 0 else 0

    return jsonify({
        'total': total,
        'atrasadas': atrasadas,
        'hoje': no_prazo_hoje,
        'futuras': futuras,
        'urgentes': urgentes,
        'taxa_atraso': round(taxa_atraso, 2),
        'categorias': categorias
    })

@app.route('/api/salvar', methods=['POST'])
def salvar_csv():
    # Remoção do bloco condicional redundante do "locals()"
    return jsonify({'mensagem': sistema.salvarArquivo()})

if __name__ == '__main__':
    app.run(debug=True, port=9090)