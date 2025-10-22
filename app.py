from flask import Flask, render_template, request, redirect, session
import mysql.connector
from functools import wraps

app = Flask(__name__)
app.secret_key = "chave_segura"

# -----------------------------
# Conexão com o banco
# -----------------------------
conexao = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="12345678",
    database="loja_informatica"
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
    cursor.execute("SELECT DISTINCT categoria FROM Produtos WHERE categoria IS NOT NULL AND categoria <> ''")
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
            (nome, email, senha)
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
@app.route("/login", methods=["GET","POST"])
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
           
            return render_template("login.html", erro="Senha incorreta.")

        
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
    cursor.execute("SELECT * FROM Produtos")
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
    return render_template("produtos.html", produtos=produtos, categorias=categorias, categoria_atual=categoria)

# -----------------------------
# Finalizar compra (checkout)
# -----------------------------
@app.route("/finalizar-compra", methods=["POST"])
@login_required
def finalizar_compra():
    usuario_id = session["usuario_id"]
    pagamento = request.form.get("pagamento", "não informado")

    # Limpar carrinho do usuário
    cursor.execute("DELETE FROM Carrinho WHERE usuario_id=%s", (usuario_id,))
    conexao.commit()

    mensagem = f"Pedido feito com sucesso! Forma de pagamento: {pagamento}. Será entregue nos próximos dias."
    return render_template("pedido_feito.html", mensagem=mensagem)

# -----------------------------
# CRUD Produtos (apenas admin)
# -----------------------------
@app.route("/novo")
@admin_required
def novo_produto():
    return render_template("novo-produto.html")

@app.route("/salvar-produto", methods=["POST"])
@admin_required
def salvar_produto():
    nome = request.form["nome"]
    preco = request.form["preco"]
    categoria = request.form.get("categoria", "")
    cursor.execute("INSERT INTO Produtos (nome, preco, categoria) VALUES (%s,%s,%s)", (nome, preco, categoria))
    conexao.commit()
    return redirect("/produtos")

@app.route("/editar/<int:id>")
@admin_required
def editar_produto(id):
    cursor.execute("SELECT * FROM Produtos WHERE id=%s", (id,))
    produto = cursor.fetchone()
    return render_template("editar-produto.html", produto=produto)

@app.route("/atualizar-produto/<int:id>", methods=["POST"])
@admin_required
def atualizar_produto(id):
    nome = request.form["nome"]
    preco = request.form["preco"]
    categoria = request.form.get("categoria", "")
    cursor.execute("UPDATE Produtos SET nome=%s, preco=%s, categoria=%s WHERE id=%s", (nome, preco, categoria, id))
    conexao.commit()
    return redirect("/produtos")

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
    cursor.execute("SELECT * FROM Carrinho WHERE produto_id=%s AND usuario_id=%s", (produto_id, usuario_id))
    item = cursor.fetchone()
    if item:
        cursor.execute("UPDATE Carrinho SET quantidade = quantidade + 1 WHERE id=%s", (item["id"],))
    else:
        cursor.execute("INSERT INTO Carrinho (produto_id, quantidade, usuario_id) VALUES (%s,1,%s)", (produto_id, usuario_id))
    conexao.commit()
    return redirect("/produtos")

@app.route("/carrinho")
@login_required
def carrinho():
    usuario_id = session["usuario_id"]
    cursor.execute("""
        SELECT c.id, p.nome, p.preco, c.quantidade
        FROM Carrinho c
        JOIN Produtos p ON c.produto_id = p.id
        WHERE c.usuario_id = %s
    """, (usuario_id,))
    carrinho = cursor.fetchall()
    total = sum(item["preco"]*item["quantidade"] for item in carrinho)
    return render_template("carrinho.html", carrinho=carrinho, total=total)

@app.route("/carrinho/deletar/<int:id>")
@login_required
def deletar_carrinho(id):
    cursor.execute("DELETE FROM Carrinho WHERE id=%s", (id,))
    conexao.commit()
    return redirect("/carrinho")

# -----------------------------
# Rodar app
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
