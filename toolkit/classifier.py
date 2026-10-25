"""Deterministic filename classification rules used before any AI fallback."""
from pathlib import Path

EXTENSION_CATEGORIES = {
    # Documents and text
    ".pdf": "Documents", ".doc": "Documents", ".docx": "Documents",
    ".txt": "Documents", ".md": "Documents", ".rtf": "Documents",
    ".odt": "Documents", ".pages": "Documents",
    # Source and web code
    ".py": "Code", ".pyw": "Code", ".js": "Code", ".jsx": "Code",
    ".ts": "Code", ".tsx": "Code", ".html": "Code", ".htm": "Code",
    ".css": "Code", ".scss": "Code", ".java": "Code", ".kt": "Code",
    ".c": "Code", ".h": "Code", ".cpp": "Code", ".hpp": "Code",
    ".cs": "Code", ".go": "Code", ".rs": "Code", ".sh": "Code",
    ".ps1": "Code", ".bat": "Code", ".sql": "Code", ".ipynb": "Code",
    # Structured data and spreadsheets
    ".json": "Data", ".jsonl": "Data", ".yaml": "Data", ".yml": "Data",
    ".xml": "Data", ".toml": "Data", ".csv": "Spreadsheets",
    ".xlsx": "Spreadsheets", ".xls": "Spreadsheets", ".ods": "Spreadsheets",
    # Media
    ".png": "Images", ".jpg": "Images", ".jpeg": "Images", ".gif": "Images",
    ".webp": "Images", ".svg": "Images", ".bmp": "Images", ".tif": "Images", ".tiff": "Images",
    ".mp3": "Audio", ".wav": "Audio", ".m4a": "Audio", ".aac": "Audio", ".flac": "Audio", ".ogg": "Audio",
    ".mp4": "Video", ".mov": "Video", ".avi": "Video", ".mkv": "Video", ".webm": "Video",
    # Archives, packages, and applications
    ".zip": "Archives", ".rar": "Archives", ".7z": "Archives", ".tar": "Archives",
    ".gz": "Archives", ".bz2": "Archives", ".xz": "Archives",
    ".exe": "Applications", ".msi": "Applications", ".apk": "Applications", ".app": "Applications",
    # Engineering and specialist files
    ".cir": "Engineering Files", ".sp": "Engineering Files", ".sch": "Engineering Files",
    ".kicad_sch": "Engineering Files", ".kicad_pcb": "Engineering Files", ".dwg": "Engineering Files",
    ".dxf": "Engineering Files", ".step": "Engineering Files", ".stp": "Engineering Files",
}

SENSITIVE_TERMS = (
    "password", "passwd", "recovery-code", "recovery_code", "recovery codes",
    "private-key", "private_key", "secret-key", "secret_key", "credentials",
    "auth-token", "access-token", "backup-codes", "backup_codes", "2fa-codes",
)


def classify_filename(filename: str) -> tuple[str, str, bool]:
    """Return (category, reason, sensitive_flag) without reading file content."""
    lower_name = filename.casefold().replace(" ", "_")
    if any(term.replace(" ", "_") in lower_name for term in SENSITIVE_TERMS):
        return "Sensitive — review", "Filename looks security-sensitive; excluded from AI fallback", True

    lower_path = filename.casefold()
    # Compound suffixes before simple suffixes.
    for suffix in (".kicad_sch", ".kicad_pcb"):
        if lower_path.endswith(suffix):
            return "Engineering Files", "Extension rule", False

    suffix = Path(filename).suffix.lower()
    if suffix in EXTENSION_CATEGORIES:
        return EXTENSION_CATEGORIES[suffix], "Extension rule", False

    if not suffix:
        return "Needs review", "No file extension; filename alone is insufficient", False

    return "Needs review", f"Unknown extension: {suffix}", False
