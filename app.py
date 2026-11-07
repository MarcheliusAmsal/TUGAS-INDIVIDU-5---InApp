from flask import Flask, render_template, session, abort, redirect, url_for, request

app = Flask(__name__)
app.secret_key = 'inapp_rahasia_123' 

# Data Dummy 
USERS_DB = {
    'admin': {
        'nama': 'Budi Santoso', 
        'role': 'Kepala Gudang', 
        'email': 'budi@inapp.com', 
        'password': 'admin123',
        'avatar': 'foto-budi.jpg'  
    },
    'petugas': {
        'nama': 'Siti Aminah', 
        'role': 'Petugas Inbound', 
        'email': 'siti@inapp.com', 
        'password': 'petugas123',
        'avatar': 'foto-siti.jpg'  
    }
}

ITEMS_DB = {
    1: {
        'nama': 'Laptop Dell',
        'kode': 'PRD-DELL-001',
        'kategori': 'Elektronik & Perangkat Komputasi',
        'brand': 'Dell Inc.',
        'harga': 'Rp 14.500.000',
        'stok': 15,
        'satuan': 'Unit',
        'lokasi_rak': 'Rak A-01 (Lantai 2)',
        'deskripsi': 'Laptop Dell performa tinggi untuk kebutuhan komputasi operasional.',
        'status': 'Tersedia'
    },
    2: {
        'nama': 'Mouse Wireless',
        'kode': 'PRD-LOGI-002',
        'kategori': 'Aksesoris Komputer',
        'brand': 'Logitech',
        'harga': 'Rp 275.000',
        'stok': 50,
        'satuan': 'Pcs',
        'lokasi_rak': 'Rak B-04 (Lantai 1)',
        'deskripsi': 'Mouse wireless ergonomis dengan konektivitas 2.4 GHz dan Bluetooth.',
        'status': 'Tersedia'
    }
}

@app.context_processor
def inject_user():
    """Mengirim data user yang sedang login ke seluruh file HTML secara otomatis"""
    if 'username' in session:
        # Jika ada yang login, ambil datanya dari USERS_DB
        aktif = USERS_DB.get(session['username'])
        return dict(current_user=aktif)
    # Jika belum login, kembalikan kosong
    return dict(current_user=None)
    
# Rute pengecekan login
@app.route('/cek', methods=['GET', 'POST'])
def cek_login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
    else:
        username = request.args.get('username', '').strip()
        password = request.args.get('password', '').strip()

    if username and username in USERS_DB and USERS_DB[username]['password'] == password:
        session['username'] = username  # Simpan sesi login
        return redirect(url_for('detail_user', username=username))

    abort(404)

@app.route('/cek/<username>')
def cek_username(username):
    if username in USERS_DB:
        return redirect(url_for('detail_user', username=username))
    abort(404)

# LANGKAH 2: Rute Cek Status Username — demonstrasi 3 kondisi Jinja2
@app.route('/cek-status')
def cek_status():
    username_input = request.args.get('username', '').strip()

    # Jika belum ada query sama sekali, tampilkan halaman kosong (state awal)
    if 'username' not in request.args:
        return render_template('cek_status.html', status=None, username_input='')

    # Kondisi 1: format tidak valid (string kosong)
    if not username_input:
        status = 'tidak valid'
    # Kondisi 2: username ditemukan di USERS_DB
    elif username_input in USERS_DB:
        status = 'tersedia'
    # Kondisi 3 (else): username tidak ditemukan
    else:
        status = 'tidak ditemukan'

    return render_template('cek_status.html', status=status, username_input=username_input)

# Rute dinamis profil user & detail produk
@app.route('/profil')
def profil_redirect():
    """Rute pintar yang mengarahkan user ke profilnya masing-masing"""
    if 'username' in session:
        return redirect(url_for('detail_user', username=session['username']))
    return redirect(url_for('signin'))

@app.route('/user/<username>')
def detail_user(username):
    user_data = USERS_DB.get(username)
    if user_data:
        return render_template('user_profile.html', username=username, user=user_data)
    abort(404)

@app.route('/produk/<int:id>')
def detail_produk(id):
    produk = ITEMS_DB.get(id)
    if produk is None:
        abort(404)
    return render_template('product_detail.html', produk=produk, id=id)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404-error.html'), 404

# Rute - rute statis 
@app.route('/', endpoint='dashboard')
@app.route('/index.html', endpoint='index')
def dashboard():
    return render_template('index.html')

@app.route('/inventory')
@app.route('/inventory.html')
def inventory():
    # LANGKAH 3: Kirim ITEMS_DB ke template agar bisa di-loop dengan {% for %}
    return render_template('inventory.html', items=ITEMS_DB)

@app.route('/create-product')
@app.route('/create-product.html')
def create_product():
    return render_template('create-product.html')

@app.route('/reports')
@app.route('/reports.html')
def reports():
    return render_template('reports.html')

@app.route('/signin')
@app.route('/signin.html')
def signin():
    return render_template('signin.html')

@app.route('/signup')
@app.route('/signup.html')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)