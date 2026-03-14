# File: app/agents/intent.py

from app.llm_client import call_llm
from app.config import MODELS


def analyze_intent(user_query: str) -> str:
    """
    Uses ONLY an LLM to determine whether the user's query
    should be handled as a SQL/database request.

    Returns:
        'valid_sql' or 'off_topic'
    """

    prompt = f"""
You are an INTENT CLASSIFIER for an Enterprise SQL Agent.

Your ONLY task:
Classify whether the user's query requires generating a SQL query
for the AdventureWorks database.

==================================================
DATABASE SCOPE
==================================================
The database contains ONLY the following domains:

- Sales (orders, revenue, customers, totals, reports)
- Products (products, inventory, categories, stock)
- Human Resources (employees, departments, jobs)
- Purchasing (vendors, suppliers, purchase orders)

==================================================
CLASSIFICATION RULES (STRICT)
==================================================
Return EXACTLY ONE of the following labels:

valid_sql
off_topic

RULES:
1. Return valid_sql IF the query:
   - Requests data
   - Asks to list, count, sum, average, rank, filter, group, or analyze
   - Mentions employees, products, customers, sales, orders, vendors, departments
   - Can reasonably be answered using SQL on AdventureWorks

2. Return off_topic IF the query:
   - Is a greeting, thanks, or casual conversation
   - Asks for explanations, essays, poems, or jokes
   - Requests programming code (Python, Java, React, etc.)
   - Is unrelated to databases or business data
   - Is ambiguous but NOT clearly a data request

==================================================
IMPORTANT CONSTRAINTS
==================================================
- Do NOT explain your reasoning
- Do NOT output SQL
- Do NOT output punctuation
- Do NOT output anything except ONE WORD:
  valid_sql OR off_topic

==================================================
EXAMPLES
==================================================
"Hi, how are you?" → off_topic
"List all employees" → valid_sql
"Show top 5 products by revenue" → valid_sql
"Explain what SQL is" → off_topic
"Write Python code" → off_topic
"Who are our best customers?" → valid_sql

==================================================
USER QUERY
==================================================
{user_query}

FINAL ANSWER:
"""

    response = call_llm(MODELS["intent"], prompt)

    # Normalize + fail-safe
    label = response.strip().lower()

    if label == "valid_sql":
        return "valid_sql"

    return "off_topic"
