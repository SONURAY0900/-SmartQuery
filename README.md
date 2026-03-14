<div align="center">

# ⚡ SmartQuery
### *Natural Language → SQL · Powered by Groq × LLaMA 3.1*

<br/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com)
[![MS SQL](https://img.shields.io/badge/SQL_Server-2016-CC2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white)](https://microsoft.com/sql-server)
[![Render](https://img.shields.io/badge/Deployed_on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

<br/>

> **Ask questions in plain English. Get SQL. Get answers.**
> A multi-agent AI system that converts natural language into production-safe T-SQL queries on the AdventureWorks 2016 database — no SQL knowledge required.

<br/>

🔗 **Live Demo:** [https://smartquery-ysef.onrender.com](https://smartquery-ysef.onrender.com)

<br/>

```
"Who are our top 5 customers by revenue?"
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
| 📖 **Query Explainer** | Every query comes with a plain-English explanation |
| 🕑 **Query History** | Persistent history stored in SQL Server cloud database |
| ⚡ **Groq-Powered** | Ultra-fast inference via LLaMA 3.1 8B Instant |
| 🌐 **Live Deployed** | Fully hosted on Render with cloud SQL Server |
| 🎨 **Beautiful UI** | Dark/Light theme, particle animations, syntax highlighting |

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
│                    FastAPI Backend                           │
│                      main.py                                │
│         ┌──────────────────────────────────┐                │
│         │           Orchestrator           │                │
│         │         orchestrator.py          │                │
│         └──┬──────────┬───────────┬────────┘                │
│            │          │           │                         │
│     ┌──────▼──┐  ┌────▼────┐  ┌──▼──────┐                  │
│     │ Intent  │  │  SQL    │  │Explainer│                  │
│     │ Agent   │  │Generator│  │ Agent   │                  │
│     └─────────┘  └────┬────┘  └─────────┘                  │
│                       │                                     │
│                  ┌────▼────┐                                │
│                  │  SQL    │                                │
│                  │  Guard  │                                │
│                  └─────────┘                                │
└──────────────────────────┬──────────────────────────────────┘
                           │
          ┌────────────────┴─────────────────┐
          │                                   │
   ┌──────▼──────┐                   ┌────────▼────────┐
   │  Groq API   │                   │  MS SQL Server  │
   │ LLaMA 3.1   │                   │ AdventureWorks  │
   └─────────────┘                   │   2016 Cloud    │
                                     └─────────────────┘
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
  Execute → Return Results → Save to Cloud DB
```

---

## 📁 Project Structure

```
SmartQuery/
│
├── app/
│   ├── templates/
│   │   ├── index.html         # 🏠 Main chat interface
│   │   ├── history.html       # 🕑 Query history page
│   │   └── about.html         # ℹ️  About page
│   │
│   ├── config.py              # 🔧 Groq API keys & model config
│   ├── db.py                  # 🗄️  MS SQL Server connection & executor
│   ├── llm_client.py          # 🤖 Unified LLM API caller
│   ├── main.py                # 🚀 FastAPI app entry point
│   ├── orchestrator.py        # 🎼 Pipeline coordinator
│   ├── prompt.py              # 📝 Master T-SQL prompt template
│   ├── schema_loader.py       # 🔍 Dynamic schema builder
│   ├── sql_guard.py           # 🛡️  Rule-based SQL safety firewall
│   ├── intent.py              # 🎯 Intent classification agent
│   ├── generator.py           # ⚙️  SQL generation agent
│   └── explainer.py           # 📖 SQL explanation agent
│
├── requirements.txt           # 📦 Python dependencies
├── .env                       # 🔐 Environment variables (not committed)
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
| **Database** | MS SQL Server 2016 | AdventureWorks 2016 data |
| **DB Driver** | pymssql | Python ↔ SQL Server connector |
| **Hosting** | Render (Free Tier) | Live deployment |
| **Cloud DB** | FreeASPHosting | Cloud SQL Server hosting |
| **Config** | python-dotenv | Environment variable management |
| **Server** | Uvicorn | ASGI production server |

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/SONURAY0900/-SmartQuery.git
cd -SmartQuery
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Groq API Key — get yours free at https://console.groq.com
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx

# MS SQL Server password
DB_PASSWORD=your_database_password
```

### 4. Run the Server

```bash
uvicorn app.main:app --reload
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
  "data": [{ "Name": "Mountain-200 Black", "Revenue": 4352820.77 }],
  "explanation": "Joins Product to SalesOrderDetail, sums revenue per product..."
}
```

**Response (off-topic)**
```json
{
  "status": "error",
  "message": "I can only answer questions about AdventureWorks data."
}
```

---

### `GET /api/history`
Retrieve the last 100 query history entries.

### `DELETE /api/history`
Clear all query history.

### `GET /` — Home page
### `GET /about` — About page
### `GET /history` — History page

---

## 🛡️ SQL Guard System

The `sql_guard.py` module is a rule-based firewall that runs on **every generated query** before execution.

| Rule | Protection |
|---|---|
| 🚫 **Destructive Keywords** | Blocks `DELETE`, `UPDATE`, `INSERT`, `DROP`, `ALTER`, `TRUNCATE` |
| 🚫 **MySQL Backticks** | Rejects queries with backticks (not valid T-SQL) |
| 🚫 **Fake `ProductName`** | Forces use of `Production.Product.Name AS ProductName` |
| 🚫 **`EmployeeID` Column** | Enforces `BusinessEntityID` (AdventureWorks standard) |
| 🚫 **Hallucinated Columns** | Blocks invented columns like `Brand`, `ModelNumber` |

If a guard check fails, the orchestrator triggers one **auto-repair pass** — feeding the error back to the generator for a corrected query.

---

## 🗄️ Database Schema

**AdventureWorks 2016 — Supported Domains:**

```
📦  Production     →  Product, ProductSubcategory, ProductCategory
💰  Sales          →  SalesOrderHeader, SalesOrderDetail, Customer
👤  Person         →  Person (names for Employees & Customers)
🧑‍💼  HumanResources →  Employee, EmployeeDepartmentHistory, Department
🏭  Purchasing     →  Vendor, PurchaseOrderHeader
```

> Schema is loaded dynamically from `INFORMATION_SCHEMA.COLUMNS` on every request — always up-to-date.

---

## 📸 Pages Overview

| Page | Route | Description |
|---|---|---|
| 🏠 **Home** | `/` | Main chat interface — type questions, see results |
| 🕑 **History** | `/history` | Browse past queries with full SQL and results |
| ℹ️ **About** | `/about` | Project info, pipeline explanation, tech stack |

---

## 🗺️ Roadmap

- [ ] 📊 Chart rendering for aggregate results
- [ ] 📤 CSV / Excel export for query results
- [ ] 🔐 User authentication & per-user history
- [ ] 🗃️ Support multiple database schemas
- [ ] 🐳 Docker deployment config

---

<div align="center">

Built by **Sonu Ray** · Internship Project @ Astro Vedangam Pvt. Ltd.

Made with ❤️ using **FastAPI** · **Groq** · **LLaMA 3.1** · **SQL Server**

*If this project helped you, consider giving it a ⭐*

</div>
