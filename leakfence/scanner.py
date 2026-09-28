from __future__ import annotations

import fnmatch
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    """A single potential secret finding."""

    path: str
    line: int
    secret_type: str


# These patterns intentionally favor high-signal formats and literal assignments.
PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "AWS Access Key",
        re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    ),
    (
        "GitHub Token",
        re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    ),
    (
        "Private Key",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    ),
    (
        "JWT Token",
        re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"),
    ),
    (
        "Google API Key",
        re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    ),
    (
        "Generic Credential",
        re.compile(
            r"(?i)\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|secret|password|passwd|private[_-]?key)"
            r"\s*(?:=|:)\s*[\"'][^\"'\n]{6,}[\"']"
        ),
    ),
)

DEFAULT_IGNORED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "build",
    "dist",
    "node_modules",
}

SCAN_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".java",
    ".c",
    ".h",
    ".cpp",
    ".hpp",
    ".go",
    ".rs",
    ".rb",
    ".php",
    ".sh",
    ".bash",
    ".zsh",
    ".yml",
    ".yaml",
    ".json",
    ".toml",
    ".ini",
    ".cfg",
    ".conf",
    ".env",
    ".sql",
    ".md",
    ".txt",
}

MAX_FILE_SIZE = 2 * 1024 * 1024


def load_ignore_patterns(root: Path) -> list[str]:
    ignore_file = root / ".leakfenceignore"
    if not ignore_file.exists():
        return []

    return [
        line.strip()
        for line in ignore_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def _is_ignored(path: Path, root: Path, patterns: list[str]) -> bool:
    relative = path.relative_to(root).as_posix()
    parts = set(path.relative_to(root).parts)

    if parts & DEFAULT_IGNORED_DIRS:
        return True

    return any(
        fnmatch.fnmatch(relative, pattern) or fnmatch.fnmatch(path.name, pattern)
        for pattern in patterns
    )


def iter_files(root: Path, patterns: list[str] | None = None):
    """Yield scannable UTF-8-ish text files under root."""
    ignore_patterns = patterns if patterns is not None else load_ignore_patterns(root)

    for path in root.rglob("*"):
        if not path.is_file() or _is_ignored(path, root, ignore_patterns):
            continue
        if path.stat().st_size > MAX_FILE_SIZE:
            continue
        if path.suffix.lower() not in SCAN_EXTENSIONS and path.name not in {"Dockerfile", "Makefile"}:
            continue
        yield path


def scan_text(text: str, display_path: str) -> list[Finding]:
    findings: list[Finding] = []
    lines = text.splitlines()

    for line_number, line in enumerate(lines, start=1):
        for secret_type, pattern in PATTERNS:
            if pattern.search(line):
                findings.append(Finding(display_path, line_number, secret_type))
                break

    return findings


def scan_directory(root: str | Path) -> list[Finding]:
    root_path = Path(root).resolve()
    if not root_path.is_dir():
        raise ValueError(f"Scan path is not a directory: {root}")

    findings: list[Finding] = []
    for path in iter_files(root_path):
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        findings.extend(scan_text(text, path.relative_to(root_path).as_posix()))

    return findings
