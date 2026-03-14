import re

# --------------------------------------------------
# Destructive operations (ALWAYS forbidden)
# --------------------------------------------------
FORBIDDEN_KEYWORDS = [
    "delete", "update", "insert",
    "drop", "truncate", "alter", "create"
]

# Known hallucinated columns (AdventureWorks does NOT have these)
HALLUCINATED_COLUMNS = [
    "brand",
    "modelnumber"
]


def guard_sql(sql: str):
    """
    Rule-based SQL safety and schema guard.
    Blocks destructive operations and common hallucinations.
    """

    lower_sql = sql.lower()

    # 1️⃣ Block destructive SQL operations
    for word in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{word}\b", lower_sql):
            raise Exception(
                f"Blocked unsafe SQL operation: {word.upper()}"
            )

    # 2️⃣ Block MySQL-style backticks
    if "`" in sql:
        raise Exception(
            "Invalid SQL syntax: backticks (`) are not supported in SQL Server."
        )

    # 3️⃣ Block fake ProductName column (alias allowed only)
    # ❌ SELECT ProductName FROM Production.Product
    # ✅ SELECT Production.Product.Name AS ProductName
    if re.search(r"\bselect\s+productname\b", lower_sql):
        raise Exception(
            "Invalid column 'ProductName'. "
            "Use Production.Product.Name AS ProductName"
        )

    # 4️⃣ 🚫 Block hallucinated EmployeeID (CRITICAL RULE)
    # AdventureWorks uses BusinessEntityID
    if re.search(r"\bemployeeid\b", lower_sql):
        raise Exception(
            "Invalid column 'EmployeeID'. "
            "Use HumanResources.Employee.BusinessEntityID"
        )

    # 5️⃣ 🚫 Block ProductID usage on SalesOrderHeader (CRITICAL FIX)
    # ProductID exists ONLY in SalesOrderDetail
    if (
        re.search(r"\bsales\.salesorderheader\.\s*productid\b", lower_sql)
        or re.search(r"\bsoh\.\s*productid\b", lower_sql)
    ):
        raise Exception(
            "Invalid column reference: ProductID does NOT exist in "
            "Sales.SalesOrderHeader. "
            "Use Sales.SalesOrderDetail.ProductID instead."
        )

    # 6️⃣ 🚨 TotalDue ORDER BY scope enforcement
    # ORDER BY TotalDue requires SalesOrderHeader in outer query
    if "order by totaldue" in lower_sql:
        if "sales.salesorderheader" not in lower_sql:
            raise Exception(
                "Invalid SQL: ORDER BY TotalDue requires "
                "joining Sales.SalesOrderHeader"
            )

    # 7️⃣ 🚫 Block other known hallucinated columns
    for col in HALLUCINATED_COLUMNS:
        if re.search(rf"\b{col}\b", lower_sql):
            raise Exception(
                f"Invalid column '{col}'. "
                "Use only real columns from the database schema."
            )

    # ✅ SQL passed all guard checks
    return
