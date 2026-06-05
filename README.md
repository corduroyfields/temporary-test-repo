# Learning to Build AI Agents

A from-scratch project where I learned how AI agents actually work by building one, one mechanic at a time, instead of starting with a framework that hides the details.

## Why this exists

I wanted hands-on understanding of how an LLM uses tools and chains actions, not just the ability to wire up someone else's library. So I built up from a single API call to a working agent loop, committing each stage separately so the progression is visible. The code is deliberately simple. The goal was to understand each stage of the workflow and execute a functioning agent.

## What's here

The repo has three scripts, each a checkpoint in the progression:

**`hello_claude.py`** - A single call to the Claude API. Sends one message, prints the reply. This is the foundation: API keys, the SDK, and the request/response shape.

**`calculator_agent.py`** - A single tool-use handoff. Claude is given a calculator tool, decides to call it, my code runs the function, and the result goes back to Claude for a final answer. This is one round of tool use, not a loop. It demonstrates the core mechanic: Claude decides, my code executes, Claude responds.

**`agent_loop.py`** - The agent loop. The tool handoff is wrapped in a `while` loop so Claude can chain multiple tool calls until the task is done. Given a two-step problem, Claude calls the calculator, reads the result, then decides on its own to call it again. A simple iteration cap keeps the loop from running away.

## How to run it

Requires Python 3.9 or later and an Anthropic API key.

1. Clone the repo and enter the folder.
2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install anthropic python-dotenv
```

4. Create a `.env` file with your key:

```
ANTHROPIC_API_KEY=your-key-here
```

5. Run any of the scripts, for example:

```bash
python agent_loop.py
```

The `.env` file is gitignored and never committed.

## What I'd add for production

This is a learning build, not production code. To harden it I would add: real error handling around the API calls and tool execution, logging when the iteration cap is hit, support for multiple tools beyond the calculator, validation of the tool inputs before running them, and tests. The iteration cap is currently a fixed number; in a real system it would be tuned and monitored.

## A note on how this was built

I built this with Claude as a programming assistant while learning the mechanics. I drove the work, made the decisions, and wrote the commits; Claude coached, explained the concepts, and helped me debug. I have noted this openly because working effectively with AI tooling is part of the skill set I am building, and because I would rather be straightforward about my process than imply I did it in isolation. I am not a developer by trade, and I have limited experience writing code.
