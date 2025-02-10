import openai
import os

# Configure OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define files to optimize
files_to_optimize = ["src/threads_downloader.py", "src/database.py"]

for file in files_to_optimize:
    print(f"Optimizing: {file}")

    # Read file content
    with open(file, "r") as f:
        code = f.read()

    # Generate optimized code using AI
    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=f"Optimize this Python code for performance:\n{code}\n\nOptimized Code:",
        max_tokens=500
    )

    optimized_code = response["choices"][0]["text"].strip()

    # Save the optimized code
    with open(file, "w") as f:
        f.write(optimized_code)

    print(f"✅ Optimization Applied to {file}")
