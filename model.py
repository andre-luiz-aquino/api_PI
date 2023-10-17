from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


def criar_codigo(nome, codigos):
    conn = sqlite3.connect('mqtt.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO codigos (nome, codigos) VALUES (?, ?)', (nome, codigos))
    conn.commit()
    conn.close()


def buscar_todos_codigos():
    conn = sqlite3.connect('mqtt.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM codigos')
    users = cursor.fetchall()
    conn.close()
    return users
def buscar_todos_horarios():
    conn = sqlite3.connect('mqtt.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM horarios')
    users = cursor.fetchall()
    conn.close()
    return users


def buscar_codigo_id(id):
    conn = sqlite3.connect('mqtt.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM codigos WHERE id = ?', (id,))
    cod = cursor.fetchone()
    conn.close()
    return cod


def redefenir(id, nome, codigos):
    conn = sqlite3.connect('mqtt.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE codigos SET name = ?, codigo = ? WHERE id = ?', (nome, codigos, id))
    conn.commit()
    conn.close()

def deletar_codigo(id):
    conn = sqlite3.connect('mqtt.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM codigos WHERE id = ?', (id,))
    conn.commit()
    conn.close()

# Rotas da API

@app.route('/cod', methods=['GET'])
def buscar_cod():
    cod = buscar_todos_codigos()
    return jsonify({'cod': cod})

@app.route('/hor', methods=['GET'])
def buscar_hor():
    cod = buscar_todos_horarios()
    return jsonify({'cod': cod})

@app.route('/cod', methods=['POST'])
def criar_codigo_rota():
    data = request.get_json()
    nome = data.get('nome')
    codigos = data.get('codigos')
    criar_codigo(nome, codigos)
    return jsonify({'menssagem': 'codigo criado com sucesso'})

@app.route('/cod/<int:id>', methods=['GET'])
def get_user_route(id):
    cod = buscar_codigo_id(id)
    if cod:
        return jsonify({'cod': cod})
    return jsonify({'menssagem': 'codigo nao encontrado'}), 404

@app.route('/cod/<int:id>', methods=['PUT'])
def redefinicao(id):
    data = request.get_json()
    nome = data.get('nome')
    codigos = data.get('codigos')
    redefenir(id, nome, codigos)
    return jsonify({'menssagem': 'codigo redefinido'})

@app.route('/cod/<int:id>', methods=['DELETE'])
def delete_user_route(id):
    deletar_codigo(id)
    return jsonify({'menssagem': 'codigo deletado'})

if __name__ == '__main__':
    # Criar a tabela se não existir
    conn = sqlite3.connect('mqtt.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS codigos (
            id INTEGER PRIMARY KEY,
            nome TEXT,
            codigos TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS horarios (
            id INTEGER PRIMARY KEY,
            dia_semana TEXT,
            hora_inicio TIMESTAMP,
            hora_fim TIMESTAMP,
            Disciplina VARCHAR,
            sala TEXT
        )
    ''')
    conn.close()

    app.run(debug=True)
