import os
import subprocess

from services.config import CONFIG

FETCH_SCRIPT = "/home/pi/smart-mirror/pi-client/mirror/fetch_layout.py"
GENERATE_SCRIPT = "/home/pi/smart-mirror/pi-client/mirror/generate_config.js"


class SyncService:
    def run_command(self, command, description):
        print(f"\n--- {description} ---")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print(result.stderr)

        return result.returncode == 0

    def fetch_layout(self, user_id, profile_id=None):
        command = f"python3 {FETCH_SCRIPT} --user-id {user_id}"
        if profile_id:
            command += f" --profile-id {profile_id}"

        return self.run_command(command, "Fetching layout from backend")

    def generate_config(self):
        return self.run_command(f"node {GENERATE_SCRIPT}", "Generating MagicMirror config")

    def restart_magicmirror(self):
        return self.run_command(CONFIG.magicmirror_restart_cmd, "Restarting MagicMirror")

    def sync_layout(self, user_id, profile_id=None, restart=None):
        if restart is None:
            restart = CONFIG.magicmirror_restart

        if not self.fetch_layout(user_id=user_id, profile_id=profile_id):
            return False

        if not self.generate_config():
            return False

        if restart:
            return self.restart_magicmirror()

        return True
