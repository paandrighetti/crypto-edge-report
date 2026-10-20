"""Render REPORT.md and SUMMARY.md from templates/ and the facts read from sources/.

    python -m cedge.build           write REPORT.md, SUMMARY.md and facts.json
    python -m cedge.build --check   fail if any of them is out of date
"""
from __future__ import annotations

import json
import re
import sys

from .facts import ROOT, build_facts

TEMPLATES = ROOT / "templates"
PLACEHOLDER = re.compile(r"\{([a-z0-9_]+)\}")


def derived(values: dict[str, str], raw: dict) -> dict[str, str]:
    """Sentences whose wording depends on the data, chosen here and nowhere else."""
    out = {}
    if raw["pp_status"] == "pending":
        out["pp_summary"] = "pending"
        out["pp_section"] = (TEMPLATES / "perp_premia_pending.md").read_text(encoding="utf-8").strip()
    else:
        verdicts = (values["pp_carry_verdict"], values["pp_mom_verdict"])
        out["pp_summary"] = ("both rejected" if verdicts == ("rejected", "rejected")
                             else f"carry {verdicts[0]}, momentum {verdicts[1]}")
        out["pp_section"] = (TEMPLATES / "perp_premia_decided.md").read_text(encoding="utf-8").strip()
    return out


def render(template: str, values: dict[str, str]) -> str:
    missing = sorted({k for k in PLACEHOLDER.findall(template) if k not in values})
    if missing:
        raise KeyError(f"no fact for: {', '.join(missing)}")
    text = template
    for _ in range(2):  # a section that contains placeholders resolves in a second pass
        text = PLACEHOLDER.sub(lambda m: values[m.group(1)], text)
    return text


def build() -> dict[str, str]:
    f = build_facts()
    values = dict(f.values)
    values.update(derived(values, f.raw))
    outputs = {name: render((TEMPLATES / name).read_text(encoding="utf-8"), values)
               for name in ("REPORT.md", "SUMMARY.md")}
    outputs["facts.json"] = json.dumps(
        {k: {"value": f.raw[k], "printed": f.values[k], "source": f.source[k]} for k in f.values},
        indent=1, ensure_ascii=False) + "\n"
    return outputs


def main(argv: list[str]) -> int:
    outputs = build()
    if "--check" in argv:
        stale = [n for n, t in outputs.items()
                 if not (ROOT / n).exists() or (ROOT / n).read_text(encoding="utf-8") != t]
        if stale:
            print("out of date: " + ", ".join(stale) + " (run python -m cedge.build)")
            return 1
        print("up to date")
        return 0
    for name, text in outputs.items():
        (ROOT / name).write_text(text, encoding="utf-8")
        print(f"wrote {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
