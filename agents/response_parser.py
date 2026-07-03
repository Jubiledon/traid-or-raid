# agents/response_parser.py

class ResponseParser:

    def parse(
        self,
        raw: str,
        percept: dict,
        communication_on: bool,
    ) -> dict:
        # print(f"[RAW] {repr(raw)}")
        action = self._extract_action(raw)
        message = self._extract_message(raw)

        return self._build_action(
            action,
            message,
            percept,
            communication_on,
        )

    # def _extract_action(self, raw: str) -> str:
    #     return self._extract_field(raw, "ACTION").lower()

    def _extract_action(self, raw: str) -> str:
    # model may return just the value since prompt ends with "ACTION:"
        first_line = raw.strip().splitlines()[0].strip().lower()
        
        # handle "ACTION: move_n" format
        if first_line.startswith("action:"):
            return first_line.split(":", 1)[1].strip()
    
        # handle bare "move_n" format (model completed the prompt)
        return first_line

    def _extract_message(self, raw: str) -> str:
        # try explicit MESSAGE: field first
        explicit = self._extract_field(raw, "MESSAGE")
        if explicit:
            return explicit[:150]
        
        # if action is broadcast, grab everything after the first line
        # as the message content
        lines = raw.strip().splitlines()
        if lines and lines[0].strip().lower().startswith("action:"):
            remainder = "\n".join(lines[1:]).strip()
            # strip REASONING: prefix if present
            if remainder.upper().startswith("REASONING:"):
                remainder = remainder.split(":", 1)[1].strip()
            return remainder[:150]
        
        return ""

    def _extract_field(
        self,
        raw: str,
        field: str,
    ) -> str:

        for line in raw.strip().splitlines():
            if line.upper().startswith(f"{field}:"):
                return line.split(":", 1)[1].strip()

        return ""

    def _build_action(
        self,
        action: str,
        message: str,
        percept: dict,
        communication_on: bool,
    ) -> dict:

        if action.startswith("move_"):
            return self._move_action(action)

        if action == "collect":
            return {"type": "collect"}

        if action.startswith("raid_"):
            return self._raid_action(action, percept)

        if action == "broadcast" and communication_on:
            return {
                "type": "broadcast",
                "message": message,
            }

        return {"type": "wait"}

    def _move_action(self, action: str) -> dict:
        direction = action.split("_")[1].upper()

        return {
            "type": "move",
            "direction": direction,
        }

    def _raid_action(
        self,
        action: str,
        percept: dict,
    ) -> dict:

        target_id = action.split("_", 1)[1].upper()

        valid_targets = [
            agent["id"]
            for agent in percept["nearby_agents"]
            if agent["distance"] == 1
        ]

        if target_id not in valid_targets:
            return {"type": "wait"}

        return {
            "type": "raid",
            "target_id": target_id,
        }