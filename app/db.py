import pymssql
import os

def get_connection():
    return pymssql.connect(
        server="sql.bsite.net\\MSSQL2016",
        user="sonuray_sonuray_",
        password=os.getenv("DB_PASSWORD"),
        database="sonuray_sonuray_"
    )

def execute_sql(sql: str):
    conn = get_connection()
    cursor = conn.cursor(as_dict=True)
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return rows