"""Do states with a hot-weather rule disconnect fewer households in summer?

Reads EIA's 2024 Residential Utility Disconnections Report (Table 5, monthly
electricity disconnections by state) and compares the summer share
(June-August / annual) across the rule groups in states.csv.

    uv run --with pdfplumber python eia_check.py
"""
import csv, os, re, statistics
import pdfplumber

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, "raw", "eia_disconnections_2024.pdf")
# New York's rule was adopted March 2026, so in 2024 it had none; it is reported apart.
RULE_AFTER_2024 = {"New York"}


def num(s):
    return int(re.sub(r"[^\d]", "", s))  # strips commas and EIA's R/Q quality flags


def table5():
    rows, on = {}, False
    with pdfplumber.open(PDF) as pdf:
        for p in pdf.pages:
            t = p.extract_text() or ""
            if "Table 5. Monthly electricity residential customer disconnections by state" in t:
                on = True
            elif on and "Table 6." in t:
                break
            if not on:
                continue
            lines = t.replace("District of\nColumbia", "District of Columbia").splitlines()
            for ln in lines:
                m = re.match(r"^([A-Z][A-Za-z .]+?)\s+((?:[\d,]+[RQ]?\s+){12}[\d,]+[RQ]?)$", ln.strip())
                if m:
                    v = [num(x) for x in m.group(2).split()]
                    rows[m.group(1).strip()] = v
    return rows


def main():
    rows = table5()
    groups = {}
    for r in csv.DictReader(open(os.path.join(HERE, "states.csv"))):
        st = r["state"]
        if st not in rows:
            continue
        v = rows[st]
        months, total = v[:12], v[12]
        assert abs(sum(months) - total) <= max(50, total * 0.01), (st, sum(months), total)
        share = sum(months[5:8]) / total
        if st in RULE_AFTER_2024:
            g = "rule adopted after 2024"
        elif r["rule"] == "No hot-weather rule":
            g = "no rule"
        elif r["covers"] == "subset":
            g = "rule covers some customers"
        else:
            g = "rule covers everyone"
        groups.setdefault(g, []).append((st, share, months[6], total))

    us = rows.get("U.S. Total") or rows.get("U.S. total")
    print("States parsed:", len(rows))
    if us:
        print(f"U.S. total 2024: {us[12]:,}; July {us[6]:,}; summer share {sum(us[5:8]) / us[12]:.1%}")
    print("Even spread would give a summer (Jun-Aug) share of 25.0%.\n")
    for g in ["no rule", "rule covers some customers", "rule covers everyone", "rule adopted after 2024"]:
        xs = groups.get(g, [])
        if not xs:
            continue
        sh = [x[1] for x in xs]
        pooled = sum(x[1] * x[3] for x in xs) / sum(x[3] for x in xs)
        summer = sum(x[1] * x[3] for x in xs)
        print(f"{g}: {len(xs)} states, median summer share {statistics.median(sh):.1%}, "
              f"pooled {pooled:.1%}, Jun-Aug disconnections {round(summer):,}")
    print("\nLowest summer shares:")
    allx = sorted((x for xs in groups.values() for x in xs), key=lambda x: x[1])
    for st, sh, jul, tot in allx[:8]:
        print(f"  {st}: {sh:.1%} (July {jul:,} of {tot:,})")
    print("Highest summer shares:")
    for st, sh, jul, tot in allx[-8:]:
        print(f"  {st}: {sh:.1%} (July {jul:,} of {tot:,})")


if __name__ == "__main__":
    main()
