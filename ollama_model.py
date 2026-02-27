import ollama
import re
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError

DB_URL = "mysql+pymysql://TEST_USER:TEST_USER@holistique-middleware.c9wdjmzy25ra.ap-south-1.rds.amazonaws.com:3306/TEST"

try:
    engine = create_engine(DB_URL, pool_pre_ping=True)
    inspector = inspect(engine)
except Exception as e:
    print("Database connection failed:")
    print(e)
    raise e


def load_schema():
    schema_info = ""
    tables = inspector.get_table_names()

    for table in tables:
        columns = inspector.get_columns(table)
        column_details = [f"{col['name']} ({col['type']})" for col in columns]
        schema_info += f"\nTable: {table}\nColumns: {column_details}\n"
    return schema_info

try:
    SCHEMA_INFO = load_schema()
except Exception as e:
    print("Failed to load schema:")
    raise e  


def validate_query_tables(sql_query):
    allowed_tables = set(inspector.get_table_names())
    found_tables = re.findall(r'from\s+([a-zA-Z0-9_]+)', sql_query, re.IGNORECASE)
    found_tables += re.findall(r'join\s+([a-zA-Z0-9_]+)', sql_query, re.IGNORECASE)
    for table in found_tables:
        if table not in allowed_tables:
            raise Exception(f"Unauthorized table detected: {table}")


def execute_sql(query, test_only=False):
    with engine.connect() as conn:
        result = conn.execute(text(query))
        if test_only:
            return
        return result.fetchall()


def generate_sql(user_input):
    base_prompt = f"""
You are a MySQL 8 expert.

STRICT RULES:
- Generate only SELECT queries.
- Use only tables and columns provided below.
- Never generate INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE.
- Always end query with semicolon.
- If LIMIT is missing, add LIMIT 100.
- Return SQL only.
- Do not explain.

Database Schema:
{SCHEMA_INFO}

User Request:
{user_input}
"""
    messages = [{"role": "system", "content": base_prompt}]
    for attempt in range(3):
        messages.append({"role": "user", "content": user_input})
        response = ollama.chat(
            # model="qwen2.5:14b",
            model="llama3",
            messages=messages,
            # options={"temperature": 0, "top_p": 0.9}
        )
        raw_output = response["message"]["content"].strip()
        match = re.search(r"(SELECT[\s\S]+?;)", raw_output, re.IGNORECASE)
        if not match:
            raise Exception("Model did not generate valid SQL.")
        sql_query = match.group(0).strip()

        if not sql_query.lower().startswith("select"):
            raise Exception("Only SELECT queries allowed.")

        if "limit" not in sql_query.lower():
            sql_query = sql_query.rstrip(";") + " LIMIT 100;"

        validate_query_tables(sql_query)

        try:
            execute_sql(sql_query, test_only=True)
            return sql_query
        except Exception as e:
            messages.append({"role": "assistant", "content": sql_query})
            messages.append({
                "role": "user",
                "content": f"""
The previous SQL failed with error:
{str(e)}

Fix the query using valid MySQL 8 syntax.
Return only corrected SQL.
"""
            })

    raise Exception("Failed after multiple attempts.")


if __name__ == "__main__":
    print("Advanced MySQL NLQ Engine Ready (Qwen2.5)")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Ask something: ")
        if user_input.lower() == "exit":
            print("Exiting...")
            break
        try:
            print("\nGenerating SQL...")
            sql_query = generate_sql(user_input)
            print("\nGenerated SQL:")
            print(sql_query)
            print("\n Executing...")
            rows = execute_sql(sql_query)
            print(f"\n Rows Returned: {len(rows)}\n")
            for row in rows:
                print(row)
            print("\n" + "-" * 60 + "\n")
        except Exception as e:
            print("Error:", e)
            print("\n" + "-" * 60 + "\n")