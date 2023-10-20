from flask import Flask, request, jsonify, g
import sqlite3

# Conectar ao banco de dados (certifique-se de que o arquivo do banco de dados exista)
db = sqlite3.connect('database.db')

# Criar a tabela "users" se ela não existir
db.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER
    )
''')

# Commit para salvar as alterações
db.commit()

# Fechar a conexão com o banco de dados
db.close()

app = Flask(__name__)
app.config['DATABASE'] = 'database.db'  # Nome do arquivo do banco de dados SQLite

# Função para conectar ao banco de dados
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

# Função para fechar a conexão com o banco de dados no final da solicitação
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    if 'nome' in data and 'idade' in data:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO users (nome, idade) VALUES (?, ?)', (data['nome'], data['idade']))
        db.commit()
        return jsonify({'message': 'Usuário adicionado com sucesso'}), 201
    else:
        return jsonify({'message': 'Requisição inválida'}), 400

@app.route('/users', methods=['GET'])
def get_users():
    db = get_db()
    cursor = db.execute('SELECT nome, idade FROM users')
    users = cursor.fetchall()
    return jsonify([dict(user) for user in users])

if __name__ == '__main__':
    app.run()
