from typing import Any, Dict, List

class Puzzle:
    def __init__(self, parameters: Dict[str, Any]):
        self.connection: str = parameters["connection"]
        self.clues: List[str] = [values for keys, values in parameters.items() if "clue" in keys]
        self.type = [values for keys, values in parameters.items() if "type" in keys]