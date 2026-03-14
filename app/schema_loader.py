from app.db import get_connection

MAX_COLUMNS_PER_TABLE = 10         # slightly expanded for Person.Person
MAX_SCHEMA_CHARS = 3000            # more schema gives better grounding

KEYWORDS = [
    "product", "sales", "order", "customer",
    "employee", "person", "address",
    "department", "humanresources",
    "vendor", "inventory", "category"
]

def load_schema(userquery: str) -> str:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, DATA_TYPE
        FROM INFORMATION_SCHEMA.COLUMNS
    """)

    query_lower = userquery.lower()
    schema_map = {}

    for schema, table, column, dtype in cur.fetchall():
        full_table = f"{schema}.{table}"
        full_table_lower = full_table.lower()

        include_table = False

        # Keyword relevance
        if any(k in full_table_lower or k in query_lower for k in KEYWORDS):
            include_table = True

        # HR domain auto-include Person.Person
        if "employee" in query_lower and (schema == "Person" and table == "Person"):
            include_table = True

        # Customer domain auto-include Person.Person
        if "customer" in query_lower and (schema == "Person" and table == "Person"):
            include_table = True

        # Sales domain auto-include PM tables
        if "sales" in query_lower:
            if schema in ["Sales", "Production"]:
                include_table = True

        if include_table:
            schema_map.setdefault(full_table, [])
            if len(schema_map[full_table]) < MAX_COLUMNS_PER_TABLE:
                schema_map[full_table].append(f"{column} ({dtype})")

    conn.close()

    # Build schema text
    schema_text = ""
    for table, cols in schema_map.items():
        block = f"\n{table}:\n"
        for col in cols:
            block += f"  - {col}\n"

        if len(schema_text) + len(block) > MAX_SCHEMA_CHARS:
            break

        schema_text += block

    return schema_text.strip()
