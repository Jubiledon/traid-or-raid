# agents/percept_filter.py

class PerceptFilter:

    @staticmethod
    def silence(percept: dict) -> dict:
        silenced = dict(percept)

        silenced["nearby_agents"] = [
            PerceptFilter._silence_agent(agent)
            for agent in percept.get("nearby_agents", [])
        ]

        return silenced

    @staticmethod
    def _silence_agent(agent: dict) -> dict:
        return {**agent, "last_message": ""}