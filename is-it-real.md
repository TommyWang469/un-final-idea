# Is the problem real? (checked 2026-10-21)

**Yes.** Nothing found says otherwise. The EIA numbers below were re-run on 2026-10-21 from the
federal report saved at `raw/eia_disconnections_2024.pdf` and came out the same. Full sources
are in `nonprofit-playbook.md`, Part 1.

## What "July was the lowest month" means

It is a national figure, and it means only this: don't say "summer is when the most people get
cut off." It does not mean summer shut-offs are rare. There were still 967,012 electric
shut-offs nationally in July 2024. The national dip partly comes from states that already
protect people in summer.

## The evidence

1. **Shut-offs keep happening in summer where there's no rule** (EIA, June to August 2024):
   - Florida, no rule: 524,907. That is 24.1% of its year, about what an even spread would give,
     so summer slows nothing down.
   - Alabama, no rule: 120,998.
   - Georgia, no rule: 124,002.
   - All 24 no-rule states together: 1,412,514.
2. **Rules work.** Arizona, which pauses shut-offs in summer, had 3,499 from June to August
   against 29,023 in December alone, or 3.1% of its year. The fix is proven, and half the states
   don't have it.
3. **People have died.** Two Arizona deaths are documented:
   - Stephanie Pullman, 2018: cut off over $51 on a 107°F day (AP).
   - Katherine Korman, 2024: her utility had dropped its heat policy three days before cutting
     her off. It later paid a $7 million settlement (Courthouse News).
4. **Lawmakers treat it as real.** California tightened its rule in July 2026. Massachusetts has
   a bill in conference. Florida and Vermont had bills that stalled.

## The one honest weak spot

Nobody counts how many people are *harmed* by heat-wave shut-offs. There are shut-off counts and
two documented deaths, but no total for injuries or deaths. Maricopa County's heat-death reports
don't say whether a person's power was off because of an unpaid bill.

- Never say: "shut-offs kill X people a year."
- Say instead: "X shut-offs happened in summer in states with no protection, and people have
  died this way."

This limits what you can claim. It doesn't make the problem fake.

## Bottom line

You won't do all this work and then find there's no problem. The risk is overclaiming, not a
fake problem. Stick to the wording above.

## Reproduce the state numbers

```sh
uv run -q --with pdfplumber python -c "
import eia_check as e; r = e.table5()
for s in ['Florida', 'Arizona', 'Alabama', 'Georgia']:
    v = r[s]; print(s, f'{sum(v[5:8]):,}', f'{sum(v[5:8]) / v[12]:.1%}')"
```

The no-rule total (1,412,514) is printed by `uv run --with pdfplumber python eia_check.py`.
