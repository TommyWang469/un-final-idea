#!/usr/bin/env python3
"""Idea 6: on how many dangerous-heat days a year can a household legally lose its electricity?

Run:  /usr/bin/python3 build.py        (stdlib only; everything fetched is cached under raw/)
Writes states.csv, result.md and site/data.js. Every number in those files comes from here.

Inputs
  rules.csv                     each state's hot-weather rule, hand-coded from its own legal text
  policies_raw.csv              the federal clearinghouse table (used only for the list of states)
  raw/CenPop2020_Mean_CO.txt    Census 2020 county populations and population centres
  api.weather.gov               forecast zone of each county centre
  Iowa Environmental Mesonet    heat-alert history per zone, and daily airport-station records

Today's rules are applied to the last ten years of weather. Observed weather stands in for the
forecasts the rules actually use.
"""
import csv, datetime, json, math, os, statistics, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
R = lambda *p: os.path.join(HERE, "raw", *p)
YEARS = range(2015, 2025)
TOP_N = 5
SKIP = {"Alaska", "Hawaii"}
# Rules that were replaced recently, kept only to measure what the change bought.
# California: 100°F on a 72-hour look-ahead until the commission's July 2026 resolution.
# Illinois: 95°F and no alert trigger until Public Act 103-0019.
OLD_RULES = {"California": {"temp": "100", "alerts": ""}, "Illinois": {"temp": "95", "alerts": ""}}
WARNINGS = {"HT.Y", "EH.W", "XH.W"}          # "dangerous heat" as the weather service itself calls it
ABBR = dict(zip("Alabama Arizona Arkansas California Colorado Connecticut Delaware Florida Georgia Idaho Illinois Indiana Iowa Kansas Kentucky Louisiana Maine Maryland Massachusetts Michigan Minnesota Mississippi Missouri Montana Nebraska Nevada Ohio Oklahoma Oregon Pennsylvania Tennessee Texas Utah Vermont Virginia Washington Wisconsin Wyoming".split(),
                "AL AZ AR CA CO CT DE FL GA ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV OH OK OR PA TN TX UT VT VA WA WI WY".split()))
ABBR.update({"District of Columbia": "DC", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
             "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Rhode Island": "RI",
             "South Carolina": "SC", "South Dakota": "SD", "West Virginia": "WV"})


def get(url):
    hdr = {"User-Agent": "student research project (zhouyimins@gmail.com)", "Accept": "application/geo+json"}
    time.sleep(0.6)
    for attempt in range(6):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=120).read().decode()
        except Exception as e:
            err = e
            time.sleep(30 if "429" in str(e) else 2 + 2 * attempt)      # the archive rate-limits
    raise err


def cached(path, url):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w").write(get(url))
    return open(path).read()


def counties():
    by, total = {}, {}
    for r in csv.DictReader(open(R("CenPop2020_Mean_CO.txt"), encoding="utf-8-sig")):
        pop = int(r["POPULATION"])
        total[r["STNAME"]] = total.get(r["STNAME"], 0) + pop
        by.setdefault(r["STNAME"], []).append((pop, float(r["LATITUDE"]), float(r["LONGITUDE"]), r["COUNAME"]))
    return {s: sorted(v, reverse=True)[:TOP_N] for s, v in by.items()}, total


def zone_of(state, name, lat, lon, zones):
    key = f"{state}|{name}"
    if key not in zones:
        zones[key] = json.loads(get(f"https://api.weather.gov/points/{lat:.4f},{lon:.4f}"))["properties"]["forecastZone"].rsplit("/", 1)[1]
    return zones[key]


def alert_days(ugc, lon):
    """{date: {code like 'HT.Y': local time the alert was first issued}} for one forecast zone.
    A day counts if the alert overlaps 09:00-21:00 local time; local time is approximated from
    longitude. Issuance time is read from the product id and falls back to the start time."""
    body = cached(R("alerts", ugc + ".json"), f"https://mesonet.agron.iastate.edu/json/vtec_events_byugc.py?ugc={ugc}"
                  f"&sdate={YEARS[0]}-01-01&edate={YEARS[-1]}-12-31")
    off, out = datetime.timedelta(hours=round(lon / 15)), {}
    for e in json.loads(body)["events"]:
        code = f"{e['phenomena']}.{e['significance']}"
        if e["phenomena"] not in ("HT", "EH", "XH") or not e["issue"] or not e["expire"]:
            continue
        a = datetime.datetime.strptime(e["issue"][:16], "%Y-%m-%dT%H:%M") + off
        b = datetime.datetime.strptime(e["expire"][:16], "%Y-%m-%dT%H:%M") + off
        pid = (e.get("product_id") or "")[:12]
        sent = datetime.datetime.strptime(pid, "%Y%m%d%H%M") + off if pid.isdigit() and len(pid) == 12 else a
        d = a.date()
        while d <= b.date():
            day0 = datetime.datetime.combine(d, datetime.time(9))
            if a < day0 + datetime.timedelta(hours=12) and b > day0:
                day = out.setdefault(d, {})
                day[code] = min(sent, day.get(code, sent))
            d += datetime.timedelta(1)
    return out


def stations(abbr):
    g = json.loads(cached(R("stations", abbr + "_ASOS.geojson"), f"https://mesonet.agron.iastate.edu/geojson/network/{abbr}_ASOS.geojson"))
    return [(f["properties"]["sid"], f["geometry"]["coordinates"][1], f["geometry"]["coordinates"][0])
            for f in g["features"]
            if (f["properties"].get("archive_begin") or "9999") <= f"{YEARS[0]}-01-01" and f["properties"].get("online")]


def station_days(abbr, sid):
    """{date: (max temperature F, max heat index F)} from one airport station."""
    q = urllib.parse.urlencode({"network": abbr + "_ASOS", "stations": sid, "year1": YEARS[0], "month1": 1, "day1": 1,
                                "year2": YEARS[-1], "month2": 12, "day2": 31, "format": "csv"})
    body = cached(R("asos", f"{abbr}_{sid}.csv"), f"https://mesonet.agron.iastate.edu/cgi-bin/request/daily.py?{q}&var=max_temp_f&var=max_feel")
    out = {}
    for r in csv.DictReader(body.splitlines()):
        try:
            t = float(r["max_temp_f"])
        except ValueError:
            continue
        try:
            f = float(r["max_feel"])           # can sit below the air temperature in dry heat; that is correct
        except ValueError:
            f = None
        out[datetime.date.fromisoformat(r["day"])] = (t, f)
    return out


def prefetch(net, sids):
    """One request for several stations of a network; the archive rate-limits per request."""
    need = [s for s in sids if not os.path.exists(R("asos", f"{net}_{s}.csv"))]
    if not need:
        return
    q = urllib.parse.urlencode([("network", net + "_ASOS")] + [("stations", s) for s in need] +
                               [("year1", YEARS[0]), ("month1", 1), ("day1", 1), ("year2", YEARS[-1]),
                                ("month2", 12), ("day2", 31), ("format", "csv"), ("var", "max_temp_f"), ("var", "max_feel")])
    rows = get(f"https://mesonet.agron.iastate.edu/cgi-bin/request/daily.py?{q}").splitlines()
    os.makedirs(R("asos"), exist_ok=True)
    for s in need:
        open(R("asos", f"{net}_{s}.csv"), "w").write("\n".join([rows[0]] + [r for r in rows[1:] if r.startswith(s + ",")]) + "\n")


def nearest_station(abbr, lat, lon):
    """Closest long-running station that actually has summer data."""
    dist = lambda s: math.hypot((s[1] - lat) * 69, (s[2] - lon) * 69 * math.cos(math.radians(lat)))
    nets = sorted(set(ABBR.values()) - {"DC"})        # the nearest airport is often across a state line
    pool = sorted([s + (a,) for a in nets for s in stations(a)], key=dist)[:6]
    for net in {s[3] for s in pool}:
        prefetch(net, [s[0] for s in pool if s[3] == net])
    for s in pool:
        days = station_days(s[3], s[0])
        summer = sum(1 for d in days if 6 <= d.month <= 9)
        if summer >= 0.9 * 122 * len(YEARS):
            return s[0], dist(s), days
    raise RuntimeError(f"no usable station near {abbr} {lat},{lon}")


def trigger_days(rule, wx, alerts, dates):
    """Set of dates on which the rule's own trigger is met (before look-ahead and carry-over)."""
    hit = set()
    strict = rule["strict"] == "1"
    t0 = float(rule["temp"]) if rule["temp"] else None
    h0 = float(rule["hi"]) if rule["hi"] else None
    codes = set(rule["alerts"].split(";")) if rule["alerts"] else set()
    lo, hi = (rule["season"].split(":") if rule["season"] else ("01-01", "12-31"))
    for d in dates:
        if not lo <= d.strftime("%m-%d") <= hi:
            continue
        t, h = wx.get(d, (None, None))
        over = lambda v, x: v is not None and x is not None and (v > x if strict else v >= x)
        by = datetime.datetime.combine(d, datetime.time(int(rule["by_hour"]))) if rule.get("by_hour") else None
        alerted = any(c in codes and (by is None or sent <= by) for c, sent in alerts.get(d, {}).items())
        if over(t, t0) or over(h, h0) or alerted:
            hit.add(d)
    return hit


def in_force(rule, wx, alerts, dates):
    """Dates on which a shut-off is barred: the trigger is met that day, within the rule's
    look-ahead window, or (Texas) within the carry-over after an alert."""
    hit = trigger_days(rule, wx, alerts, dates)
    out = set(hit)
    for k in range(1, int(rule["lookahead"]) + 1):
        out |= {d - datetime.timedelta(k) for d in hit}
    for k in range(1, int(rule["carry"]) + 1):
        out |= {d + datetime.timedelta(k) for d in hit}
    return out & set(dates)                 # never count a day that was not asked about (no station record)


def selfcheck():
    d = [datetime.date(2024, 7, i) for i in range(1, 8)]
    wx = {d[2]: (96.0, 100.0), d[5]: (95.0, 106.0)}
    base = {"strict": "0", "temp": "95", "hi": "", "alerts": "", "season": "", "lookahead": "0", "carry": "0"}
    assert in_force(base, wx, {}, d) == {d[2], d[5]}
    assert in_force({**base, "strict": "1"}, wx, {}, d) == {d[2]}                       # "above 95" excludes 95
    assert in_force({**base, "lookahead": "2"}, wx, {}, d) == {d[0], d[1], d[2], d[3], d[4], d[5]}
    assert in_force({**base, "temp": "", "hi": "105"}, wx, {}, d) == {d[5]}
    noon, dawn = datetime.datetime(2024, 7, 2, 12), datetime.datetime(2024, 7, 2, 5)
    assert in_force({**base, "temp": "", "alerts": "HT.Y", "carry": "2"}, wx, {d[1]: {"HT.Y": noon}}, d) == {d[1], d[2], d[3]}
    late = {**base, "temp": "", "alerts": "EH.W", "by_hour": "8"}
    assert in_force(late, wx, {d[1]: {"EH.W": noon}}, d) == set()          # issued after the 8 a.m. cutoff
    assert in_force(late, wx, {d[1]: {"EH.W": dawn}}, d) == {d[1]}
    assert in_force({**base, "temp": "", "hi": "100"}, {d[0]: (101.0, None)}, {}, d) == set()   # unknown heat index is not a trigger
    assert in_force({**base, "season": "07-04:07-31"}, wx, {}, d) == {d[5]}
    assert in_force({**base, "lookahead": "2"}, wx, {}, d[2:]) == {d[2], d[3], d[4], d[5]}   # look-ahead stays inside the days given


def main():
    selfcheck()
    top, total = counties()
    rules = {r["state"]: r for r in csv.DictReader(open(os.path.join(HERE, "rules.csv")))}
    table = {r["state"]: r for r in csv.DictReader(open(os.path.join(HERE, "policies_raw.csv")))}
    checked = {r["state"]: r for r in csv.DictReader(open(os.path.join(HERE, "no_rule_check.csv")))}
    states = [s for s in sorted(table) if s not in SKIP]
    zpath = R("zones.json")
    zones = json.load(open(zpath)) if os.path.exists(zpath) else {}
    jobs = [(s, c) for s in states for c in top[s]]
    for s, c in jobs:                          # one request at a time: the archive rate-limits
        zone_of(s, c[3], c[1], c[2], zones)
    json.dump(zones, open(zpath, "w"), indent=0, sort_keys=True)

    dates = [datetime.date(y, 1, 1) + datetime.timedelta(i) for y in YEARS for i in range(366)
             if (datetime.date(y, 1, 1) + datetime.timedelta(i)).year == y]
    out, far = [], []
    for s in states:
        rule = rules.get(s)
        w = sum(c[0] for c in top[s])
        old = {**rule, **OLD_RULES[s]} if s in OLD_RULES else None
        acc = {k: 0.0 for k in ("old_on", "old_alert_open", "on", "alert", "alert_open", "hot95", "hot95_open", "hi105", "hi105_open")}
        zone_alerts = [alert_days(zone_of(s, c[3], c[1], c[2], zones), c[2]) for c in top[s]]
        statewide = {}                              # Rhode Island: an alert anywhere in the state counts
        for za in zone_alerts:
            for d, codes in za.items():
                for c, sent in codes.items():
                    statewide.setdefault(d, {})[c] = min(sent, statewide.get(d, {}).get(c, sent))
        for (pop, lat, lon, name), al in zip(top[s], zone_alerts):
            sid, miles, wx = nearest_station(ABBR[s], lat, lon)
            if miles > 40:
                far.append(f"{name}, {s} ({sid}, {miles:.0f} mi)")
            known = [d for d in dates if d in wx]      # a day with no station record is left out, not called unprotected
            on = in_force(rule, wx, statewide if rule.get("scope") == "state" else al, known) if rule else set()
            danger = {"alert": {d for d in known if WARNINGS & set(al.get(d, {}))},
                      "hot95": {d for d in known if wx[d][0] >= 95},
                      "hi105": {d for d in known if wx[d][1] is not None and wx[d][1] >= 105}}
            share, n = pop / w, len(YEARS)
            acc["on"] += share * len(on) / n
            if old:
                old_on = in_force(old, wx, al, dates)
                acc["old_on"] += share * len(old_on) / n
                acc["old_alert_open"] += share * len(danger["alert"] - old_on) / n
            for k, ds in danger.items():
                acc[k] += share * len(ds) / n
                acc[k + "_open"] += share * len(ds - on) / n
        out.append({"state": s, "abbr": ABBR[s], "rule": rule, "cover": w / total[s], "pop": total[s], **acc})

    # ---------- outputs ----------
    def describe(r):
        if not r:
            return "No hot-weather rule"
        bits = []
        if r["temp"]:
            bits.append(f"{'above' if r['strict'] == '1' else 'at or above'} {r['temp']}°F")
        if r["hi"]:
            bits.append(f"heat index {'above' if r['strict'] == '1' else 'at or above'} {r['hi']}°F")
        if r["alerts"]:
            a = set(r["alerts"].split(";"))
            bits.append("weather-service " + ("excessive heat warning" if "HT.Y" not in a else
                        "heat advisory, warning or watch" if "EH.A" in a else "heat advisory or warning"))
        return " or ".join(bits) + (f" ({r['season'].replace(':', ' to ')} only)" if r["season"] else "")

    with open(os.path.join(HERE, "states.csv"), "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["state", "rule", "covers", "covers_note", "verified", "days_rule_in_force", "alert_days",
                     "alert_days_unprotected", "days_95F", "days_95F_unprotected", "days_hi105",
                     "days_hi105_unprotected", "share_of_state_population_sampled", "source"])
        for o in out:
            r = o["rule"] or {}
            wr.writerow([o["state"], describe(o["rule"]), r.get("covers", ""), r.get("covers_note", ""),
                         r.get("verified", "no rule: " + checked.get(o["state"], {}).get("level", "two compilations agree"))] +
                        [round(o[k], 1) for k in ("on", "alert", "alert_open", "hot95", "hot95_open", "hi105", "hi105_open")] +
                        [round(o["cover"], 2), r.get("source", checked.get(o["state"], {}).get("source", "https://liheapch.acf.gov/Disconnect/disconnect.htm"))])

    ruled = [o for o in out if o["rule"]]
    none = [o for o in out if not o["rule"]]
    full = [o for o in ruled if o["rule"]["covers"] == "all"]
    tot = lambda k, grp: sum(o[k] for o in grp)
    L = ["# Idea 6 result — generated by build.py, do not edit by hand\n",
         f"{len(out)} jurisdictions (48 states and DC). {len(ruled)} have a hot-weather shut-off rule; "
         f"{len(none)} have none. Of the {len(ruled)}, {len(ruled) - len(full)} protect only some customers "
         f"({', '.join(o['state'] for o in ruled if o['rule']['covers'] != 'all')}).\n",
         f"Weather: {YEARS[0]}-{YEARS[-1]}, nearest long-running airport station to the population centre of "
         f"each state's {TOP_N} most populous counties, weighted by county population. Those counties hold "
         f"{min(o['cover'] for o in out):.0%} to {max(o['cover'] for o in out):.0%} of their state's people "
         f"(median {statistics.median(o['cover'] for o in out):.0%}).\n",
         f"Rules read from the state's own legal text: {sum(o['rule']['verified'] == 'primary' for o in ruled)} "
         f"of {len(ruled)}. The rest rest on a secondary source and are marked.\n",
         "A *dangerous day* here is a day the National Weather Service had a heat advisory or (excessive) "
         "heat warning out for the county's forecast zone. Days at or above 95°F and days with a heat index "
         "at or above 105°F are shown beside it.\n",
         "## States with a rule: is it in force when the weather service says the heat is dangerous?\n",
         "| State | Rule | Days a year in force | Alert days a year | of which unprotected | Share unprotected | Read from |",
         "|---|---|---|---|---|---|---|"]
    share = lambda o: o["alert_open"] / o["alert"] if o["alert"] >= 0.5 else None
    for o in sorted(full, key=lambda o: -(share(o) if share(o) is not None else -1)):
        sh = f"{share(o):.0%}" if share(o) is not None else "n/a"
        L.append(f"| {o['state']} | {describe(o['rule'])} | {o['on']:.1f} | {o['alert']:.1f} | "
                 f"{o['alert_open']:.1f} | {sh} | {o['rule']['verified']} |")
    L += ["\n## States whose rule covers only some customers\n",
          "| State | Rule | Who is covered | Days a year in force for them | Alert days a year (everyone else is unprotected on all of them) |",
          "|---|---|---|---|---|"]
    for o in ruled:
        if o["rule"]["covers"] != "all":
            L.append(f"| {o['state']} | {describe(o['rule'])} | {o['rule']['covers_note']} | {o['on']:.1f} | {o['alert']:.1f} |")
    L += ["\n## States with no hot-weather rule, most alert days first\n",
          "| State | Alert days a year | Days at or above 95°F | Days with heat index at or above 105°F |", "|---|---|---|---|"]
    for o in sorted(none, key=lambda o: -o["alert"]):
        L.append(f"| {o['state']} | {o['alert']:.1f} | {o['hot95']:.1f} | {o['hi105']:.1f} |")

    # headline comparisons
    med_rule = statistics.median(o["alert"] for o in full)
    hot_none = [o for o in none if o["alert"] > med_rule]
    gaps = [o for o in full if share(o) is not None and share(o) >= 0.5]
    tight = [o for o in full if share(o) is not None and share(o) <= 0.1]
    L += ["\n## Headline numbers\n",
          f"- Among the {len(full)} states whose rule covers all residential customers, {len(gaps)} leave at "
          f"least half of their weather-service alert days unprotected"
          + (": " + ", ".join(f"{o['state']} ({share(o):.0%})" for o in sorted(gaps, key=lambda o: -share(o))) if gaps else "") + ".",
          f"- {len(tight)} of them leave one alert day in ten or fewer unprotected"
          + (": " + ", ".join(o["state"] for o in tight) if tight else "") + ".",
          f"- {len(hot_none)} of the {len(none)} states with no rule have more alert days a year than the median "
          f"state with a full rule ({med_rule:.1f}): " + ", ".join(f"{o['state']} ({o['alert']:.1f})" for o in sorted(hot_none, key=lambda o: -o["alert"])) + ".",
          "- Rules keyed to a weather-service alert cover every alert day by construction, so their 0% is not evidence "
          "that they are well set. The comparison is informative only for rules with a temperature or heat-index "
          "trigger, and for Mississippi's, which needs the rarer warning.",
          f"- Days a year a rule is in force range from {min(o['on'] for o in full):.1f} to {max(o['on'] for o in full):.1f} "
          f"across the {len(full)} full-coverage states.\n",
          "## Where the uncovered exposure is\n",
          "Uncovered alert days a year for an ordinary household, multiplied by state population. This is a scenario, "
          "not a measurement: it applies the weather of each state's five largest counties to the whole state, and in "
          "Arkansas and Indiana it treats every resident as outside the covered group.\n",
          "| Group | States | Share of uncovered person-alert-days |", "|---|---|---|"]
    opened = lambda o: o["alert"] if (not o["rule"] or o["rule"]["covers"] != "all") else o["alert_open"]
    whole = sum(o["pop"] * opened(o) for o in out)
    for label, grp in (("No hot-weather rule", none), ("Rule covers only some customers", [o for o in ruled if o["rule"]["covers"] != "all"]),
                       ("Rule covers everyone but misses alert days", full)):
        L.append(f"| {label} | {len(grp)} | {sum(o['pop'] * opened(o) for o in grp) / whole:.1%} |")
    L += ["\n## What two recent rule changes bought\n",
          "The old rule and the current rule, both run on the same 2015-2024 weather.\n",
          "| State | Old rule | Days in force, old | Days in force, now | Alert days uncovered, old | Alert days uncovered, now |",
          "|---|---|---|---|---|---|"]
    for o in out:
        if o["state"] in OLD_RULES:
            L.append(f"| {o['state']} | at or above {OLD_RULES[o['state']]['temp']}°F | {o['old_on']:.1f} | {o['on']:.1f} | "
                     f"{o['old_alert_open']:.1f} | {o['alert_open']:.1f} |")
    L += ["\n## Limits\n",
          "- **Observed weather stands in for forecasts.** Rules act on forecasts, which can be wrong in either direction.",
          "- **Today's rules, past weather.** Several rules changed between 2023 and 2026; this applies the current rule to 2015-2024.",
          "- **Airport stations.** Readings come from the nearest long-running airport, not from neighbourhoods."
          + (f" Stations more than 40 miles from the county centre: {'; '.join(far)}." if far else " No station is more than 40 miles from its county centre."),
          f"- **Top {TOP_N} counties per state.** Rural areas are under-represented.",
          "- **Alert history is per forecast zone as zones are drawn today.** Where a zone was redrawn, early years can be undercounted.",
          "- **Alerts became more frequent over the period.** The archive holds about four times as many heat advisories "
          "and warnings for these zones in 2024 as in 2015. Some of that is hotter weather and some is the weather service "
          "lowering its criteria in places, so a ten-year average understates today's alert frequency.",
          "- **An alert day means the alert overlapped 09:00 to 21:00 local time.** Alerts confined to the night are not counted.",
          "- **Days with no station record are left out,** for the rule and for the danger counts alike.",
          "- **Alert criteria differ by region.** A heat advisory in Maine and one in Arizona are not the same temperature. That is deliberate: it is the weather service's own local definition of dangerous.",
          "- **Texas is undercounted.** Its rule triggers on an advisory anywhere in the utility's territory; this checks only the customer's own zone.",
          "- **Arizona is scored on its temperature option.** A utility may instead adopt a June 1 to October 15 moratorium, which protects more days.",
          "- **Who a rule covers is simplified.** Many rules apply only to regulated utilities, or only where electricity runs the cooling. Cooperatives and municipal utilities are often outside them.",
          "- **The no-rule list is the weakest input.** A state is counted as having no rule only where two independent "
          "compilations agree: the federal LIHEAP Clearinghouse table and ElectricRates.org's state table (August 2026). "
          "The federal table alone lists Maine, Minnesota, New York and Oregon as having no rule, and all four have one. "
          f"Of the {len(none)} no-rule states, {sum(o['state'] in checked for o in none)} were checked further "
          f"({sum(checked.get(o['state'], {}).get('level', '').startswith(('own code', 'regulator')) for o in none)} against the state's own code or regulator, "
          f"{sum(checked.get(o['state'], {}).get('level') == 'news report' for o in none)} against a news report); they hold "
          f"{sum(o['pop'] * o['alert'] for o in none if o['state'] in checked) / sum(o['pop'] * o['alert'] for o in none):.0%} "
          "of the no-rule group's person-alert-days. The rest rest on the two compilations. See `no_rule_check.csv`.",
          "- **A rule in force is not a shut-off prevented.** This counts legal protection, not what utilities did.\n"]
    open(os.path.join(HERE, "result.md"), "w").write("\n".join(L) + "\n")

    site = [{"state": o["state"], "abbr": o["abbr"], "rule": describe(o["rule"]),
             "covers": (o["rule"] or {}).get("covers", "none"), "note": (o["rule"] or {}).get("covers_note", ""),
             "verified": (o["rule"] or {}).get("verified", checked.get(o["state"], {}).get("level", "none")),
             "source": (o["rule"] or {}).get("source", checked.get(o["state"], {}).get("source", "https://liheapch.acf.gov/Disconnect/disconnect.htm")),
             "quote": (o["rule"] or {}).get("quote", checked.get(o["state"], {}).get("quote", "")),
             "pop": o["pop"],
             **{k: round(o[k], 1) for k in ("on", "alert", "alert_open", "hot95", "hot95_open", "hi105", "hi105_open")}}
            for o in out]
    os.makedirs(os.path.join(HERE, "site"), exist_ok=True)
    open(os.path.join(HERE, "site", "data.js"), "w").write(
        "// generated by build.py, do not edit\nconst STATES = " + json.dumps(site, indent=0) + ";\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
