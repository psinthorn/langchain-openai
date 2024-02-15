import sqlite3
from langchain.tools import Tool

# 1. สร้าง connection database ในกรณีนี้เป็น sqlite3
# 2. สร้าง function cursor สำหรับ execute คำสั่ง sql

# สร้าง connection ไปยัง database
conn = sqlite3.connect('db.sqlite') 

# สร้าง function สำหรับ list ชื่อตารางที่มีใน database
def list_tables():
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = cursor.fetchall()
    return "\n".join(row[0] for row in rows if row[0] is not None)

    # or you can return cursor.fetchall() directly not need to create rows variable
    # return cursor.fetchall()

def run_sqlite_query(query):
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.OperationalError as err:
        return f"The following error is occured: {err}"
    
# สร้าง tool จาก function run_sqlite_query
run_query_tool = Tool.from_function(
    name = 'run_sqlite_query',
    description = 'Run a query on a sqlite database',
    func = run_sqlite_query
) 

def describe_table(table_names):
    cursor = conn.cursor()
    tables = ", ".join("'" + table + "'" for table in table_names)
    rows = cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' and name IN ({tables})")
    return "\n".join(row[0] for row in rows if row[0] is not None)

describe_tables_tool = Tool.from_function(
    name = 'describe_tables',
    description = 'Describe the schema of a table',
    func = describe_table
)