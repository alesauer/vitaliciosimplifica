import csv
import sys
import mysql.connector

# Configurações do banco de dados
DB = "vitaliciosimplifica"
USER = "root"
PASS = "teste10"
#PASS = "GxgLTr201@#$"
TABLE = "leads"

# Caminho do CSV (por padrão, 'leads.csv' ou argumento passado)
CSV_PATH = sys.argv[1] if len(sys.argv) > 1 else "leads.csv"

try:
    # Conexão com o banco
    conn = mysql.connector.connect(
        host="localhost",
        user=USER,
        password=PASS,
        database=DB
    )
    cursor = conn.cursor()

    # Abre e lê o CSV
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)  # Pula o cabeçalho

        for linha in reader:
            if len(linha) < 2:
                continue  # pula linhas incompletas

            email, desconto = linha
            cursor.execute(
                f"INSERT INTO `{TABLE}` (email, tipo, desconto) VALUES (%s, 'aluno', %s)",
                (email.strip(), desconto.strip())
            )

    conn.commit()
    print("✅ Importação concluída com sucesso.")

except mysql.connector.Error as err:
    print(f"❌ Erro no MySQL: {err}")
except FileNotFoundError:
    print(f"❌ Arquivo CSV não encontrado: {CSV_PATH}")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
