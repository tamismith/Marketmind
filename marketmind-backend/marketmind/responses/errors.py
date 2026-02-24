from typing import Any, Dict, Optional, Tuple

from flask import jsonify


def error_response(
    code: str,
    message: str,
    status: int,
    details: Optional[Dict[str, Any]] = None,
) -> Tuple[Any, int]:
    payload: Dict[str, Any] = {
        "error": {
            "code": code,
            "message": message,
        }
    }
    if details:
        payload["error"]["details"] = details
    return jsonify(payload), status
