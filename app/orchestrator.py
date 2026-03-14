# from app.agents.intent import analyze_intent
# from app.agents.generator import generate_sql
# from app.agents.explainer import explain_sql  

# from app.sql_guard import guard_sql
# def orchestrate(userquery: str):
#     try:
#         # 1️⃣ Intent Detection (The Gatekeeper)
#         # We use the new semantic analyzer we built
#         intent = analyze_intent(userquery)
        
#         # 🛑 CASE 1: General Chat / Off-Topic
#         if intent == "off_topic":
#             return {
#                 "type": "chat",
#                 "message": "👋 I am the AdventureWorks SQL Agent. I can help you with Sales, HR, Purchasing, and Inventory data. Try asking: 'Who are our top vendors?'",
#                 "sql": None,
#                 "explanation": []
#             }

#         # 🚀 CASE 2: Database Query (Valid SQL)
        
#         # 2️⃣ SQL Generation
#         sql = generate_sql(userquery)

#         # 🔁 Retry Logic: If model failed to give raw SQL, try one more time
#         if not sql.strip().lower().startswith("select"):
#             sql = generate_sql(
#                 "CRITICAL: RETURN ONLY SQL. NO TEXT. \n" + userquery
#             )

#         # Defensive cleanup
#         sql = sql.replace("`", "").strip()

#         # 3️⃣ Security Guard (Raises error if unsafe)
#         guard_sql(sql)

#         # 4️⃣ Explanation (Returns the new clean List of steps)
#         explanation_steps = explain_sql(sql)

#         return {
#             "type": "sql",
#             "sql": sql,
#             "explanation": explanation_steps, # This is now a List[]
#             "message": "Query generated successfully."
#         }

#     except Exception as e:
#         # 🔴 Error Handling: Return safe error state
#         return {
#             "type": "error",
#             "sql": "SELECT 'Error detected' AS Status",
#             "explanation": [str(e)], # Wrap error in a list for consistency
#             "message": f"Error: {str(e)}"
#         }

from app.agents.intent import analyze_intent
from app.agents.generator import generate_sql
from app.agents.explainer import explain_sql
from app.sql_guard import guard_sql


MAX_SQL_RETRIES = 1  # ⚠️ never increase (safety)


def orchestrate(userquery: str):
    try:
        # 1️⃣ Intent Detection (LLM-based)
        intent = analyze_intent(userquery)

        # 🛑 Off-topic / Chat
        if intent == "off_topic":
            return {
                "type": "chat",
                "message": (
                    "I am the AdventureWorks SQL Agent. "
                    "I can help with Sales, HR, Purchasing, and Inventory data. "
                    "Example: 'List all employees and their departments.'"
                ),
                "sql": None,
                "explanation": []
            }

        # 2️⃣ SQL Generation (first attempt)
        sql = generate_sql(userquery)

        if not sql.strip().lower().startswith("select"):
            sql = generate_sql(
                "RETURN ONLY A VALID SQL SERVER SELECT QUERY.\n" + userquery
            )

        sql = sql.replace("`", "").strip()

        # 3️⃣ Guard + Auto-Repair Loop
        attempts = 0
        while True:
            try:
                guard_sql(sql)
                break  # ✅ SQL is valid
            except Exception as guard_error:
                if attempts >= MAX_SQL_RETRIES:
                    raise guard_error

                # 🔁 Auto-fix with explicit correction
                correction_prompt = f"""
The following SQL is INVALID for AdventureWorks:

ERROR:
{str(guard_error)}

RULES:
- Use ONLY real columns from schema
- NEVER use EmployeeID
- Use BusinessEntityID instead
- NEVER invent columns
- RETURN SQL ONLY

FIX THIS SQL:
{sql}
"""
                sql = generate_sql(correction_prompt)
                sql = sql.replace("`", "").strip()
                attempts += 1

        # 4️⃣ Explanation (human-readable)
        explanation_steps = explain_sql(sql)

        return {
            "type": "sql",
            "sql": sql,
            "explanation": explanation_steps,
            "message": "Query generated successfully."
        }

    except Exception as e:
        # 🔴 Final Safe Failure
        return {
            "type": "error",
            "sql": "SELECT 'Error detected' AS Status;",
            "explanation": [str(e)],
            "message": f"Error: {str(e)}"
        }
