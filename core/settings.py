"""Runtime configuration — credentials and SSH constants."""
import os

USERNAME = os.getenv("ROUTER_USERNAME", "")
PASSWORD = os.getenv("ROUTER_PASSWORD", "")

SSH_TIMEOUT_OPS = 30
SSH_TIMEOUT_OPS_LONG = 90
SSH_RETRIES = 1
SSH_RETRY_DELAY = 2
SSH_MAX_CONCURRENT = 5
SSH_STRICT_HOST_KEY = os.getenv("SSH_STRICT_HOST_KEY", "").lower() in ("true", "1", "yes")
