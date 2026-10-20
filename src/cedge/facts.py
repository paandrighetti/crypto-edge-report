"""Every figure the report prints, read from the study outputs in sources/.

Each fact records the file it came from. Statements the report makes in words (a decision, a sign,
"no design passes") are checked with `claim`: if a regenerated source contradicts one, the build
fails instead of printing a sentence the data no longer support.
"""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "sources"


class ClaimError(AssertionError):
    pass


@dataclass
class Facts:
    values: dict[str, str] = field(default_factory=dict)
    raw: dict[str, float | int | str | bool] = field(default_factory=dict)
    source: dict[str, str] = field(default_factory=dict)

    def put(self, key: str, value, fmt: str, src: Path) -> None:
        if key in self.values:
            raise KeyError(f"duplicate fact {key}")
        self.raw[key] = value
        self.values[key] = _fmt(value, fmt)
        self.source[key] = str(src.relative_to(ROOT))


def _fmt(value, fmt: str) -> str:
    """Format with half-up rounding on the decimal representation, so 0.245 prints 0.25."""
    if not fmt:
        return str(value)
    m = re.fullmatch(r"(.*)\{:(\+?)\.(\d)f\}(.*)", fmt)
    if m and isinstance(value, float):
        q = Decimal(repr(value)).quantize(Decimal(1).scaleb(-int(m.group(3))), rounding=ROUND_HALF_UP)
        body = f"{q:+f}" if m.group(2) else f"{q:f}"
        if re.fullmatch(r"[+-]0(\.0+)?", body):
            body = ("+" if m.group(2) else "") + body.lstrip("+-")
        return m.group(1) + body + m.group(4)
    return fmt.format(value)


def claim(ok: bool, text: str) -> None:
    if not ok:
        raise ClaimError(f"source no longer supports: {text}")


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- round 1
def round1(f: Facts) -> None:
    src = SRC / "round1-flows" / "results.json"
    d = _json(src)
    names = ["D1", "D2", "D3", "D4"]
    claim(all(not d["decisions"][n]["pass"] for n in names), "no design of round 1 passes")
    claim(not any(d["holm"].values()), "no design of round 1 passes Holm's test")
    f.put("r1_trials", d["trials"], "{}", src)
    for n in names:
        c = d["configs"][n]
        k = n.lower()
        f.put(f"r1_{k}_desc", c["description"], "", src)
        f.put(f"r1_{k}_from", c["net"]["first_day"], "", src)
        f.put(f"r1_{k}_to", c["net"]["last_day"], "", src)
        f.put(f"r1_{k}_sr_gross", c["before_costs"]["sharpe"], "{:.2f}", src)
        f.put(f"r1_{k}_sr", c["net"]["sharpe"], "{:.2f}", src)
        lo, hi = c["bootstrap_sharpe_ci95"]
        f.put(f"r1_{k}_ci", f"[{_fmt(lo, '{:.2f}')}, {_fmt(hi, '{:.2f}')}]", "", src)
        f.put(f"r1_{k}_t", c["test"]["hac_t"], "{:.2f}", src)
        f.put(f"r1_{k}_p", c["test"]["p_one_sided"], "{:.3f}", src)
    d1 = d["configs"]["D1"]
    claim(d1["before_costs"]["mean_bp_per_day"] > 0 > d1["net"]["mean_bp_per_day"],
          "the funding carry is positive before costs and negative after")
    f.put("r1_d1_gross_bp", d1["before_costs"]["mean_bp_per_day"], "{:.2f}", src)
    f.put("r1_d1_cost_bp", d1["cost_bp_per_day"], "{:.2f}", src)
    f.put("r1_d1_breakeven", d1["break_even_cost_multiple"] * 100, "{:.0f}%", src)
    srs = [d["configs"][n]["net"]["sharpe"] for n in names]
    f.put("r1_sr_lo", min(srs), "{:.2f}", src)
    f.put("r1_sr_hi", max(srs), "{:.2f}", src)
    claim(max(srs) < 0, "every primary design of round 1 has a negative net Sharpe ratio")
    for n in ("D1", "D2", "D4"):
        c = d["configs"][n]
        claim(c["before_costs"]["sharpe"] > 0 > c["net"]["sharpe"], f"{n} earns before costs and loses after")
    for n in ("D2", "D4"):
        claim(all(v["mean_bp_per_day"] < 0 for v in d["configs"][n]["by_year"].values()),
              f"{n} loses money net of costs in every year")
    v = _json(SRC / "round1-flows" / "verification.json")
    gap = max(abs(v[n]["mean_net_bp"] - d["configs"][n]["net"]["mean_bp_per_day"]) for n in ("D2", "D3", "D4"))
    claim(gap < 1e-6,
          "round 1's second implementation reproduces the daily net means of D2 to D4 to the decimals it prints")
    src_p = SRC / "round1-flows" / "POST_RESULTS.md"
    m = re.search(r"largest absolute difference across price, funding and cost components is ([0-9.]+) bp a day, "
                  r"and the trade counts match", " ".join(src_p.read_text(encoding="utf-8").split()))
    claim(m is not None, "round 1's post-results note states the largest difference and that the trade counts match")
    f.put("r1_v_diff", m.group(1), "", src_p)


# --------------------------------------------------------------------------- round 2
def round2(f: Facts) -> None:
    src = SRC / "round2-slow" / "results.json"
    d = _json(src)
    dec = d["decisions"]
    claim(not dec["composite"]["pass"] and dec["E3"]["pass"], "the composite fails and E3 passes")
    claim(not dec["composite"]["closes_direction"], "the composite's failure is inconclusive")
    comp, e3, e4 = d["configs"]["composite"], d["configs"]["E3"], d["configs"]["E4"]
    f.put("r2_universe", d["universe"]["members_ever"], "{:,}", src)
    f.put("r2_comp_desc", comp["description"], "", src)
    f.put("r2_comp_sr", comp["net"]["sharpe"], "{:.2f}", src)
    lo, hi = comp["bootstrap_sharpe_ci95"]
    f.put("r2_comp_ci", f"[{_fmt(lo, '{:.2f}')}, {_fmt(hi, '{:.2f}')}]", "", src)
    f.put("r2_comp_t", comp["test"]["hac_t"], "{:.2f}", src)
    f.put("r2_comp_p", comp["test"]["p_one_sided"], "{:.3f}", src)
    f.put("r2_comp_bound", dec["composite"]["upper_bound"], "{:.2f}", src)
    f.put("r2_comp_from", comp["net"]["first_day"], "", src)
    f.put("r2_e3_desc", e3["description"], "", src)
    f.put("r2_e3_ir", e3["timing"]["information_ratio"], "{:.2f}", src)
    lo, hi = e3["timing_ci95"]
    f.put("r2_e3_ci", f"[{_fmt(lo, '{:.2f}')}, {_fmt(hi, '{:.2f}')}]", "", src)
    f.put("r2_e3_t", e3["timing"]["hac_t"], "{:.2f}", src)
    f.put("r2_e3_p", e3["timing"]["p_one_sided"], "{:.4f}", src)
    f.put("r2_e3_months", e3["timing"]["months"], "{}", src)
    f.put("r2_e3_from", e3["net"]["first_day"], "", src)
    f.put("r2_e3_to", e3["net"]["last_day"], "", src)
    f.put("r2_e4_desc_lc", e4["description"][:1].lower() + e4["description"][1:], "", src)
    descriptive = {k: c["dsr"] for k, c in d["configs"].items() if c.get("role") == "descriptive"}
    claim(max(descriptive, key=descriptive.get) == "E4",
          "E4 has the highest deflated Sharpe ratio of round 2's descriptive designs")
    src_v = SRC / "round2-slow" / "verification.json"
    v = _json(src_v)
    vd = v["decision"]
    claim(vd["E3"]["passes"] and not vd["composite"]["passes"]
          and vd["composite"]["verdict"].startswith("fail, inconclusive"),
          "round 2's second implementation takes the run's decisions")
    f.put("r2_comp_p4", comp["test"]["p_one_sided"], "{:.4f}", src)
    f.put("r2_v_comp_p", vd["holm"]["p_values"]["composite"], "{:.4f}", src_v)
    f.put("r2_v_e3_p", vd["holm"]["p_values"]["E3"], "{:.4f}", src_v)
    claim(v["spot_checks"]["mismatches"] == 0, "round 2's spot checks find no mismatch")
    f.put("r2_v_checks", v["spot_checks"]["comparisons"], "{:,}", src_v)
    f.put("r2_e4_sr", e4["net"]["sharpe"], "{:.2f}", src)
    f.put("r2_e4_dsr", e4["dsr"], "{:.2f}", src)
    f.put("r2_e4_bcm", e4["break_even_cost_multiple"], "{:.1f}", src)
    claim(e4["role"] == "descriptive", "E4 was descriptive in round 2")


# --------------------------------------------------------------------------- round 3
def round3(f: Facts) -> None:
    src = SRC / "round3-e4b" / "results.json"
    d = _json(src)
    dec = d["decision"]
    c = d["configs"][dec["design"]]
    claim(not dec["pass"] and dec["criteria"]["p_at_most_alpha"] and not dec["criteria"]["intercept_p_at_most_alpha"],
          "study B's mean passes its test but its intercept on E4 does not, so it fails")
    claim(not dec["closes_direction"], "study B's failure is inconclusive")
    f.put("r3_desc", c["description"], "", src)
    f.put("r3_from", d["window"][0] if isinstance(d["window"], list) else c["net"]["first_day"], "", src)
    f.put("r3_sr", c["net"]["sharpe"], "{:.2f}", src)
    lo, hi = c["bootstrap_sharpe_ci95"]
    f.put("r3_ci", f"[{_fmt(lo, '{:.2f}')}, {_fmt(hi, '{:.2f}')}]", "", src)
    f.put("r3_t", c["test"]["hac_t"], "{:.2f}", src)
    f.put("r3_p", c["test"]["p_one_sided"], "{:.3f}", src)
    ref = d["against_reference"]
    f.put("r3_alpha", ref["alpha_pct_per_month"], "{:.2f}%", src)
    f.put("r3_alpha_t", ref["hac_t"], "{:.2f}", src)
    f.put("r3_alpha_p", ref["p_one_sided"], "{:.3f}", src)
    f.put("r3_corr", ref["corr_monthly"], "{:.2f}", src)
    f.put("r3_alpha_p4", ref["p_one_sided"], "{:.4f}", src)
    src_v = SRC / "round3-e4b" / "verification.json"
    v = _json(src_v)
    claim(v["decision"]["verdict"].startswith("fail, inconclusive") and not v["decision"]["passes"],
          "round 3's second implementation takes the run's decision")
    f.put("r3_v_alpha_p", v["intercept"]["p_value"], "{:.4f}", src_v)
    meta = v["meta"]
    claim(meta["preregistration_sha256_found"] == d["prereg_sha256"] != meta["preregistration_sha256_expected"],
          "round 3's second implementation was written from the frozen pre-registration, which the run amended")
    f.put("r3_v_hash_frozen", v["meta"]["preregistration_sha256_expected"][:8], "", src_v)
    f.put("r3_v_hash_run", d["prereg_sha256"][:8], "", src)
    claim(v["spot_checks"]["mismatches"] == 0, "round 3's spot checks find no mismatch")
    f.put("r3_v_checks", v["spot_checks"]["comparisons"], "{:,}", src_v)


# --------------------------------------------------------------------------- dealer gamma
def gamma(f: Facts) -> None:
    src = SRC / "deribit-gamma" / "stage1.json"
    d = _json(src)
    claim(not any(d["decision"].values()), "no hypothesis passes stage 1")
    f.put("dg_hours", d["hours"], "{:,}", src)
    for h in ("H1", "H2", "H3"):
        f.put(f"dg_{h.lower()}_p", d[h]["p_one_sided"], "{:.3f}", src)
    src2 = SRC / "deribit-gamma" / "followup.json"
    g = _json(src2)
    claim(not any(g["decision"].values()), "neither follow-up hypothesis passes")
    f.put("dg_test_hours", g["hours"], "{:,}", src2)
    for h in ("F1", "F2"):
        f.put(f"dg_{h.lower()}_p", g[h]["p_one_sided"], "{:.3f}", src2)


# --------------------------------------------------------------------------- volatility
def vol(f: Facts) -> None:
    src = SRC / "vol-edges" / "results.json"
    d = _json(src)
    dec = d["decision"]
    claim(dec["pass"] == {"V1": False, "V2": False, "V3": False, "T1": True}, "V1 to V3 fail and T1 passes")
    for k in ("V1", "V2", "V3", "T1"):
        f.put(f"ve_{k.lower()}_p", dec["p_one_sided"][k], "{:.3f}" if k != "T1" else "{:.4f}", src)
    f.put("ve_v1_beta", d["V1"]["test"]["beta"], "{:.2f}", src)
    f.put("ve_v2_mean_bp", d["V2"]["test"]["mean"] * 1e4, "{:.1f}", src)
    f.put("ve_v3_theta", d["V3"]["test"]["theta"], "{:.3f}", src)
    t1 = d["T1"]
    f.put("ve_t1_weeks", t1["test"]["weeks"], "{}", src)
    f.put("ve_t1_mean_bp", t1["test"]["mean"] * 1e4, "{:.1f}", src)
    f.put("ve_t1_t", t1["test"]["t"], "{:.2f}", src)
    f.put("ve_t1_won", t1["share_won"] * 100, "{:.0f}%", src)
    f.put("ve_t1_skew", t1["strangle"]["skewness"], "{:.1f}", src)
    f.put("ve_t1_worst", t1["worst_weekend"]["return"] * 100, "{:.1f}%", src)
    f.put("ve_t1_worst_entry", t1["worst_weekend"]["entry"][:10], "", src)
    src_v = SRC / "vol-edges" / "verification.json"
    v = _json(src_v)
    claim(sorted(v["passing_tests"]) == sorted(k for k, ok in dec["pass"].items() if ok),
          "the volatility study's second implementation passes the same tests")
    f.put("ve_v_diff", max(abs(v["tests"][k]["p_value"] - dec["p_one_sided"][k]) for k in ("V1", "V2", "V3")),
          "{:.4f}", src_v)
    f.put("ve_v_t1_p", v["tests"]["T1"]["p_value"], "{:.4f}", src_v)
    vs = v["tests"]["T1"]["statistic"]
    claim(abs(vs["mean"] - t1["test"]["mean"]) < 1e-12 and abs(vs["t"] - t1["test"]["t"]) < 1e-9,
          "the second implementation finds T1's mean and t-statistic")
    claim(t1["test"]["mean"] > 0, "the weekend strangle's mean return is positive")
    claim(v["prereg_sha256"] != d["prereg_sha256"],
          "the volatility study's second implementation checked the frozen pre-registration")
    f.put("ve_v_hash_frozen", v["prereg_sha256"][:8], "", src_v)
    f.put("ve_v_hash_run", d["prereg_sha256"][:8], "", src)
    claim(t1["strangle"]["skewness"] < 0, "the strangle's weekly returns are negatively skewed")
    claim(t1["worst_weekend"]["entry"].startswith("2025-10-10"), "the worst weekend is that of 10 October 2025")


# --------------------------------------------------------------------------- Hyperliquid alts
def hl_alts(f: Facts) -> None:
    src = SRC / "hl-alts-ml" / "xs_ls_tradeable_verdict.json"
    v = _json(src)
    claim(v["verdict"] == "REJET", "the cross-sectional long/short arc is rejected")
    checks = {c["rule"]: c for c in v["checks"]}
    f.put("hl_trials", v["n_trials"], "{}", src)
    f.put("hl_champion", v["champion"], "", src)
    sig, n_top, scheme = v["champion"].split("/")
    m = re.fullmatch(r"([a-z]+?)(\d+)", sig)
    names = {"mom": "momentum", "rev": "reversal", "carry": "carry", "resmom": "residual momentum"}
    claim(m is not None and m.group(1) in names and scheme in ("quintile", "rank"),
          "the best cell's label is understood")
    weights = "long the top quintile and short the bottom one" if scheme == "quintile" else "weighted by rank"
    f.put("hl_champion_text", f"{m.group(2)}-day {names[m.group(1)]} on the {n_top} contracts with the highest median "
                              f"dollar volume, {weights}", "", src)
    f.put("hl_sr_net", float(next(c["value"] for r, c in checks.items() if r.startswith("Sharpe net"))), "{:.2f}", src)
    f.put("hl_dsr", float(next(c["value"] for r, c in checks.items() if r.startswith("Sharpe deflat"))), "{:.3f}", src)
    years = next(c["value"] for r, c in checks.items() if "annees positives" in r)
    pos, n = (int(x) for x in years.split("/"))
    f.put("hl_years_pos", pos, "{}", src)
    f.put("hl_years_n", n, "{}", src)
    f.put("hl_sr0", v["sr0_annual"], "{:.2f}", src)
    src_g = SRC / "hl-alts-ml" / "xs_ls_tradeable_grid.csv"
    cell = next(r for r in csv.DictReader(src_g.open(encoding="utf-8"))
                if (r["signal"], r["n_top"], r["scheme"]) == (sig, n_top, scheme))
    claim(abs(float(cell["sr_net_15"]) - f.raw["hl_sr_net"]) < 0.005, "the grid and the verdict agree on the best cell")
    claim(float(cell["sr_gross"]) > 0, "the best long/short cell earns before costs")
    claim(float(cell["sr_gross"]) > float(cell["sr_net_15"]), "costs lower the best cell's Sharpe ratio")
    f.put("hl_sr_gross", float(cell["sr_gross"]), "{:.2f}", src_g)
    f.put("hl_grid_median", v["grid_median_sr_net_15"], "{:.2f}", src)
    fin = _json(SRC / "hl-alts-ml" / "xs_ls_final_verdict.json")
    claim(set(fin.values()) == {"REJET"}, "every version of the long/short arc is rejected")
    src_b = SRC / "hl-alts-ml" / "hl_summary.json"
    b = _json(src_b)
    pb = b["configs"][b["primary"]]
    claim(b["verdict"] == "REJET" and pb["dll_mean"] < 0, "meta-labeling of the trend sleeve is rejected, with a worse log-loss")
    f.put("hl_b_dll_p", pb["dll_p"], "{:.2f}", src_b)
    f.put("hl_b_auc", pb["auc_meta"], "{:.3f}", src_b)
    f.put("hl_b_auc_base", pb["auc_base"], "{:.3f}", src_b)
    f.put("hl_b_configs", len(b["configs"]), "{}", src_b)
    claim(all(c["dll_mean"] < 0 for c in b["configs"].values()),
          "in every configuration the meta-model predicts worse than the signal alone")
    src_c = SRC / "hl-alts-ml" / "a4_summary.json"
    a = _json(src_c)
    pa = a["configs"][a["primary"]]
    claim(a["verdict"] == "REJET", "meta-labeling of the BTC and ETH trend rule is rejected")
    claim(all(c["dll_mean"] < 0 for c in a["configs"].values()),
          "in every configuration of arc C the filter predicts worse than the signal alone")
    f.put("hl_c_configs", len(a["configs"]), "{}", src_c)
    f.put("hl_c_dll_p", pa["dll_p"], "{:.2f}", src_c)
    f.put("hl_c_dg", pa["dg_ann"] * 100, "{:+.1f}%", src_c)
    f.put("hl_c_dg_t", pa["dg_t_nw"], "{:.2f}", src_c)


# --------------------------------------------------------------------------- perp premia
def perp_premia(f: Facts) -> None:
    src = SRC / "perp-premia" / "results.csv"
    if not src.exists():
        f.put("pp_status", "pending", "", ROOT / "sources")
        return
    rows = {r["strategy"]: r for r in csv.DictReader(src.open(encoding="utf-8"))}
    verdict = (SRC / "perp-premia" / "verdict.txt").read_text(encoding="utf-8")
    f.put("pp_status", "decided", "", src)
    for key, name in (("carry", "carry_lb7_h10"), ("mom", "mom_lb14")):
        r = rows[name]
        f.put(f"pp_{key}_oos_sr", float(r["oos_sharpe"]), "{:.2f}", src)
        f.put(f"pp_{key}_t", float(r["oos_t_alpha"]), "{:.2f}", src)
        f.put(f"pp_{key}_dsr", float(r["dsr_full"]), "{:.2f}", src)
        f.put(f"pp_{key}_dd", float(r["full_max_dd"]) * 100, "{:.0f}%", src)
        f.put(f"pp_{key}_cagr", float(r["after_tax_cagr"]) * 100, "{:+.1f}%", src)
        retained = re.search(rf"{name} : (RETENUE|REJETÉE)", verdict)
        claim(retained is not None, f"the verdict file states the decision on {name}")
        f.put(f"pp_{key}_verdict", "retained" if retained.group(1) == "RETENUE" else "rejected", "",
              SRC / "perp-premia" / "verdict.txt")
    claim(f.raw["pp_carry_verdict"] == f.raw["pp_mom_verdict"] == "rejected", "both premia are rejected")
    claim(len([k for k in rows if k != "btc_buy_and_hold"]) == 13, "thirteen configurations are declared")
    primary = rows["carry_lb7_h10"]
    claim(float(primary["is_sharpe"]) > 0 > float(primary["oos_sharpe"]),
          "the primary carry has a positive Sharpe ratio before 2023 and a negative one after")
    f.put("pp_btc_oos_sr", float(rows["carry_lb7_h10"]["oos_btc_sharpe"]), "{:.2f}", src)
    f.put("pp_carry_is_sr", float(rows["carry_lb7_h10"]["is_sharpe"]), "{:.2f}", src)
    carry = [r for k, r in rows.items() if k.startswith("carry_")]
    claim(len(carry) == 9, "nine carry configurations are reported")
    negative = sum(float(r["oos_sharpe"]) < 0 for r in carry)
    f.put("pp_carry_negative_oos", "all nine" if negative == 9 else f"{negative} of the nine", "", src)


def build_facts() -> Facts:
    f = Facts()
    for step in (round1, round2, round3, gamma, vol, hl_alts, perp_premia):
        step(f)
    return f
