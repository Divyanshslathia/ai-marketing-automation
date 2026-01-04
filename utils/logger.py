from datetime import datetime


def log(agent: str, message: str):
    timestamp = datetime.utcnow().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{agent}] {message}")
