import pyodbc

def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=sql.bsite.net\\MSSQL2016;"
        "DATABASE=sonuray_sonuray_;"
        "UID=sonuray_sonuray_;"
        "PWD=RRAYsonu@0900@;"
        "TrustServerCertificate=yes;"
    )

def execute_sql(sql: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return rows