from pathlib import Path

from leakfence.scanner import scan_directory, scan_text


def test_aws_key_is_detected():
    prefix = "AK" + "IA"
    key = prefix + "LEAKFENCEDEMO123"
    findings = scan_text(f'key = "{key}"', "demo.py")
    assert len(findings) == 1
    assert findings[0].secret_type == "AWS Access Key"
    assert findings[0].line == 1


def test_private_key_is_detected():
    header = "-----BEGIN " + "RSA PRIVATE KEY" + "-----"
    findings = scan_text(header, "key.pem")
    assert findings[0].secret_type == "Private Key"


def test_environment_variable_reference_is_safe():
    findings = scan_text('API_KEY = os.getenv("API_KEY")', "config.py")
    assert findings == []


def test_jwt_is_detected():
    token = ".".join(["eyJ" + "A" * 8, "B" * 12, "C" * 12])
    findings = scan_text(f'token = "{token}"', "auth.py")
    assert findings[0].secret_type == "JWT Token"


def test_directory_scan_honors_ignore_file(tmp_path: Path):
    ignored = tmp_path / "fixtures"
    ignored.mkdir()
    name = "pass" + "word"
    value = "hunter" + "2"
    (ignored / "bad.py").write_text(f"{name} = '{value}'", encoding="utf-8")
    (tmp_path / ".leakfenceignore").write_text("fixtures/*\n", encoding="utf-8")

    assert scan_directory(tmp_path) == []
