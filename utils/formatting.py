def format_currency(amount: float, currency: str = "₹") -> str:
    """Formats numeric values into clean localized currency string."""
    try:
        return f"{currency}{int(amount):,}"
    except Exception:
        return f"{currency}{amount}"

def get_source_badge_html(source_text: str) -> str:
    """Renders HTML badge showing data provenance tag (LIVE, ESTIMATED, DEMO, CURATED)."""
    src_upper = source_text.upper()
    if "LIVE" in src_upper:
        bg_color = "#10B981"  # Emerald green
        txt = f"🟢 {source_text}"
    elif "ESTIMATED" in src_upper:
        bg_color = "#F59E0B"  # Amber orange
        txt = f"⚡ {source_text}"
    elif "CURATED" in src_upper or "DEMO" in src_upper:
        bg_color = "#3B82F6"  # Royal blue
        txt = f"📦 {source_text}"
    else:
        bg_color = "#6B7280"  # Gray
        txt = f"ℹ️ {source_text}"

    return f"""<span style="background-color: {bg_color}; color: white; padding: 3px 8px; border-radius: 6px; font-size: 0.8rem; font-weight: 600;">{txt}</span>"""
