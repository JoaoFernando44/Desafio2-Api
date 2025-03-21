from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def conectar_bd():
    return sqlite3.connect('database.db')

def criar_tabela():
    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS LIVROS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            categoria TEXT NOT NULL,
            autor TEXT NOT NULL,
            imagem_url TEXT NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

criar_tabela()

@app.route('/')
def pagina_inicial():
    return "Bem-vindo à API de livros! Sinta-se à vontade para cadastrar e listar livros."

@app.route('/doar', methods=['POST', 'GET'])

def cadastrar_livro():
    dados = request.get_json()
    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute('''
        INSERT INTO LIVROS (titulo, categoria, autor, imagem_url)
        VALUES (?, ?, ?, ?)
    ''', (dados['titulo'], dados['categoria'], dados['autor'], dados['imagem_url']))
    conexao.commit()
    conexao.close()
    return jsonify({'mensagem': 'Livro cadastrado com sucesso!'}), 201

@app.route('/livros', methods=['GET'])
def listar_livros():
    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM LIVROS')
    livros = cursor.fetchall()
    conexao.close()
    resultado = []
    for livro in livros:
        resultado.append({
            'id': livro[0],
            'titulo': livro[1],
            'categoria': livro[2],
            'autor': livro[3],
            'imagem_url': livro[4]
        })
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
