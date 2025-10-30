from flask import Flask, render_template, request
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consulta', methods=['GET'])
def consulta():
    email = request.args.get('email', '').strip().lower()
    if not email:
        return render_template('indexn.html')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT desconto FROM leads WHERE LOWER(email) = %s LIMIT 1", (email,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if not row:
            return render_template('index.html', not_found=True, searched_email=email)

        desconto = (row['desconto'] or '').strip().upper()

        if desconto == '2000':
            return render_template('opcao4.html')
        elif desconto == '3000':
            return render_template('opcao1.html')
        elif desconto == '2500':
            return render_template('opcao2.html')
        else:
            return render_template('index.html', not_found=True, searched_email=email)
    except Exception as e:
        print("Erro ao consultar o banco:", e)
        return render_template('index.html', db_error=True)

if __name__ == '__main__':
    app.run(debug=True)