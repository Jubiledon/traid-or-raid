# Trade or Raid: Language and Strategy in Competing LLM Agents

This project simulates competing LLM-powered agents in a shared grid world. Agents collect resources and optionally raid rivals, with or without natural language communication enabled. Three core agent types are compared across multiple experimental conditions.

---

## Setup

### 1. Install dependencies

```bash
pip install anthropic pygame numpy pandas matplotlib python-dotenv
```

### 2. Create a `.env` file

In the root of the project, create a file named `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your-api-key-here
```

The project will not run LLM conditions without this key.

---

## Running Experiments

All experiments are run via `main.py`. The flags are:

| Flag | Description |
|------|-------------|
| `-t` | Number of trials |
| `-a` | Number of agents |
| `-H` | Headless mode (no display, required for bulk runs) |
| `-T` | Agent type (`simple` or `llm`) |
| `-c` | Condition name (used for logging) |

### Replicate the reported experiments

Run each command separately. Results are saved to CSV automatically.

```bash
# Rule-based baseline
python main.py -t 30 -a 4 -H -T simple -c simple

# LLM agents, communication disabled
python main.py -t 30 -a 4 -H -T llm -c llm_silent

# LLM agents, communication enabled, random personality mix
python main.py -t 30 -a 4 -H -T llm -c llm_comms

# LLM agents, communication enabled, mixed personalities
python main.py -t 30 -a 4 -H -T llm -c llm_comms_mixed

# LLM agents, communication enabled, cooperative personalities only
python main.py -t 30 -a 4 -H -T llm -c llm_comms_coop

# LLM agents, communication enabled, aggressive personalities only
python main.py -t 30 -a 4 -H -T llm -c llm_comms_aggr
```

To watch the simulation live (single trial, with display), remove the `-H` flag and set `-t 1`.

---

## Output

Each run produces per-trial CSV files in `logs/runs/<condition>/` and an aggregated summary in `logs/summaries/`. These contain per-trial metrics including collective efficiency, raid count, broadcast count, and per-agent inventory scores. Figures are saved to `figures/` when running `analysis/plots.py`.

---

## Project Structure

```
.
+-- main.py                        # Entry point
+-- config.py                      # Shared configuration constants
+-- agents/
|   +-- agent.py                   # Agent data class
|   +-- brains.py                  # SimpleBrain and LLMBrain implementations
|   +-- llm_client.py              # Anthropic API client wrapper
|   +-- percept_filter.py          # Strips communication from silent agent percepts
|   +-- personalities.py           # Personality prompt definitions
|   +-- prompt_builder.py          # Builds natural language prompts from percepts
|   +-- response_parser.py         # Parses LLM output into structured actions
+-- simulation/
|   +-- conditions.py              # Condition definitions (simple, llm_silent, etc.)
|   +-- experiment_config.py       # Experiment configuration dataclass
|   +-- experiment_runner.py       # Runs trials and aggregates results
|   +-- metrics.py                 # Collective efficiency and other metrics
|   +-- simulation_runner.py       # Single episode loop
|   +-- turn_manager.py            # Per-tick agent ordering and action dispatch
+-- world/
|   +-- world.py                   # Grid world state
|   +-- action_resolver.py         # Applies actions to world state
|   +-- percept_builder.py         # Builds agent percepts from world state
|   +-- raid_resolver.py           # Raid logic and inventory transfer
|   +-- resource_manager.py        # Resource placement and collection
|   +-- movement.py                # Agent movement and collision checks
|   +-- spawning.py                # Agent initialisation and placement
|   +-- logger.py                  # Per-tick CSV event logging
|   +-- metrics.py                 # World-level metric helpers
|   +-- actions.py                 # Action type definitions
+-- rendering/
|   +-- renderer.py                # Pygame display (skipped in headless mode)
|   +-- ui_panel.py                # Sidebar panel for scores and messages
|   +-- colours.py                 # Colour constants
+-- cli/
|   +-- arguments.py               # CLI argument parsing
+-- analysis/
|   +-- plots.py                   # Generates figures from CSV logs
|   +-- find_interesting.py        # Identifies notable episodes for qualitative analysis
+-- logs/
|   +-- runs/                      # Per-trial CSV logs, organised by condition
|   +-- summaries/                 # Aggregated summary CSVs per condition
+-- figures/                       # Generated plots used in the report
+-- .env                           # API key (not committed)
```

---

## Notes

- LLM conditions use the Anthropic API (Claude Haiku). Running all conditions costs a small amount in API credits. The `simple` condition uses no API calls.
- Headless mode (`-H`) disables Pygame entirely and is recommended for replication.
- Trials use random initialisation with no fixed seed. Results will vary slightly from those reported, but should be consistent in direction across 30 trials.
