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
    {"role": "user", "content": "What is 347 multiplied by 29?"}
]

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    tools=tools,
    messages=messages,
)

print("Stop reason:", response.stop_reason)
print("Full response content:", response.content)

if response.stop_reason == "tool_use":
    tool_use_block = None
    for block in response.content:
        if block.type == "tool_use":
            tool_use_block = block

    tool_name = tool_use_block.name
    tool_input = tool_use_block.input
    print("Claude wants to call:", tool_name, "with", tool_input)

    result = calculator(
        tool_input["operation"],
        tool_input["a"],
        tool_input["b"],
    )
    print("Our function returned:", result)

    messages.append({"role": "assistant", "content": response.content})
    messages.append({
        "role": "user",
        "content": [
            {
                "type": "tool_result",
                "tool_use_id": tool_use_block.id,
                "content": str(result),
            }
        ],
    })

    final_response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )
    print("\nClaude's final answer:")
    print(final_response.content[0].text)
