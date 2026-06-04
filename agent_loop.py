import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv(override=True)

client = Anthropic()

def calculator(operation, a, b):
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b
    else:
        return "unknown operation"

tools = [
    {
        "name": "calculator",
        "description": "Performs basic arithmetic. Use this for any math calculation rather than computing it yourself.",
        "input_schema": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "The arithmetic operation to perform.",
                },
                "a": {"type": "number", "description": "The first number."},
                "b": {"type": "number", "description": "The second number."},
            },
            "required": ["operation", "a", "b"],
        },
    }
]

messages = [
    {"role": "user", "content": "Multiply 347 by 29, then subtract 63 from the result."}
]

# First call to start things off
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    tools=tools,
    messages=messages,
)

# THE LOOP: keep going as long as Claude keeps asking for tools
max_iterations = 10
iterations = 0
while response.stop_reason == "tool_use" and iterations < max_iterations:

    iterations += 1

    # Append Claude's tool-request turn to the conversation
    messages.append({"role": "assistant", "content": response.content})

    # There may be one or more tool requests in this turn.
    # We collect a result for each one.
    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            print("Claude wants:", block.name, block.input)
            result = calculator(
                block.input["operation"],
                block.input["a"],
                block.input["b"],
            )
            print("  -> result:", result)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": str(result),
            })

    # Send all the results back as one user turn
    messages.append({"role": "user", "content": tool_results})

    # Call the API again. Its response becomes the new loop condition.
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )

# Loop has exited: Claude stopped asking for tools.
print("\nFinal answer:")
print(response.content[0].text)
