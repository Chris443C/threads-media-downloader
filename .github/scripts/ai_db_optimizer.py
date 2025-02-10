import openai
import os

# Configure OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define database files to optimize
db_files = ["src/database.py", "src/db_queries.sql"]

for file in db_files:
    print(f"Optimizing: {file}")

    # Read file content
    with open(file, "r") as f:
        code = f.read()

    # Generate optimized SQL queries using AI
    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=f"Optimize this SQL for performance:\n{code}\n\nOptimized Query with Indexes:",
        max_tokens=500
    )

    optimized_code = response["choices"][0]["text"].strip()

    # Save the optimized SQL
    with open(file, "w") as f:
        f.write(optimized_code)

    print(f"✅ Optimization Applied to {file}")
