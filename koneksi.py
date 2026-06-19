import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='sekolah'
    )
    return conn

if __name__ == "__main__":
    conn = get_connection()
    if conn.is_connected():
        print("Koneksi berhasil!")
    conn.close()