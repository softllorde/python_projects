def normalize_phone(phone: str) -> str:
    return (
        phone.strip()
        .replace(" ", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
    )
