from datetime import datetime
import locale
from pyexpat.errors import messages
from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
from flask_socketio import SocketIO, emit
import mysql.connector
from flask import session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Ganti dengan kunci rahasia yang kuat

# Konfigurasi MySQL
db_config = {
    cnx = mysql.connector.connect(user="ccweb", 
    password="Amikom01",
    host="webfpccawan1.mysql.database.azure.com",
    port=3306, 
    database="db_merek",
    ssl_ca="{ca-cert filename}", 
    ssl_disabled=False)
}

socketio = SocketIO(app)

# Helper untuk koneksi database
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Halaman utama
@app.route('/')
def index():
    if 'user_id' in session:  # Cek apakah pengguna sudah login
        return redirect('/dashboard')  # Arahkan ke dashboard jika sudah login

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM db_mobil")  # Mengambil semua mobil dari tabel db_mobil
    cars = cursor.fetchall()  # Menyimpan hasil query
    conn.close()
    return render_template('index.html', cars=cars)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validasi input
        if not username or not password:
            flash('Username dan password harus diisi!', 'error')
            return redirect('/login')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM akun WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']  # Pastikan role diambil dari database
            flash('Login berhasil!', 'success')
            return redirect('/dashboard')
        else:
            flash('Username atau password salah!', 'error')
            return redirect('/login')
    return render_template('login.html')

# Logout pengguna
@app.route('/logout')
def logout():
    session.clear()
    flash('Anda telah logout.', 'success')
    return redirect('/')

# Registrasi pengguna baru
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validasi input
        if not username or not password:
            flash('Username dan password harus diisi!', 'error')
            return redirect('/register')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO akun (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            flash('Registrasi berhasil! Silakan login.', 'success')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'error')
        finally:
            conn.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Anda harus login untuk mengakses halaman ini.', 'error')
        return redirect('/login')
    
    # Memeriksa role user dan mengarahkan ke dashboard yang sesuai
    role = session['role']
    if role == 'admin':
        return redirect('/dashboard/admin')  # Redirect ke dashboard admin
    elif role == 'user':
        return redirect('/dashboard/user')  # Redirect ke dashboard user

# Dashboard untuk Admin
@app.route('/dashboard/admin')
def dashboard_admin():
    if 'user_id' not in session:
        flash('Anda harus login untuk mengakses halaman ini.', 'error')
        return redirect('/login')

    # Pastikan hanya admin yang bisa mengakses halaman ini
    if session['role'] != 'admin':
        flash('Anda tidak memiliki akses untuk halaman ini.', 'error')
        return redirect('/')

    # Mengambil data mobil dari database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM db_mobil")
    cars = cursor.fetchall()

    # Mengambil data akun dari database
    cursor.execute("SELECT * FROM akun")  # Ambil semua akun
    users = cursor.fetchall()

    conn.close()
    return render_template('dashboard_admin.html', cars=cars, users=users)

@app.route('/user/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    if 'user_id' not in session:
        flash('Anda harus login untuk mengakses halaman ini.', 'error')
        return redirect('/login')

    # Pastikan hanya admin yang bisa mengedit akun
    if session['role'] != 'admin':
        flash('Anda tidak memiliki akses untuk mengedit akun.', 'error')
        return redirect('/dashboard/admin')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM akun WHERE id = %s", (id,))
    user = cursor.fetchone()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        cursor.execute("""
            UPDATE akun
            SET username = %s, password = %s, role = %s
            WHERE id = %s
        """, (username, password, role, id))
        conn.commit()
        flash('Akun berhasil diperbarui!', 'success')
        return redirect('/dashboard/admin')

    conn.close()
    return render_template('edit_user.html', user=user)

@app.route('/user/delete/<int:id>', methods=['POST'])
def delete_user(id):
    if 'user_id' not in session:
        flash('Anda harus login untuk mengakses halaman ini.', 'error')
        return redirect('/login')

    # Pastikan hanya admin yang bisa menghapus akun
    if session['role'] != 'admin':
        flash('Anda tidak memiliki akses untuk menghapus akun.', 'error')
        return redirect('/dashboard/admin')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # SQL query untuk menghapus akun berdasarkan id
        cursor.execute("DELETE FROM akun WHERE id = %s", (id,))
        conn.commit()
        flash('Akun berhasil dihapus.', 'success')

    except Exception as e:
        flash(f'Error: {e}', 'error')

    finally:
        conn.close()

    return redirect('/dashboard/admin')

# Dashboard untuk User
@app.route('/dashboard/user')
def dashboard_user():
    if 'user_id' not in session:
        flash('Anda harus login untuk mengakses halaman ini.', 'error')
        return redirect('/login')
    
    # Menampilkan hanya daftar mobil tanpa kemampuan untuk mengedit atau menghapus
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM db_mobil")
    cars = cursor.fetchall()
    conn.close()
    return render_template('dashboard_user.html', cars=cars)

@app.route('/mobil')
def list_mobil():
    if 'user_id' not in session:
        flash('Anda harus login untuk mengakses halaman ini.', 'error')
        return redirect('/login')

    # Mengambil data mobil dari database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM db_mobil")
    cars = cursor.fetchall()
    conn.close()

    # Cek apakah pengguna adalah admin atau user
    role = session['role']
    
    return render_template('list_mobil.html', cars=cars, role=role)


@app.route('/mobil/add', methods=['GET', 'POST'])
def add_mobil():
    if 'user_id' not in session:
        flash('Anda harus login untuk mengakses halaman ini.', 'error')
        return redirect('/login')

    if request.method == 'POST':
        nama = request.form['nama_mobil']
        warna = request.form['warna']
        merek = request.form['merek']
        tipe = request.form['tipe']
        deskripsi = request.form['deskripsi']
        harga = request.form['harga']
        image_url = request.form['image_url']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO db_mobil (nama_mobil, warna, merek, tipe, deskripsi, harga, image_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nama, warna, merek, tipe, deskripsi, harga, image_url))
        conn.commit()
        conn.close()
        flash('Mobil berhasil ditambahkan!', 'success')
        return redirect('/mobil')
    return render_template('add_mobil.html')

@app.route('/register/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        id = request.form['id']
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO db_mobil (id, username, password, role)
            VALUES (%s, %s, %s, %s)
        """, (id, username, password, role))
        conn.commit()
        conn.close()
        flash('User berhasil ditambahkan!', 'success')
        return redirect('/login')
    return render_template('register.html')

@app.route('/mobil/edit/<int:id_mobil>', methods=['GET', 'POST'])
def edit_mobil(id_mobil):
    if 'user_id' not in session:
        flash('Anda harus login untuk mengakses halaman ini.', 'error')
        return redirect('/login')

    # Pastikan hanya admin yang bisa mengedit mobil
    if session['role'] != 'admin':
        flash('Anda tidak memiliki akses untuk mengedit mobil.', 'error')
        return redirect('/mobil')

    # Retrieve the car data from the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM db_mobil WHERE id_mobil = %s", (id_mobil,))
    car = cursor.fetchone()
    
    if car is None:
        flash('Mobil tidak ditemukan!', 'error')
        conn.close()
        return redirect('/mobil')

    # If the form is submitted (POST method)
    if request.method == 'POST':
        nama_mobil = request.form['nama_mobil']
        warna = request.form['warna']
        merek = request.form['merek']
        tipe = request.form['tipe']
        deskripsi = request.form['deskripsi']
        harga = request.form['harga']
        image_url = request.form['image_url']

        # Update the car data in the database
        cursor.execute("""
            UPDATE db_mobil
            SET nama_mobil = %s, warna = %s, merek = %s, tipe = %s, deskripsi = %s, harga = %s, image_url = %s
            WHERE id_mobil = %s
        """, (nama_mobil, warna, merek, tipe, deskripsi, harga, image_url, id_mobil))
        
        conn.commit()
        conn.close()

        flash('Mobil berhasil diperbarui!', 'success')
        return redirect('/mobil')

    # If the form is not submitted, render the edit form with existing car data
    conn.close()
    return render_template('edit_mobil.html', car=car)

    
@app.route('/mobil/delete/<int:id_mobil>', methods=['POST'])
def delete_mobil(id_mobil):
    if 'user_id' not in session:
        flash('Anda harus login untuk mengakses halaman ini.', 'error')
        return redirect('/login')

    # Pastikan hanya admin yang bisa menghapus mobil
    if session['role'] != 'admin':
        flash('Anda tidak memiliki akses untuk menghapus mobil.', 'error')
        return redirect('/mobil')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # SQL query untuk menghapus mobil berdasarkan id_mobil
        cursor.execute("DELETE FROM db_mobil WHERE id_mobil = %s", (id_mobil,))
        conn.commit()

        flash('Mobil berhasil dihapus.', 'success')

    except Exception as e:
        flash(f'Error: {e}', 'error')

    finally:
        conn.close()

    return redirect('/mobil')
    
@app.template_filter('format_currency')
def format_currency(value):
    return f"Rp {value:,.0f}"
    
@app.route('/mobil/search', methods=['GET'])
def search_mobil():
    query = request.args.get('query', '')  # Pencarian berdasarkan nama mobil
    min_price = request.args.get('min_price', type=int)  # Harga minimum
    max_price = request.args.get('max_price', type=int)  # Harga maksimum
    sort_by = request.args.get('sort_by', 'asc')  # Urutkan berdasarkan harga ('asc' atau 'desc')

    # Membuat query dasar untuk pencarian nama mobil
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql_query = "SELECT * FROM db_mobil WHERE nama_mobil LIKE %s"
    params = [f"%{query}%"]

    # Jika min_price diberikan, tambahkan ke query
    if min_price:
        sql_query += " AND harga >= %s"
        params.append(min_price)
    
    # Jika max_price diberikan, tambahkan ke query
    if max_price:
        sql_query += " AND harga <= %s"
        params.append(max_price)

    # Menambahkan pengurutan berdasarkan harga
    if sort_by == 'asc':
        sql_query += " ORDER BY harga ASC"
    else:
        sql_query += " ORDER BY harga DESC"

    cursor.execute(sql_query, params)
    cars = cursor.fetchall()
    conn.close()

    return render_template('mobil.html', cars=cars, query=query, min_price=min_price, max_price=max_price, sort_by=sort_by)


@app.route('/mobil/<int:id>')
def detail_mobil(id):
    if 'user_id' not in session:
        flash('Anda harus login untuk mengakses halaman ini.', 'error')
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM db_mobil WHERE id = %s", (id,))
    mobil = cursor.fetchone()
    conn.close()

    if mobil:
        return render_template('detail_mobil.html', mobil=mobil)
    else:
        flash('Mobil tidak ditemukan!', 'error')
        return redirect('/mobil')

@app.route('/forum', methods=['GET'])
def forum():
    if 'user_id' not in session:
        return redirect('/login')  # Arahkan ke login jika belum login

    user_id = session['user_id']
    role = session.get('role')  # Ambil role dari sesi

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT username FROM akun WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    cursor.execute("SELECT m.message, u.username, m.timestamp FROM messages m JOIN akun u ON m.user_id=u.id ORDER BY m.timestamp")
    messages = cursor.fetchall()
    cursor.close()

    return render_template('forum.html', user=user, role=role, messages=messages)

# SocketIO event untuk menerima pesan
@socketio.on('send_message')
def handle_send_message(data):
    message = data['message']
    user_id = session['user_id']
    
    # Simpan pesan ke database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (user_id, message) VALUES (%s, %s)", (user_id, message))
    conn.commit()
    cursor.close()
    
    # Emit pesan ke semua klien
    emit('receive_message', {'message': message, 'username': session['username']}, broadcast=True)

if __name__ == '__main__':
    app.run(debug=True)
