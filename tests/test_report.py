import re
import subprocess

from cedge.build import TEMPLATES, build, main
from cedge.facts import ROOT, _fmt

# Digits allowed in template prose: protocol parameters fixed before the runs, labels of designs,
# years, dates of fixed schedules, section numbers and bibliographic references. Every measured
# figure must be a placeholder.
ALLOWED = [
    r"\b(?:19|20)\d\d\b", r"^\s*(\d+\.|##\s*\d+\.)", r"\b[DEHFVT]\d\b", (r"\b\d{1,2} (?:January|February|March|"
    r"April|May|June|July|August|September|October|November|December)\b"), r"\b5pm\b", r"\b3pm to 4pm\b",
    r"\b101 to 200\b", r"\b21-day\b", r"\b30% tax\b", r"\b0\.95\b", r"\b50%", r"\b15 bp\b",
    r"(?i)\bsections? \d( (to|and) \d)?\b", r"(?i)\brounds? \d( (to|and) \d)?\b", r"\bSHA-256\b", r"Paper \d+(-\d+)?",
    r"\d+\(\d+\), \d+-\d+", r"\b95%", r"REPORT-2\.md", r"POST_RESULTS-2\.md", r"MANIFEST\.sha256",
]


def test_build_is_current():
    assert main(["--check"]) == 0


def test_template_prose_has_no_hand_typed_figures():
    for path in TEMPLATES.glob("*.md"):
        body = path.read_text(encoding="utf-8").split("## References")[0]
        for line in body.splitlines():
            stripped = re.sub(r"\{[a-z0-9_]+\}", "", line)
            stripped = re.sub(r"\([^)]*\.(md|csv|txt)\)", "", stripped)
            for pat in ALLOWED:
                stripped = re.sub(pat, "", stripped)
            assert not re.search(r"\d", stripped), f"{path.name}: hand-typed figure in: {line}"


def test_every_placeholder_resolves():
    for text in build().values():
        assert not re.search(r"\{[a-z0-9_]+\}", text)


def test_no_em_dash():
    for text in build().values():
        assert "—" not in text


def test_manifests_match_the_sources():
    manifests = list((ROOT / "sources").glob("*/MANIFEST.sha256"))
    assert manifests
    for manifest in manifests:
        r = subprocess.run(["sha256sum", "-c", "--quiet", manifest.name], cwd=manifest.parent, check=False)
        assert r.returncode == 0, manifest


def test_half_up_rounding():
    assert _fmt(0.245, "{:.2f}") == "0.25"
    assert _fmt(-0.0001, "{:.1f}") == "0.0"
    assert _fmt(0.0001, "{:+.1f}%") == "+0.0%"
