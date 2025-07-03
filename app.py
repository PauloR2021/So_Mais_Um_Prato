from flask import Flask, render_template, request, redirect,flash,session,url_for
from datetime import timedelta
from DAO import *

app = Flask(__name__)
app.secret_key = 'dados'
app.permanent_session_lifetime = timedelta(minutes=30)

# Rota do Index - Página Principal
@app.route("/")
def index():
    return render_template('index.html')



# Rota de Login - Utilizada para Fazer Login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = login_usuario(email=email, senha=senha)

        if usuario is None:
            flash("Usuário ou senha inválidos", "error")
            return redirect(url_for('login'))  # volta para tela de login

        session['NOME'] = usuario['NOME']
        flash('Login realizado com sucesso!', 'success')
        return redirect(url_for('admin'))  # ✅ redireciona para painel admin

    return render_template('login.html')  # GET request (abrir o formulário)


#Rota para Logou - Encessa a Sessão Criada pelo Usuário
@app.route('/logout')
def logout():
    session.clear()
    flash("Logout realizado com sucesso!", "info")
    return redirect('/')


# Rota para acessar a área do Admin
@app.route('/admin')
def admin():
    if 'NOME' in session:
        nome = session['NOME']
        return render_template('sessaoAdmin.html',nome=nome)
    else:
        flash("Você precisa estar logado para acessar esta página.", "error")
        return redirect('/login')

# Página de listagem de receitas + busca por nome
@app.route('/receitas')
def receitas():
    nome_busca = request.args.get('nome')

    if nome_busca:
        receitas = todas_receitas_busca(busca=nome_busca)
    else:
        receitas = todas_receitas()

    return render_template('receitas.html', receitas=receitas)


"""
# Página de detalhes de uma receita específica
@app.route('/receita/<int:id>')
def detalhes_receita(id):
    receita = buscar_receita_por_id(id)
    if receita:
        return render_template('detalhes.html', receita=receita)
    else:
        flash("Receita não encontrada.", "error")
        return redirect(url_for('receitas'))"""

if __name__ == '__main__':
    app.run(debug=True)