<div align="center">

# 🧠 SQL Whisperer
### *Natural Language → SQL · Powered by Groq × LLaMA 3.1*

<br/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com)
[![MS SQL](https://img.shields.io/badge/SQL_Server-MSSQL-CC2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white)](https://microsoft.com/sql-server)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

<br/>

> **Ask questions in plain English. Get SQL. Get answers.**  
> A multi-agent AI system that converts natural language into production-safe T-SQL queries for the AdventureWorks database — no SQL knowledge required.

<br/>

```
"Who are our top 5 customers by revenue this year?"
         ↓  Intent Agent  ↓  Generator Agent  ↓  Guard  ↓  Explainer Agent
SELECT TOP (5) p.FirstName + ' ' + p.LastName AS CustomerName,
       SUM(soh.TotalDue) AS TotalRevenue
FROM Sales.Customer c ...
```

</div>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [🤖 Agent Pipeline](#-agent-pipeline)
- [📁 Project Structure](#-project-structure)
- [⚙️ Tech Stack](#️-tech-stack)
- [🚀 Quick Start](#-quick-start)
- [🌐 API Reference](#-api-reference)
- [🛡️ SQL Guard System](#️-sql-guard-system)
- [🗄️ Database Schema](#️-database-schema)
- [🔧 Configuration](#-configuration)
- [📸 Pages Overview](#-pages-overview)
- [🗺️ Roadmap](#️-roadmap)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🗣️ **Natural Language Input** | Ask anything in plain English — no SQL needed |
| 🤖 **Multi-Agent AI** | Dedicated agents for Intent, Generation, and Explanation |
| 🛡️ **SQL Safety Guard** | Rule-based firewall blocks destructive queries & hallucinations |
| 🔁 **Auto-Repair Loop** | Automatically detects and corrects invalid SQL before execution |
| 📖 **Query Explainer** | Every query comes with a plain-English step-by-step explanation |
| 🕑 **Query History** | Persistent history stored in SQL Server with full result data |
| ⚡ **Groq-Powered** | Ultra-fast inference via LLaMA 3.1 8B Instant (free tier) |
| 🌐 **REST API** | Clean FastAPI endpoints ready for frontend or integration use |
| 🎨 **Web UI** | Jinja2-rendered pages: Home, History, and About |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│               (Web Browser / REST API Client)                │
└──────────────────────────┬──────────────────────────────────┘
                           │  POST /ask
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                         │
│                        main.py                               │
│         ┌──────────────────────────────────┐                 │
│         │         Orchestrator             │                 │
│         │       orchestrator.py            │                 │
│         └──┬──────────┬───────────┬────────┘                 │
│            │          │           │                          │
│     ┌──────▼──┐  ┌────▼────┐  ┌──▼──────┐                   │
│     │ Intent  │  │  SQL    │  │Explainer│                   │
│     │ Agent   │  │Generator│  │ Agent   │                   │
│     └─────────┘  └────┬────┘  └─────────┘                   │
│                       │                                      │
│                  ┌────▼────┐                                 │
│                  │ SQL     │                                 │
│                  │ Guard   │                                 │
│                  └─────────┘                                 │
└──────────────────────────┬──────────────────────────────────┘
                           │
          ┌────────────────┴─────────────────┐
          │                                   │
   ┌──────▼──────┐                   ┌────────▼────────┐
   │  Groq API   │                   │  MS SQL Server  │
   │ LLaMA 3.1   │                   │  AdventureWorks │
   └─────────────┘                   └─────────────────┘
```

---

## 🤖 Agent Pipeline

Every query flows through a strict 4-stage pipeline:

```
User Query
    │
    ▼
┌──────────────────────────────────────────┐
│  Stage 1 │ 🎯 Intent Agent               │
│           │ Classifies: valid_sql         │
│           │             or off_topic      │
└──────────────────────────────────────────┘
    │ valid_sql
    ▼
┌──────────────────────────────────────────┐
│  Stage 2 │ ⚙️  Generator Agent           │
│           │ Loads dynamic schema          │
│           │ Fills PROMPT_TEMPLATE         │
│           │ Calls LLaMA 3.1 → raw SQL     │
└──────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────┐
│  Stage 3 │ 🛡️  SQL Guard                 │
│           │ Blocks: DELETE/UPDATE/DROP    │
│           │ Blocks: Hallucinated columns  │
│           │ Auto-Repair: up to 1 retry    │
└──────────────────────────────────────────┘
    │ safe SQL
    ▼
┌──────────────────────────────────────────┐
│  Stage 4 │ 📖 Explainer Agent            │
│           │ Produces plain-English steps  │
│           │ Shown alongside results       │
└──────────────────────────────────────────┘
    │
    ▼
  Execute → Return Results → Save History
```

---

## 📁 Project Structure

```
sql-whisperer/
│
├── app/
│   ├── agents/
│   │   ├── intent.py          # 🎯 Classifies user intent (valid_sql / off_topic)
│   │   ├── generator.py       # ⚙️  Generates T-SQL from natural language
│   │   └── explainer.py       # 📖 Explains SQL in plain English
│   │
│   ├── templates/
│   │   ├── index.html         # 🏠 Main chat interface
│   │   ├── history.html       # 🕑 Query history page
│   │   └── about.html         # ℹ️  About page
│   │
│   ├── config.py              # 🔧 Groq API keys & model config
│   ├── db.py                  # 🗄️  MS SQL Server connection & executor
│   ├── llm_client.py          # 🤖 Unified LLM API caller (Groq-compatible)
│   ├── orchestrator.py        # 🎼 Pipeline coordinator
│   ├── prompt.py              # 📝 Master T-SQL prompt template
│   ├── schema_loader.py       # 🔍 Dynamic schema builder from INFORMATION_SCHEMA
│   └── sql_guard.py           # 🛡️  Rule-based SQL safety firewall
│
├── main.py                    # 🚀 FastAPI app entry point
├── requirements.txt           # 📦 Python dependencies
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Web Framework** | FastAPI | REST API + HTML routing |
| **Templating** | Jinja2 | Server-side rendered pages |
| **LLM Provider** | Groq API | Fast LLaMA 3.1 inference |
| **LLM Model** | `llama-3.1-8b-instant` | Intent, generation, explanation |
| **Database** | MS SQL Server 2016 | AdventureWorks data storage |
| **DB Driver** | pymssql | Python ↔ SQL Server connector |
| **Config** | python-dotenv | Environment variable management |
| **Server** | Uvicorn | ASGI production server |

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/sql-whisperer.git
cd sql-whisperer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Groq API Key — get yours at https://console.groq.com
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx

# MS SQL Server password
DB_PASSWORD=your_database_password
```

### 4. Run the Server

```bash
uvicorn main:app --reload
```

### 5. Open the App

```
http://localhost:8000
```

---

## 🌐 API Reference

### `POST /ask`
Convert a natural language question into SQL and return results.

**Request**
```json
{
  "userquery": "Show me the top 10 products by sales revenue"
}
```

**Response (success)**
```json
{
  "status": "success",
  "sql": "SELECT TOP (10) p.Name, SUM(sod.LineTotal) AS Revenue ...",
  "data": [ { "Name": "Mountain-200 Black", "Revenue": 4352820.77 }, ... ],
  "explanation": [
    "Joins Product to SalesOrderDetail via ProductID",
    "Sums LineTotal per product to get total revenue",
    "Orders by revenue descending and limits to top 10"
  ]
}
```

**Response (off-topic)**
```json
{
  "status": "error",
  "message": "I am the AdventureWorks SQL Agent. I can help with Sales, HR, Purchasing, and Inventory data."
}
```

---

### `GET /api/history`
Retrieve the last 100 query history entries.

```json
{
  "entries": [
    {
      "id": 42,
      "timestamp": "2025-07-10 14:32:01",
      "query": "List all employees by department",
      "sql": "SELECT ...",
      "row_count": 290,
      "status": "success",
      "data": [ ... ]
    }
  ]
}
```

---

### `DELETE /api/history`
Clear all query history.

```json
{ "status": "cleared" }
```

---

### `GET /`
Home page — chat interface.

### `GET /about`
About page — project information.

### `GET /history`
History page — past queries browser.

---

## 🛡️ SQL Guard System

The `sql_guard.py` module is a rule-based firewall that runs on **every generated query** before execution.

| Rule | Protection |
|---|---|
| 🚫 **Destructive Keywords** | Blocks `DELETE`, `UPDATE`, `INSERT`, `DROP`, `ALTER`, `CREATE`, `TRUNCATE` |
| 🚫 **MySQL Backticks** | Rejects queries with `` ` `` (not valid T-SQL) |
| 🚫 **Fake `ProductName`** | Forces use of `Production.Product.Name AS ProductName` |
| 🚫 **`EmployeeID` Column** | Enforces `BusinessEntityID` (AdventureWorks standard) |
| 🚫 **Wrong `ProductID` Scope** | Blocks `ProductID` on `SalesOrderHeader` (it lives in `SalesOrderDetail`) |
| 🚫 **Orphaned `TotalDue`** | Requires `SalesOrderHeader` in scope when ordering by `TotalDue` |
| 🚫 **Hallucinated Columns** | Blocks invented columns like `Brand`, `ModelNumber` |

If a guard check fails, the orchestrator triggers one **auto-repair pass** — feeding the error message back to the generator for a corrected query.

---

## 🗄️ Database Schema

The `schema_loader.py` dynamically builds a **filtered schema snapshot** per query — only the relevant tables are included to keep the LLM prompt focused.

**Supported Domains:**

```
📦  Production     →  Product, ProductSubcategory, ProductCategory,
                       ProductInventory

💰  Sales          →  SalesOrderHeader, SalesOrderDetail, Customer

👤  Person         →  Person (names for Employees & Customers)

🧑‍💼  HumanResources →  Employee, EmployeeDepartmentHistory, Department

🏭  Purchasing     →  Vendor, PurchaseOrderHeader
```

> **Schema is loaded live** from `INFORMATION_SCHEMA.COLUMNS` on every request — always up-to-date, never stale.

---

## 🔧 Configuration

All configuration lives in `config.py` and `.env`.

```python
# config.py

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

MODELS = {
    "intent":    "llama-3.1-8b-instant",   # Fast classifier
    "generator": "llama-3.1-8b-instant",   # SQL generation
    "validator": "llama-3.1-8b-instant",   # (reserved)
    "explainer": "llama-3.1-8b-instant"    # Plain-English explanations
}
```

To swap in a different model (e.g., `llama-3.3-70b-versatile` for better accuracy), update the relevant key.

---

## 📸 Pages Overview

| Page | Route | Description |
|---|---|---|
| 🏠 **Home** | `/` | Main chat interface — type questions, see results |
| 🕑 **History** | `/history` | Browse, inspect, and clear past queries |
| ℹ️ **About** | `/about` | Project info and usage guide |

---

## 🗺️ Roadmap

- [ ] 🔐 User authentication & per-user history
- [ ] 📊 Chart rendering for aggregate query results
- [ ] 🗃️ Support multiple database schemas (beyond AdventureWorks)
- [ ] 🔄 Streaming responses via Server-Sent Events
- [ ] 🧪 Automated prompt evaluation suite
- [ ] 📤 CSV / Excel export for query results
- [ ] 🐳 Docker deployment config

---

<div align="center">

Made with ❤️ using **FastAPI** · **Groq** · **LLaMA 3.1**

*If this project helped you, consider giving it a ⭐*

</div>
