class LocalCommandHandler:
    def handle(self, command: str, user_id: int) -> dict:
        normalized = (command or "").strip().lower()

        if not normalized:
            return {
                "text": "Nezachytil som ziadny prikaz.",
                "display": "No command captured",
                "speak": False,
            }

        if "weather" in normalized or "pocasie" in normalized:
            return {
                "text": "Zobrazujem modul pocasia.",
                "display": "Weather module opened",
                "speak": True,
                "action": "show_weather",
            }

        if "profile" in normalized and "switch" in normalized:
            return {
                "text": f"Prepinam profil pre pouzivatela {user_id}.",
                "display": f"Switching profile for user {user_id}",
                "speak": True,
                "action": "switch_profile",
            }

        return {
            "text": "Prikaz bol prijaty, ale nie je mapovany.",
            "display": f"Unknown command: {command}",
            "speak": True,
            "action": "unknown",
        }
