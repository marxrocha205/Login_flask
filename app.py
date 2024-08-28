import json
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Caminho do arquivo JSON para armazenar os usuários
USERS_FILE = 'users.json'

# Função para carregar usuários do arquivo JSON
def load_users():
    try:
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # Retorna um dicionário vazio se o arquivo não existir

# Função para salvar usuários no arquivo JSON
def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)

# Carrega os usuários na inicialização do aplicativo
users_db = load_users()

# Função para criar um administrador inicial se não existir
def create_initial_admin():
    admin_username = 'admin'
    admin_password = 'admin123'
    if admin_username not in users_db:
        users_db[admin_username] = {
            'password': generate_password_hash(admin_password),
            'role': 1  # 1 para administrador
        }
        save_users(users_db)

create_initial_admin()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users_db.get(username)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            session['role'] = user['role']
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Nome de usuário ou senha incorretos!', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users_db:
            flash('Nome de usuário já existe!', 'danger')
        else:
            users_db[username] = {
                'password': generate_password_hash(password),
                'role': 0  # 0 para usuário normal
            }
            save_users(users_db)
            flash('Registrado com sucesso!', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'username' not in session or session['role'] != 1:
        flash('Acesso negado!', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'create_admin' in request.form:
            new_admin_username = request.form['new_admin_username']
            new_admin_password = request.form['new_admin_password']
            if new_admin_username not in users_db:
                users_db[new_admin_username] = {
                    'password': generate_password_hash(new_admin_password),
                    'role': 1  # 1 para administrador
                }
                save_users(users_db)
                flash(f'Administrador {new_admin_username} criado com sucesso!', 'success')
            else:
                flash('Nome de usuário já existe!', 'danger')
        elif 'remove_user' in request.form:
            user_to_remove = request.form['user_to_remove']
            if user_to_remove in users_db and user_to_remove != session['username']:
                del users_db[user_to_remove]
                save_users(users_db)
                flash(f'Usuário {user_to_remove} removido com sucesso!', 'success')
            else:
                flash('Usuário não encontrado ou tentativa de remover a si mesmo!', 'danger')

    # Lista de usuários descriptografados (exceto o administrador atual)
    users_list = {username: user_data for username, user_data in users_db.items() if username != session['username']}
    
    return render_template('admin.html', users=users_list)

@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu!', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
