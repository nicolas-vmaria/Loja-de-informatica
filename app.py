from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

conexao = mysql.connector.connect(
    host="localhost", port="3406", user="root", password="", database="loja_informatica"
)
cursor = conexao.cursor(dictionary=True)


# -----------------------------
# Página inicial
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")


# -----------------------------
# Listar produtos
# -----------------------------
@app.route("/produtos")
def listar_produtos():
    cursor.execute("SELECT * FROM Produtos")
    produtos = cursor.fetchall()
    return render_template("produtos.html", produtos=produtos)


# -----------------------------
# Formulário novo produto
# -----------------------------
@app.route("/novo")
def novo_produto():
    return render_template("novo-produto.html")


# -----------------------------
# Salvar novo produto
# -----------------------------
@app.route("/salvar-produto", methods=["POST"])
def salvar_produto():
    nome = request.form["nome"]
    preco = request.form["preco"]

    sql = "INSERT INTO Produtos (nome, preco) VALUES (%s, %s)"
    cursor.execute(sql, (nome, preco))
    conexao.commit()

    return redirect("/produtos")


# -----------------------------
# Deletar produto
# -----------------------------
@app.route("/delete/<int:id>")
def delete(id):
    cursor.execute("DELETE FROM Produtos WHERE id=%s", (id,))
    conexao.commit()
    return redirect("/produtos")


# -----------------------------
# Editar produto
# -----------------------------
@app.route("/editar/<int:id>")
def editar_produto(id):
    cursor.execute("SELECT * FROM Produtos WHERE id=%s", (id,))
    produto = cursor.fetchone()
    return render_template("editar-produto.html", produto=produto)


# -----------------------------
# Atualizar produto
# -----------------------------
@app.route("/atualizar-produto/<int:id>", methods=["POST"])
def atualizar_produto(id):
    nome = request.form["nome"]
    preco = request.form["preco"]

    sql = "UPDATE Produtos SET nome=%s, preco=%s WHERE id=%s"
    cursor.execute(sql, (nome, preco, id))
    conexao.commit()

    return redirect("/produtos")


# -----------------------------
# Adicionar produto ao carrinho
# -----------------------------
@app.route("/colocar/<int:produto_id>")
def colocar_no_carrinho(produto_id):
    # Carrinho global (sem usuário)
    cursor.execute("SELECT * FROM Carrinho WHERE produto_id=%s", (produto_id,))
    item = cursor.fetchone()
    if item:
        cursor.execute(
            "UPDATE Carrinho SET quantidade = quantidade + 1 WHERE id=%s", (item["id"],)
        )
    else:
        cursor.execute(
            "INSERT INTO Carrinho (produto_id, quantidade) VALUES (%s, 1)",
            (produto_id,),
        )
    conexao.commit()
    return redirect("/produtos")


# -----------------------------
# Página do carrinho
# -----------------------------
@app.route("/carrinho")
def carrinho():
    cursor.execute(
        """
        SELECT c.id, p.nome, p.preco, c.quantidade
        FROM Carrinho c
        JOIN Produtos p ON c.produto_id = p.id
    """
    )
    carrinho = cursor.fetchall()

    total = sum(item["preco"] * item["quantidade"] for item in carrinho)

    return render_template("carrinho.html", carrinho=carrinho, total=total)


# -----------------------------
# Remover item do carrinho
# -----------------------------
@app.route("/carrinho/deletar/<int:id>")
def deletar_carrinho(id):
    # Remove o item do carrinho pelo id
    cursor.execute("DELETE FROM Carrinho WHERE id=%s", (id,))
    conexao.commit()
    return redirect("/carrinho")


# -----------------------------
# Rodar app
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
