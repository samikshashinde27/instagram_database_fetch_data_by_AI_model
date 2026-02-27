We have created a virtual environment for that code.
===========================================================
NATURAL LANGUAGE TO SQL ENGINE
Simple Client Documentation
===========================================================

1. OVERVIEW
-----------------------------------------------------------
This system allows users to query a MySQL database using 
plain English instead of writing SQL queries manually.

Users can type questions like:
- Show all customers
- Get last 10 orders
- How many users are registered?

The system automatically:
1. Converts the question into a SQL query
2. Checks if the query is safe
3. Executes it on the database
4. Returns the results


2. HOW THE SYSTEM WORKS
-----------------------------------------------------------

Step 1 – User Input
The user types a question in natural language.

Step 2 – AI Converts to SQL
An AI model generates a SQL SELECT query using:
- Database schema information
- Strict safety rules

Step 3 – Query Validation
The system checks:
- Only SELECT queries are allowed
- No INSERT, UPDATE, DELETE, DROP, ALTER
- Only existing database tables are used
- LIMIT 100 is added if missing

Step 4 – Execution
The validated SQL query is executed on the MySQL database.

Step 5 – Results
The system returns and displays the query results.


3. KEY FEATURES
-----------------------------------------------------------

- Natural language querying (No SQL knowledge required)
- Secure read-only access (SELECT only)
- Schema-aware AI to reduce errors
- Automatic error correction (Retries up to 3 times)
- Default LIMIT to protect database performance


4. SECURITY CONTROLS
-----------------------------------------------------------

The system prevents:

- Data deletion
- Data updates
- Schema modifications
- Unauthorized table access
- Large unbounded queries

This ensures the database remains safe at all times.


5. TECHNOLOGY STACK
-----------------------------------------------------------

- Python
- SQLAlchemy (Database connection & execution)
- MySQL 8
- Ollama LLM (LLaMA3 / Qwen models)
- Regex validation for table checking


6. LIMITATIONS
-----------------------------------------------------------

- Only SELECT queries are supported
- Maximum 100 rows returned by default
- Query accuracy depends on AI model quality


7. IDEAL USE CASES
-----------------------------------------------------------

- Internal reporting tools
- Business dashboards
- Admin panels
- Customer support systems
- Non-technical database access



===========================================================
ADVANCED MYSQL NLQ API
Simple Documentation
===========================================================

1. OVERVIEW
-----------------------------------------------------------
This API allows users to send a natural language question 
(plain English) and receive:

1. The generated SQL SELECT query
2. The query results from the database

It connects to the previously built NLQ (Natural Language 
to SQL) engine and exposes it as a REST API using FastAPI.


2. TECHNOLOGY USED
-----------------------------------------------------------
- Python
- FastAPI (API framework)
- Pydantic (Request/Response validation)
- Ollama-based SQL generator
- SQL execution module


3. HOW THE API WORKS
-----------------------------------------------------------

Step 1 – Client Sends Request
A POST request is sent to:

    /generate_sql

With JSON body:

{
    "user_input": "Show all customers"
}

Step 2 – SQL Generation
The API calls:

    generate_sql(user_input)

This function:
- Converts natural language into a SELECT SQL query
- Applies safety rules

Step 3 – SQL Execution
The API calls:

    execute_sql(sql_query)

This:
- Executes the query on MySQL
- Fetches the results


4. API ENDPOINTS
-----------------------------------------------------------

1) GET /
-----------------------------------------------------------
Purpose:
Check if API is running.

Response:
{
    "message": "Advanced MySQL NLQ API is running!"
}


2) POST /generate_sql
-----------------------------------------------------------
Purpose:
Generate and execute SQL from natural language.

Request Body:
{
    "user_input": "Your question here"
}

Response:
{
    "sql_query": "Generated SQL query",
    "rows": [List of result rows]
}


5. REQUEST MODEL
-----------------------------------------------------------

NLQRequest:
- user_input (string)
  The natural language question.


6. RESPONSE MODEL
-----------------------------------------------------------

SQLResponse:
- sql_query (string)
  The generated SQL SELECT statement.
  
- rows (List of List)
  Query results returned from the database.


7. ERROR HANDLING
-----------------------------------------------------------

If SQL generation or execution fails:
- The API returns an empty SQL string
- The API returns an empty rows list

If an unexpected error occurs:
- The API returns HTTP 400
- Error details and traceback are included


8. INTERNAL FLOW SUMMARY
-----------------------------------------------------------

Client → FastAPI → generate_sql() → execute_sql() → Response


9. SECURITY NOTES
-----------------------------------------------------------

- Only SELECT queries are allowed (enforced in generator)
- No INSERT, UPDATE, DELETE, DROP allowed
- Safe read-only database access


10. USE CASES
-----------------------------------------------------------

- Frontend dashboard integration
- Chat-based analytics tools
- Admin panels
- Internal reporting systems
- AI-powered database assistants




run queries :

ollama_model.py --------->  python ollama_model.py
route.py ---------> uvicorn route:app --reload

----------------------------------------------------------------------------------------------
example queries we can try on model :

Basic Join Questions
"Get all ads along with their campaign name and objective."

"Show ad name, campaign name, campaign objective, and ad status."

"List all ads with their campaign effective status."

"Fetch ads and their campaign start and stop dates."

🔹 Filter-Based Questions
"Get all ads under campaigns where objective = 'CONVERSIONS'."

"Show ads where campaign effective_status = 'ACTIVE'."

"List ads created after 2024-01-01 with campaign name."

"Fetch ads for client_id = '12345' with campaign run_status = 'PENDING'."

🔹 Aggregation Questions
"Count number of ads per campaign."

"Show campaign name and total ads under each campaign."

"Find campaigns that have more than 10 ads."

🔹 Advanced Join Questions
"Get campaign name, ad name, and creative_id for all ads where campaign buying_type = 'AUCTION'."

"Show campaigns that do not have any ads."
(Requires LEFT JOIN)

"List ads whose campaign is stopped."

"Find latest updated ads with their campaign objective."




