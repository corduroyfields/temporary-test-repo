# Project Handover

Purpose: context for a new chat so it can pick up without re-deriving everything. Two parts: what was already built (first AI agent), and what comes next (Livability scoring pipeline).

---

## Part 1: What was built (completed)

### First AI agent, from scratch, for learning + portfolio

A public GitHub repo built one mechanic at a time, with Claude coaching and me driving. Goal was hands-on understanding of how agents work, plus a portfolio artifact for employers. I am a non-engineer (TAM / Solutions Consultant background); the code is deliberately simple.

Three scripts, each a checkpoint:

1. `hello_claude.py` — a single Claude API call. Foundation: API keys, the SDK, request/response shape.
2. `calculator_agent.py` — a single tool-use handoff. Claude decides to call a calculator tool, my code runs it, the result goes back, Claude gives the final answer. One round, no loop. Demonstrates the core mechanic: Claude decides, my code executes, Claude responds.
3. `agent_loop.py` — the agent loop. The tool handoff wrapped in a `while` loop so Claude can chain multiple tool calls until done. Includes a simple iteration cap (max 10) as a runaway guardrail.

A README written for the employer audience tells the progression and includes an honest statement that the build was done with Claude as a pair-programming assistant.

### Environment / setup facts (carry these forward)

- Python: system Python was 3.8 (too old); the project uses a virtual environment built with Python 3.13. **Must activate the venv each new terminal session:** `source venv/bin/activate`. The `(venv)` prefix in the prompt confirms it is active. The most common "module not found" error is just a forgotten activation.
- API key lives only in `.env`, loaded with `load_dotenv(override=True)`. `.gitignore` covers `.env`, `__pycache__/`, `.DS_Store`, and `venv/`. The key never appears in code or in chat. (One key was exposed and rotated during setup; the rule now is: key only ever in `.env`, never pasted into a chat.)
- Git identity is configured with a GitHub noreply email so commits attribute correctly without exposing a personal address.
- Tooling split that worked well: **terminal** for running `python ...` commands (where venv is active and output is visible); **Claude Code** for editing files and git operations.
- Model used for learning: `claude-haiku-4-5-20251001` (cheapest; correct for plumbing/loops, not reasoning quality).

### Key learning conventions (keep these)

- Label every command with where it runs: **[TERMINAL]** or **[CLAUDE CODE]**. Do not assume I know which.
- Coach-and-drive: one beat at a time, I run it, I paste the result back. Verify each small step before moving on (e.g., a quick syntax-load check after each edit).
- Keep working files intact as milestones; build new steps in new files rather than overwriting.

---

## Part 2: What comes next (the next project)

### The app: Livability Recommendation App

A personalized "best places to live in the USA" app. Full design spec exists in Google Drive: **`Livability_App_Framework_and_MVP_Spec`** (Google Doc, owner corduroyfields@gmail.com). The new chat should read that doc first; everything below is a summary, the doc is the source of truth.

Core design (three-layer model):
- **Layer 1 Disqualifiers** — hard filters that remove places (set via optional toggle in the quiz).
- **Layer 2 Preferences** — soft match to who the user is (quiz). Person-properties with no universal "better" (city size, climate type, political leaning, etc.).
- **Layer 3 Factors** — objective place quality, weighted by a user stack-rank (~11 factors: Housing, Cost of Living, Economy, Jobs, Education, Health, Safety, Amenities, Transportation, Environment, Infrastructure).
- Final recommendation = places surviving Layer 1, ranked by a blend of Layer 2 match score and Layer 3 weighted quality score, with an AI agent generating a plain-language rationale.

The six-stage user workflow has been modeled in Miro already (board exists; faithfully represents spec section 5). **The Miro board is considered done** and serves as interview substance, not further build work.

### Why this is the next step (and not more Miro work)

Per the spec's own build order (section 8), step 1 was "model the workflow in Miro" — done. **Step 2 is: hand the data model and scoring pipeline to Claude Code and scaffold the pure scoring functions, unit-tested against a small seeded dataset.** That is the next build target.

Rationale: it is a genuine difficulty step up from the agent work (structured data, a scoring pipeline, unit tests), it builds directly on existing Python skills, and critically it does **not** require the Miro MCP or OAuth. (Calling Miro's MCP from my own code requires OAuth 2.1, which we are deliberately deferring as too much under interview-week time pressure. Miro's MCP connection from Claude Code already works for writing to an existing board; free-tier limits board *creation* to 3 boards.)

### The next project, scoped

**Build the thin-slice scoring pipeline as pure, unit-tested Python functions.** From spec section 6:

```
filter(places, disqualifiers)      -> candidates
cluster(candidates, preferences)   -> cohort
normalize(cohort.factor_scores)    -> z-scores
matchScore(place, preferences)     -> 0..1        (Layer 2)
qualityScore(place_z, factor_weights) -> number   (Layer 3)
finalScore = blend(matchScore, qualityScore)
explain(place, profile)            -> rationale   (AI agent; the AI-skills core)
```

Suggested approach for the new chat:
1. Read the spec doc first.
2. Create a small seeded dataset (~10-20 cities to start, not the full 50-100) with hand-entered sample factor values, matching the `Place` entity in spec section 6.
3. Build the pure functions one at a time (`filter` first), with a unit test for each before moving on. Same coach-and-drive, one-beat-at-a-time rhythm.
4. Save it as a new file in the same repo (e.g., `livability_pipeline.py` + a test file). Keep the agent scripts untouched.
5. The `explain()` function is where the agent skills come back in — it is a Claude call that reasons over a scored place and produces a rationale. Save this for last.

Open design decisions from the spec to settle when relevant (not blockers to start): blend ratio (start 50/50), cohort vs absolute scoring (use cohort), how many factors to rank (consider top-5 instead of all 11), data-confidence threshold.

### Scope discipline (important)

The temptation is to build the whole app. Do not. The MVP is explicitly: seeded data, no backend, no storage, prove the matching loop end to end. UI and the full feedback loop come later. Start with the pure scoring functions and their tests — smallest thing that demonstrates the core loop.

### Writing-rules reminder (for any written deliverable, e.g. a README for this project)

No em dashes. Avoid AI-writing tells (consult `signs-of-ai-writing.md` in Google Drive). Concise, direct prose; sentence-case headings; no rule-of-three list constructions; no inflated-significance phrasing. Be straightforward about AI assistance rather than hiding it.
