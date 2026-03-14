from app.llm_client import call_llm
from app.config import MODELS


def explain_sql(sql: str):
    """
    Explains how the SQL query is executed.
    Returns a list of simple steps.
    """

    prompt = f"""
Explain how the following SQL query is executed.
Use short, simple steps.
Do NOT include SQL code.

SQL:
{sql}
"""

    explanation = call_llm(MODELS["explainer"], prompt)

    return [
        line.strip("-• ").strip()
        for line in explanation.split("\n")
        if line.strip()
    ]
