# app/core/session_store.py
from typing import Dict, Any

# Simple in-memory store
USER_STATE: Dict[str, Dict[str, Any]] = {}
