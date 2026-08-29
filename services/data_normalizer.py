from typing import Any, Dict, List, Optional

def normalize_response(
    status: str,
    source: str,
    data: Any,
    message: Optional[str] = None
) -> Dict[str, Any]:
    """
    Standardizes tool response format across all data providers.
    Status can be: 'success', 'partial', or 'error'.
    Source can be: 'LIVE API', 'ESTIMATED DATA', 'CURATED FALLBACK', 'DEMO DATA'.
    """
    valid_statuses = {"success", "partial", "error"}
    norm_status = status.lower() if status.lower() in valid_statuses else "success"
    
    return {
        "status": norm_status,
        "source": source,
        "data": data if data is not None else [],
        "message": message or f"Data retrieved via {source}"
    }
