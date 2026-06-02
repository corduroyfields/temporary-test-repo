import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load the key from .env into the environment
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"), override=True)

# Create the client (it reads ANTHROPIC_API_KEY automatically)
client = Anthropic()

# Send one message to Claude
message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude! Reply in one short sentence."}
    ],
)

# Print just the text of the reply
print(message.content[0].text)
