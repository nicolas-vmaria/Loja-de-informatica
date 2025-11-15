import os
from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector
from functools import wraps
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, Produtos, Usuarios
import unicodedata

admin = Admin()

def init_app(app):
    admin.name = "Loja de Informática Admin"
    admin.template_mode = "bootstrap3"
    admin.init_app(app)

# Configurações iniciais

app = Flask(__name__)
app.secret_key = "chave_segura"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:12345678@localhost/loja_informatica"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
UPLOAD_FOLDER = 'static/img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db.init_app(app)
admin.sinit_app(app)

admin.add_view(ModelView(Produtos, db.session))
admin.add_view(ModelView(Usuarios, db.session))

# -----------------------------
# Conexão com o banco
# -----------------------------
conexao = mysql.connector.connect(
    host="localhost", port="3306", user="root", password="12345678", database="loja_informatica"
)
cursor = conexao.cursor(dictionary=True)


# -----------------------------
# Helpers / decorators
# -----------------------------
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect("/")
        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("usuario_admin") != 1:
            return redirect("/produtos")
        return f(*args, **kwargs)

    return decorated


def buscar_categorias():
    cursor.execute(
        "SELECT DISTINCT categoria FROM Produtos WHERE categoria IS NOT NULL AND categoria <> ''"
    )
    rows = cursor.fetchall()
    return [r["categoria"] for r in rows]


# -----------------------------
# Rota inicial
# -----------------------------
@app.route("/")
def index():
    if "usuario_id" in session:
        return redirect("/produtos")
    return render_template("index.html")


# -----------------------------
# Cadastro (não permite admin)
# -----------------------------
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        cursor.execute(
            "INSERT INTO Usuarios (nome, email, senha, admin) VALUES (%s, %s, %s, 0)",
            (nome, email, senha),
        )
        conexao.commit()

        usuario_id = cursor.lastrowid

        session["usuario_id"] = usuario_id
        session["usuario_nome"] = nome
        session["usuario_admin"] = 0

        return redirect("/produtos")

    return render_template("cadastro.html")


# -----------------------------
# Login
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        cursor.execute("SELECT * FROM Usuarios WHERE email=%s", (email,))
        user = cursor.fetchone()

        if not user:

            erro = "Usuário não encontrado. Cadastre-se primeiro."
            return redirect(f"/cadastro?erro={erro}")

        if user["senha"] != senha:
            erro = "Senha incorreta. Tente Novamente."
            return redirect(f"/login?erro={erro}")
    

        session["usuario_id"] = user["id"]
        session["usuario_nome"] = user["nome"]
        session["usuario_admin"] = user.get("admin", 0)

        return redirect("/produtos")

    return render_template("login.html")


# -----------------------------
# Logout
# -----------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# -----------------------------
# Listar produtos (todos)
# -----------------------------
@app.route("/produtos")
@login_required
def listar_produtos():
    cursor.execute("SELECT * FROM Produtos ORDER BY nome ASC")
    produtos = cursor.fetchall()
    categorias = buscar_categorias()
    return render_template("produtos.html", produtos=produtos, categorias=categorias)


# -----------------------------
# Filtrar por categoria
# -----------------------------
@app.route("/categoria/<categoria>")
@login_required
def produtos_por_categoria(categoria):
    cursor.execute("SELECT * FROM Produtos WHERE categoria=%s", (categoria,))
    produtos = cursor.fetchall()
    categorias = buscar_categorias()
    return render_template(
        "produtos.html",
        produtos=produtos,
        categorias=categorias,
        categoria_atual=categoria,
    )


# -----------------------------
# Finalizar compra (checkout)
# -----------------------------
@app.route("/finalizar-compra", methods=["POST"])
@login_required
def finalizar_compra():
    usuario_id = session["usuario_id"]
    pagamento = request.form.get("pagamento", "não informado")

    cursor.execute("DELETE FROM Carrinho WHERE usuario_id=%s", (usuario_id,))
    conexao.commit()

    mensagem = f"Pedido feito com sucesso! Forma de pagamento: {pagamento}. Será entregue nos próximos dias."
    return f"<div class='mensagem'>{mensagem}</div>"


# -----------------------------
# CRUD Produtos (apenas admin)
# -----------------------------
@app.route("/novo")
@admin_required
def novo_produto():
    return render_template("novo-produto.html")


def normalizar_categoria(categoria):
    mapa = {
        "perifericos": "Periféricos",
        "periferico": "Periféricos",
        "monitores": "Monitores",
        "monitor": "Monitores",
        "componentes": "Componentes",
        "componente": "Componentes",
        "cadeira": "Cadeiras",
        "cadeiras": "Cadeiras",
        "outros": "Outros",
    }
    chave = (
        unicodedata.normalize("NFKD", categoria.strip().lower())
        .encode("ASCII", "ignore")
        .decode("ASCII")
    )
    return mapa.get(chave, categoria.strip().capitalize())

def inicial_categoria(categoria):
    return categoria[0].upper()


@app.route("/salvar-produto", methods=["POST"])
@admin_required
def salvar_produto():
    nome = request.form["nome"]
    preco = float(request.form["preco"])
    categoria = normalizar_categoria(request.form.get("categoria", ""))
    estoque = int(request.form.get("estoque", 0))  

    imagem = request.files.get('imagem')
    if not imagem or not imagem.filename.endswith('.png'):
        return "Erro: Imagem inválida. Só PNG permitido."

    # ID do produto
    cursor.execute("SELECT MAX(id) AS max_id FROM Produtos")
    resultado = cursor.fetchone()
    id_produto = (resultado['max_id'] if resultado['max_id'] is not None else 0) + 1

    id_str = str(id_produto).zfill(2)

    # Ordem na categoria
    cursor.execute("SELECT COUNT(*) AS total FROM Produtos WHERE categoria = %s", (categoria,))
    resultado = cursor.fetchone()
    ordem_categoria = (resultado['total'] if resultado['total'] is not None else 0) + 1

    ordem_str = str(ordem_categoria).zfill(2)

    cat_inicial = categoria[0].upper()
    nome_arquivo = f"{id_str}{cat_inicial}{ordem_str}.png"
    caminho = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)

    # Salvar a imagem
    imagem.save(caminho)

    # Inserir no banco
    cursor.execute(
        "INSERT INTO Produtos (nome, preco, categoria, estoque, id_imagem) VALUES (%s,%s,%s,%s,%s)",
        (nome, preco, categoria, estoque, nome_arquivo),
    )
    conexao.commit()
    return redirect("/produtos")


@app.route("/api/produto/<int:id>")
@admin_required
def api_produto(id):
    cursor.execute("SELECT * FROM Produtos WHERE id=%s", (id,))
    produto = cursor.fetchone()
    if produto:
        return jsonify(produto)
    
    else:
        return jsonify({"erro": "Produto não encontrado"}), 404


@app.route("/api/produto/<int:id>", methods=["POST"])
@admin_required
def api_atualizar_produto(id):
    nome = request.form["nome"]
    preco = float(request.form["preco"])
    categoria = request.form.get("categoria", "")
    estoque = int(request.form.get("estoque", 0)) 
    categoria = normalizar_categoria(categoria)
    cursor.execute(
        "UPDATE Produtos SET nome=%s, preco=%s, categoria=%s, estoque=%s WHERE id=%s",
        (nome, preco, categoria, estoque, id),
    )
    conexao.commit()
    
    return jsonify({"mensagem": "Produto atualizado com sucesso!"})


@app.route("/delete/<int:id>")
@admin_required
def delete(id):
    cursor.execute("DELETE FROM Produtos WHERE id=%s", (id,))
    conexao.commit()
    return redirect("/produtos")


# -----------------------------
# Carrinho
# -----------------------------
@app.route("/colocar/<int:produto_id>")
@login_required
def colocar_no_carrinho(produto_id):
    usuario_id = session["usuario_id"]

    cursor.execute("SELECT * FROM Produtos WHERE id=%s", (produto_id,))
    produto = cursor.fetchone()
    if produto['estoque'] <= 0:
        return redirect("/produtos")
        

    cursor.execute(
        "SELECT * FROM Carrinho WHERE produto_id=%s AND usuario_id=%s",
        (produto_id, usuario_id),
    )
    item = cursor.fetchone()
    if item:
        cursor.execute(
            "UPDATE Carrinho SET quantidade = quantidade + 1 WHERE id=%s", (item["id"],)
        )
    else:
        cursor.execute(
            "INSERT INTO Carrinho (produto_id, quantidade, usuario_id) VALUES (%s,1,%s)",
            (produto_id, usuario_id),
        )

    cursor.execute("UPDATE Produtos SET estoque = estoque - 1 WHERE id=%s", (produto_id,))
    conexao.commit()
    return redirect("/produtos")


@app.route("/carrinho")
@login_required
def carrinho():
    usuario_id = session["usuario_id"]
    cursor.execute(
        """
        SELECT c.id, p.nome, p.preco, c.quantidade
        FROM Carrinho c
        JOIN Produtos p ON c.produto_id = p.id
        WHERE c.usuario_id = %s
    """,
        (usuario_id,),
    )
    carrinho = cursor.fetchall()
    total = sum(item["preco"] * item["quantidade"] for item in carrinho)
    return render_template("carrinho.html", carrinho=carrinho, total=total)


@app.route("/carrinho/deletar/<int:id>")
@login_required
def deletar_carrinho(id):
    cursor.execute("SELECT produto_id, quantidade FROM Carrinho WHERE id=%s", (id,))
    item = cursor.fetchone()

    if item:
        produto_id = item["produto_id"]
        quantidade = item["quantidade"]

        cursor.execute(
            "UPDATE Produtos SET estoque = estoque + %s WHERE id=%s",
            (quantidade, produto_id),
        )

    cursor.execute("DELETE FROM Carrinho WHERE id=%s", (id,))
    conexao.commit()
    return redirect("/carrinho")


# -----------------------------
# Rodar app
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
