# agents/prompt_builder.py

from agents.personalities import PERSONALITY_PROMPTS


class PromptBuilder:

    def build(
        self,
        percept: dict,
        communication_on: bool,
        personality: str,
    ) -> str:

        resources = self._describe_resources(percept)
        agents = self._describe_agents(percept)
        actions = self._valid_actions(percept, communication_on)

        return self._format_prompt(
            percept,
            personality,
            resources,
            agents,
            actions,
        )

    def _describe_resources(self, percept: dict) -> str:
        resources = percept["nearby_resources"]

        if not resources:
            return "none visible"

        return ", ".join(f"({x},{y})" for x, y in resources)

    def _describe_agents(self, percept: dict) -> str:
        agents = percept["nearby_agents"]

        if not agents:
            return "  none nearby"

        lines = [self._agent_line(agent) for agent in agents]

        return "\n".join(lines)

    def _agent_line(self, agent: dict) -> str:
        msg = self._message_fragment(agent)

        return (
            f'  - {agent["id"]} at distance {agent["distance"]}, '
            f'inventory {agent["inventory"]}{msg}'
        )

    def _message_fragment(self, agent: dict) -> str:
        message = agent["last_message"]

        if not message:
            return ""

        return f', said: "{message}"'

    def _valid_actions(
        self,
        percept: dict,
        communication_on: bool,
    ) -> str:

        actions = self._base_actions()
        actions += self._raid_actions(percept)

        if communication_on:
            actions.append("broadcast")

        return " | ".join(actions)

    def _base_actions(self) -> list[str]:
        return [
            "move_N",
            "move_S",
            "move_E",
            "move_W",
            "collect",
            "wait",
        ]

    def _raid_actions(self, percept: dict) -> list[str]:
        agents = percept["nearby_agents"]

        return [
            f'raid_{agent["id"]}'
            for agent in agents
            if agent["distance"] == 1
        ]

    def _format_prompt(
        self,
        percept: dict,
        personality: str,
        resources: str,
        agents: str,
        actions: str,
    ) -> str:

        personality_text = PERSONALITY_PROMPTS[personality]

        return f"""You are {percept["agent_id"]}, an agent in a competitive grid world.
    Personality: {personality_text}

    Tick {percept["tick"]} of 200. Position: {percept["position"]}.
    Your inventory: {percept["inventory"]}. Resources remaining: {percept["resources_remaining"]}.
    Nearby resources: {resources}
    Nearby agents: {agents}

    Your goal: maximise your inventory.

    Respond on ONE line only, starting with ACTION:
    Valid actions: {actions}

    ACTION:"""

#         return f"""
# You are {percept["agent_id"]}, an agent in a competitive grid world.

# Personality:
# {personality_text}

# Current state (tick {percept["tick"]} of 200):
#   Position: {percept["position"]}
#   Your inventory: {percept["inventory"]}
#   Resources remaining: {percept["resources_remaining"]}

# Nearby resources:
# {resources}

# Nearby agents:
# {agents}

# Your goal is to maximise your own inventory.

# Choose EXACTLY one action.

# ACTION: <{actions}>
# MESSAGE: <optional broadcast>
# REASONING: <one sentence>
# """