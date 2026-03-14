from app.llm_client import call_llm
from app.config import MODELS
from app.schema_loader import load_schema
from app.prompt import PROMPT_TEMPLATE


def generate_sql(userquery: str) -> str:
    """
    Generates a SQL Server SELECT query for AdventureWorks.
    """

    schema = load_schema(userquery)

    if not schema.strip():
        return "SELECT 'Query cannot be answered with available schema' AS Message;"

    prompt = PROMPT_TEMPLATE.format(
        schema=schema,
        userquery=userquery
    )

    sql = call_llm(MODELS["generator"], prompt)

    # Defensive cleanup
    sql = sql.strip()

    if not sql.endswith(";"):
        sql += ";"

    return sql
