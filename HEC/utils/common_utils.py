from datetime import datetime

def clean_date(value):
    """Return a valid date or None. Handles blank strings and multiple formats."""
    if not value or not str(value).strip():
        return None
    value = str(value).strip()
    for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y'):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None
    # or raise/log if you want to reject bad input