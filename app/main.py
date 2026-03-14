from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
import logging
from datetime import datetime

from app.orchestrator import orchestrate
from app.db import execute_sql, get_connection

logger = logging.getLogger(__name__)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FIX TEMPLATE PATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


# ---------------- HISTORY DB FUNCTIONS ----------------
def save_history(query: str, sql: str, row_count: int, status: str, data: list = None):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        result_data = json.dumps(data or [], default=str)
        cursor.execute(
            """
            INSERT INTO dbo.QueryHistory (UserQuery, GeneratedSQL, TotalRows, Status, ResultData)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (query, sql, row_count, status, result_data)
        )
        conn.commit()
        conn.close()
    except Exception:
        logger.exception("Failed to save history to database")


def load_history():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT TOP 100 Id, Timestamp, UserQuery, GeneratedSQL, TotalRows, Status, ResultData
            FROM dbo.QueryHistory
            ORDER BY Timestamp DESC
            """
        )
        rows = cursor.fetchall()
        conn.close()
        entries = []
        for row in rows:
            try:
                data = json.loads(row[6]) if row[6] else []
            except Exception:
                data = []
            entries.append({
                "id": row[0],
                "timestamp": row[1].strftime("%Y-%m-%d %H:%M:%S") if row[1] else "",
                "query": row[2] or "",
                "sql": row[3] or "",
                "row_count": row[4] or 0,
                "status": row[5] or "",
                "data": data
            })
        return entries
    except Exception:
        logger.exception("Failed to load history from database")
        return []


def clear_history_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM dbo.QueryHistory")
        conn.commit()
        conn.close()
    except Exception:
        logger.exception("Failed to clear history from database")


class QueryRequest(BaseModel):
    userquery: str


# ---------------- HOME PAGE ----------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ---------------- ABOUT PAGE ----------------
@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


# ---------------- HISTORY PAGE ----------------
@app.get("/history", response_class=HTMLResponse)
def history_page(request: Request):
    return templates.TemplateResponse("history.html", {"request": request})


# ---------------- HISTORY API ----------------
@app.get("/api/history")
def get_history():
    return {"entries": load_history()}


@app.delete("/api/history")
def clear_history():
    try:
        clear_history_db()
        return {"status": "cleared"}
    except Exception:
        logger.exception("Failed to clear history")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "Could not clear history."}
        )


# ---------------- ASK ENDPOINT ----------------
@app.post("/ask")
def ask(req: QueryRequest):
    try:
        result = orchestrate(req.userquery)

        sql = result.get("sql", "").strip()
        explanation = result.get("explanation", "")

        if not sql.lower().startswith("select"):
            save_history(req.userquery, sql, 0, "error")
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": explanation or "Could not generate a valid query for your question."
                }
            )

        data = execute_sql(sql)
        save_history(req.userquery, sql, len(data), "success", data)

        return {
            "status": "success",
            "sql": sql,
            "data": data,
            "explanation": explanation
        }

    except Exception as e:
        logger.exception("Unhandled error in /ask endpoint")
        save_history(req.userquery, "", 0, "error")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Something went wrong on our end. Please try again."
            }
        )


# ---------------- FAVICON ----------------
@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)