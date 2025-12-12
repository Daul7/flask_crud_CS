from flask import Flask, request, jsonify, make_response
from flask_mysqldb import MySQL
from dicttoxml import dicttoxml
import jwt
import datetime
from functools import wraps
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# --- MySQL configuration ---
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'  # change if needed
app.config['MYSQL_DB'] = 'sales_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# --- JWT & Bcrypt configuration ---
app.config['SECRET_KEY'] = 'supersecretkey123'
bcrypt = Bcrypt(app)

mysql = MySQL(app)

# --- Helper: format response JSON/XML ---
def format_response(data, fmt='json'):
    if fmt.lower() == 'xml':
        xml = dicttoxml(data, custom_root='response', attr_type=False)
        response = make_response(xml)
        response.headers['Content-Type'] = 'application/xml'
        return response
    return jsonify(data)

# --- JWT decorator ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split()[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Token format invalid'}), 401

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token is invalid'}), 401

        return f(*args, **kwargs)
    return decorated

# --- Auto-create default admin user ---
def create_default_user():
    cursor = mysql.connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE,
            password VARCHAR(255)
        )
    """)
    cursor.execute("SELECT * FROM api_users WHERE username='admin'")
    user = cursor.fetchone()
    if not user:
        hashed_pw = bcrypt.generate_password_hash("adminpassword").decode('utf-8')
        cursor.execute("INSERT INTO api_users (username, password) VALUES (%s, %s)", ('admin', hashed_pw))
        mysql.connection.commit()
    cursor.close()

with app.app_context():
    create_default_user()

# --- LOGIN ---
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM api_users WHERE username=%s", (username,))
    user = cursor.fetchone()
    cursor.close()

    if not user:
        return jsonify({'error': 'User not found'}), 401

    if bcrypt.check_password_hash(user['password'], password):
        token = jwt.encode({
            'user': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})

    return jsonify({'error': 'Invalid password'}), 401

# --- CRUD ROUTES ---
# CREATE, GET ALL, DELETE by query
@app.route('/company', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@token_required
def companies():
    fmt = request.args.get('format', 'json')

    # DELETE via query ?id=
    if request.method == 'DELETE':
        company_id = request.args.get('id')
        if not company_id:
            return format_response({'error': 'Company id is required'}, fmt), 400
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM company WHERE id=%s", (company_id,))
        mysql.connection.commit()
        cursor.close()
        return format_response({'message': f'Company {company_id} deleted'}, fmt)

    # CREATE
    if request.method == 'POST':
        data = request.get_json()
        honda = data.get('HONDA')
        yamaha = data.get('YAMAHA')
        suzuki = data.get('SUZUKI')
        rusi = data.get('RUSI')
        kawasaki = data.get('KAWASAKI')

        if not all([honda, yamaha, suzuki, rusi, kawasaki]):
            return format_response({'error': 'All fields are required'}, fmt), 400

        cursor = mysql.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO company (HONDA, YAMAHA, SUZUKI, RUSI, KAWASAKI) VALUES (%s,%s,%s,%s,%s)",
                (honda, yamaha, suzuki, rusi, kawasaki)
            )
            mysql.connection.commit()
            company_id = cursor.lastrowid
            cursor.close()
            return format_response({'message': 'Company created', 'id': company_id}, fmt), 201
        except Exception as e:
            cursor.close()
            return format_response({'error': str(e)}, fmt), 500

    # GET with optional search
    search = request.args.get('search')
    cursor = mysql.connection.cursor()
    if search:
        query = """
            SELECT * FROM company 
            WHERE LOWER(HONDA) LIKE %s
            OR LOWER(YAMAHA) LIKE %s
            OR LOWER(SUZUKI) LIKE %s
            OR LOWER(RUSI) LIKE %s
            OR LOWER(KAWASAKI) LIKE %s
        """
        search_param = f"%{search.lower()}%"
        cursor.execute(query, (search_param, search_param, search_param, search_param, search_param))
    else:
        cursor.execute("SELECT * FROM company")
    companies = cursor.fetchall()
    cursor.close()
    return format_response(companies, fmt)

# GET SINGLE, UPDATE, DELETE by ID
@app.route('/company/<int:company_id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
@token_required
def company_operations(company_id):
    fmt = request.args.get('format', 'json')
    cursor = mysql.connection.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM company WHERE id=%s", (company_id,))
        company = cursor.fetchone()
        cursor.close()
        if not company:
            return format_response({'error': 'Company not found'}, fmt), 404
        return format_response(company, fmt)

    elif request.method == 'PUT':
        data = request.get_json()
        honda = data.get('HONDA')
        yamaha = data.get('YAMAHA')
        suzuki = data.get('SUZUKI')
        rusi = data.get('RUSI')
        kawasaki = data.get('KAWASAKI')

        if not all([honda, yamaha, suzuki, rusi, kawasaki]):
            return format_response({'error': 'All fields are required'}, fmt), 400

        try:
            cursor.execute(
                "UPDATE company SET HONDA=%s,YAMAHA=%s,SUZUKI=%s,RUSI=%s,KAWASAKI=%s WHERE id=%s",
                (honda, yamaha, suzuki, rusi, kawasaki, company_id)
            )
            mysql.connection.commit()
            cursor.close()
            return format_response({'message': 'Company updated'}, fmt)
        except Exception as e:
            cursor.close()
            return format_response({'error': str(e)}, fmt), 500

    elif request.method == 'DELETE':
        cursor.execute("DELETE FROM company WHERE id=%s", (company_id,))
        mysql.connection.commit()
        cursor.close()
        return format_response({'message': f'Company {company_id} deleted'}, fmt)

# Home
@app.route('/')
def home():
    return "Company CRUD API is running. Use /company endpoints."

if __name__ == '__main__':
    app.run(debug=True)
