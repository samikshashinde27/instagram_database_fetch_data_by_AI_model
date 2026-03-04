

## Project Explanation Document

To make sure this entire process finishes within 5 seconds, I used these optimizations:

1. Database connection pooling – The system keeps the database connection ready instead of creating a new one every time. This saves time.

2. Schema loaded once – The database structure is loaded only once at the start, so it does not repeatedly fetch it.

3. Only SELECT queries allowed – This prevents heavy operations like INSERT, UPDATE, DELETE that could slow down the system.

4. LIMIT 100 added automatically – This ensures the system does not return too many rows, which keeps responses fast.

5. Query validation before execution – Invalid or unsafe queries are stopped early to avoid wasting time.

6. Maximum 3 retries for AI – This prevents the system from running too long if the model makes mistakes.

These steps help reduce unnecessary processing and database load, ensuring that the query response time stays within 5 seconds.


## 1. Project Overview

This project is a **Natural Language to SQL (NLQ) Engine**.

It allows a user to:

* Ask questions in plain English
* Automatically convert them into a MySQL SELECT query
* Execute the query on a database
* Display the results

The system uses:

* **Ollama (LLM Model – llama3)** for generating SQL
* **SQLAlchemy** for database connection
* **MySQL 8** as the database

---

# Function-by-Function Explanation

---

## 2. Database Connection Setup

```python
engine = create_engine(DB_URL, pool_pre_ping=True)
inspector = inspect(engine)
```

### Purpose:

This section creates a connection to the MySQL database.

### What it does:

* `create_engine()` connects to the database using the given DB_URL.
* `pool_pre_ping=True` ensures the connection is alive before using it.
* `inspect(engine)` allows reading database structure (tables & columns).

If connection fails, it prints an error and stops execution.

---

## 3. load_schema()

```python
def load_schema():
```

### Purpose:

Loads database structure information (schema).

### What it does:

1. Gets all table names from the database.
2. For each table:

   * Gets all column names and their data types.
3. Stores this information as a formatted string.
4. Returns the complete schema information.

### Why it is needed:

The schema is given to the AI model so it:

* Uses only existing tables
* Uses only valid columns
* Avoids generating incorrect queries

---

## 4. validate_query_tables(sql_query)

```python
def validate_query_tables(sql_query):
```

### Purpose:

Security validation for generated SQL queries.

### What it does:

1. Gets allowed tables from the database.
2. Extracts table names used in:

   * FROM clause
   * JOIN clause
3. Checks if all tables used in the query exist in the database.
4. If not, raises an exception.

### Why it is important:

* Prevents unauthorized table access
* Adds basic SQL injection protection
* Improves system security

---

## 5. execute_sql(query, test_only=False)

```python
def execute_sql(query, test_only=False):
```

### Purpose:

Executes SQL query on the database.

### What it does:

* Opens database connection
* Executes the SQL query
* If `test_only=True`, it only validates query (does not fetch data)
* If `test_only=False`, it returns all rows

### Why test_only is used:

Before running a query fully, the system checks if it runs without error.

---

## 6. generate_sql(user_input)

```python
def generate_sql(user_input):
```

### Purpose:

Converts user English question into a valid MySQL SELECT query.

### Step-by-step Working:

### Step 1: Create AI Prompt

The system sends instructions to the model:

* Only generate SELECT queries
* Do not use INSERT, UPDATE, DELETE
* Always end with semicolon
* Add LIMIT 100 if missing
* Use only provided schema

---

### Step 2: Call AI Model

```python
response = ollama.chat(
    model="llama3",
    messages=messages
)
```

The llama3 model generates SQL based on:

* Schema information
* User request

---

### Step 3: Extract SQL from Model Output

Using regex:

```python
match = re.search(r"(SELECT[\s\S]+?;)", raw_output, re.IGNORECASE)
```

This ensures:

* Only SELECT statement is captured
* Query ends with semicolon

---

### Step 4: Security Checks

* Ensures query starts with SELECT
* Adds LIMIT 100 if missing
* Validates table names
* Runs test execution

---

### Step 5: Auto Error Correction

If SQL fails:

* The error message is sent back to the AI
* AI attempts to fix the query
* Maximum 3 attempts allowed

---

## 7. Main Program Execution

```python
if __name__ == "__main__":
```

### Purpose:

Runs the interactive system.

### How it works:

1. User types question
2. System generates SQL
3. SQL is validated
4. SQL is executed
5. Results are displayed
6. User can type "exit" to stop

---

# Overall System Flow

User Question
↓
AI Generates SQL
↓
Security Validation
↓
Test Execution
↓
Final Execution
↓
Results Displayed

---

# Key Features of the System

✔ Converts English to SQL
✔ Restricts to SELECT queries only
✔ Prevents dangerous SQL commands
✔ Auto-corrects invalid queries
✔ Limits output to 100 rows
✔ Validates table access

---

# Technologies Used

* Python
* Ollama (LLM – llama3)
* SQLAlchemy
* MySQL 8
* Regex (for validation)

---

# Conclusion

This system acts as an intelligent database assistant that:

* Allows non-technical users to query databases
* Automates SQL generation
* Maintains security restrictions
* Ensures controlled database access

It can be extended into:

* REST API service
* Chatbot integration
* Admin dashboard reporting tool
* Enterprise analytics system

---

