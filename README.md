# Can your power be cut off in a heat wave?

Chosen as the final capstone idea on 2026-10-17. It was Idea 6 in `un-brainstorm`
(`ideas/heat_shutoffs/`), where the analysis was built on 2026-10-10. Everything was copied here,
and `build.py` reproduces `result.md` byte-for-byte from this folder.

## The project: where it is going

The counselor's advice was to build the website for sure. The plan has three parts, in order:

1. **The website.** Each state's rule and how many of its dangerously hot days the rule covers.
   It starts from `site/`, which already works locally but isn't deployed.
2. **An advocacy guide on the site.** It teaches people how to contact their lawmakers and ask
   for a hot-weather shut-off rule, or a better one. The guide should be specific to each state:
   what the state has now, what its gap is in alert days, and who to contact.
3. **Local chapters in other states.** These are students who take the guide to their own
   legislators.

**Who to contact: mostly state lawmakers, not Congress.** Every rule in `rules.csv` is a state
statute or a state utility-commission regulation. So the people who can create or change a rule
are state legislators and the state's public utility commission. Members of Congress can't change
these rules. The guide should send people to their state legislator and their utility commission
first. Congress only matters if a federal bill on utility shut-offs exists. None has been checked
for this project, so look before the guide mentions one.

**What each state's advocacy page can say, from the data we already have:**
- The 24 no-rule states: "your state has no rule; here are its alert days a year" (for example,
  Kansas 14.2, Alabama 10.9, Pennsylvania 9.4).
- States with a weak rule: Delaware and Mississippi miss 76% of their alert days, and Missouri
  misses 44%. The ask is to change the trigger.
- Proof that a change works: California's July 2026 move from 100°F to 90°F cut its uncovered
  alert days from 4.0 to 1.1 a year. Illinois's change cut its uncovered days from 0.9 to 0.0.

**Before anything goes public (the guide included):**
- The three conditions at the end of this file still apply. Tommy re-reads all 25 rules and signs
  off `rules.csv`, an expert looks at the rule table, and the last 8 no-rule states are confirmed.
  An advocacy page that is wrong about a state's law does more harm than a report would.
- A chapter counts once it has a real person running it. Until then, the site says "start a
  chapter", not "chapters in N states".

**Ground rules** (carried over from `un-brainstorm`):
- **Never invent a number.** Every figure traces to `build.py` output.
- **Never inflate a role or a team's size.**
- **This is a nonprofit project** (Tommy's decision, 2026-10-17). It replaces the old
  `un-brainstorm` rule "don't found anything". How to set it up is covered in `nonprofit-playbook.md`.
- **Stays smaller than the hurdle AI**, which is the ISEF project. Chapters are the part most
  likely to grow without limit, so they come last.
- **No claim about a UN conference** until a specific named event has accepted the project.
- **Nothing goes on an application until it exists and is public.**

---

# The analysis

Built 2026-10-10. Every number below is copied from `result.md`, which `build.py` regenerates.

## The question

Some US states bar utilities from disconnecting a household's electricity for an unpaid bill
during extreme heat. **For each state: on how many of the days the National Weather Service
called dangerously hot was a household actually protected by the state's rule?**

## What it found

1. **About half the country has no rule.** Of 49 jurisdictions (48 states and DC), 25 have a
   hot-weather shut-off rule and 24 have none. Two of the 25 (Arkansas, Indiana) cover only some
   customers.
2. **That is where the exposure is.** 78.9% of uncovered person-alert-days are in states with no
   rule, 6.1% in the two states that cover only some customers, and 15.0% in states whose rule
   covers everyone but misses some alert days. This split is a scenario, not a measurement.
3. **Where a rule covers everyone, it usually works.** 16 of 23 such states leave one alert day
   in ten or fewer uncovered. Rules tied to a weather-service alert cover alert days by
   construction, so this is a real test only for the temperature and heat-index rules.
4. **Two rules miss most of the danger.** Delaware leaves 76% of its alert days uncovered (heat
   index of 105°F, 2.9 days a year in force against 9.4 alert days). Mississippi leaves 76%
   (it needs an excessive heat warning, the rarer alert, issued by 8 a.m.). Missouri leaves 44%.
5. **Some no-rule states are hot.** 8 of the 24 have more alert days a year than the median state
   with a full rule (7.2): Kansas (14.2), Alabama (10.9), Pennsylvania (9.4), Tennessee (8.4),
   Florida (8.4), Nebraska (8.2), Connecticut (8.1), Massachusetts (7.9). Florida also has 20.2
   days a year with a heat index at or above 105°F.
6. **Two recent rule changes can be measured.** Run on the same ten years of weather,
   California's July 2026 move from 100°F to 90°F takes the rule from 20.1 to 81.6 days a year
   in force and uncovered alert days from 4.0 to 1.1. Illinois's move from 95°F to 90°F plus
   alerts takes it from 2.6 to 18.2 days in force and from 0.9 to 0.0 uncovered.
7. **The federal reference table is wrong in ways that matter.** The LIHEAP Clearinghouse table
   lists Maine, Minnesota, New York and Oregon as having no hot-weather rule; all four have one.
   It also misstates the trigger in several states that do (heat index reported as temperature in
   Delaware and Oklahoma, an advisory rule reported as 98°F in Georgia, superseded thresholds in
   California and Illinois).

**What it did not find.** The idea began as "rules exist on paper but are set too high to ever
trigger." That is true of Delaware and Mississippi and partly of Missouri. It is not true in
general. The larger problem is the absence of rules, which was already known as a count; what is
new here is the size of it in alert days and where it falls.

## How it was built

| File | What it is |
|---|---|
| `rules.csv` | Each state's rule, hand-coded: trigger, look-ahead, season, who is covered, the source link and the quoted text. 23 of 25 were read from the state's own legal text; 2 rest on a secondary source and are marked (Indiana, New York). |
| `build.py` | Applies today's rules to 2015-2024 weather. Stdlib only. `/usr/bin/python3 build.py` |
| `result.md`, `states.csv` | Output. |
| `site/` | A results page that reads `site/data.js`. `cd site && python3 -m http.server`, then open `localhost:8000`. Not deployed. |
| `no_rule_check.csv` | For 16 no-rule states, the source showing there is no hot-weather rule. |
| `policies_raw.csv`, `policy_sources.csv` | The federal clearinghouse table as extracted, kept to show where it differs. |
| `raw/` | Everything downloaded: the clearinghouse page, Census county centres, forecast zones, alert history, airport-station records. |

**Weather:** daily maximum temperature and heat index from the nearest long-running airport
station to the population centre of each state's five most populous counties, weighted by county
population. **Dangerous day:** the weather service had a heat advisory or (excessive) heat warning
out for that county's forecast zone. **Covered:** today's rule would have barred a shut-off.

The full list of limits is at the end of `result.md`. The three that matter most:

- **The legal coding has not been checked by a lawyer or a regulator.** Most rules were read
  through a tool that quotes a page in answer to a question, not by reading the whole rule.
- **The no-rule list is the weakest input.** A state counts as having no rule only where two
  independent compilations agree. 16 of the 24 were checked further (13 against the state's own
  code or regulator, 3 against a news report or legal-aid summary); they hold 92% of the
  no-rule group's person-alert-days. The other 8 rest on the compilations. See `no_rule_check.csv`.
- **It counts legal protection, not what happened.** No disconnection data is used.

## Mistakes caught along the way

Kept because each one would have produced a confident wrong claim.

- **A first quick test passed for the wrong reason.** It took the federal table at face value;
  three of the four states behind the pass were errors in that table.
- **A heat-index estimate was far too high in humid places.** It was built from daily mean
  humidity, and when checked against airport records for Miami, Tampa and Oklahoma City it
  overcounted dangerous days severalfold. Every heat-index figure now comes from station
  records. The check was run by hand and is not part of `build.py`.
- **New York was nearly reported as the second-worst unprotected state.** It has a rule, adopted
  March 2026. Checking it exposed three more states the federal table gets wrong.
- **A Codex review of `build.py` found seven real problems, all fixed.** Days with no station
  record were being counted as unprotected. A shortcut never let the heat index sit below the air
  temperature, which added a trigger to heat-index-only rules. Mississippi's and Georgia's 8 a.m.
  cutoffs were ignored. The nearest station was searched only within the state. Rhode Island's
  statewide trigger was scored by zone. The exposure split was not labelled as a scenario. The
  daytime window for an alert day was not stated. None changed the two headline conclusions.
- **The page-question tool gives false confirmations.** Asked whether a page contains a heat
  provision, it answered "no heat provision" for pages that had redirected to an index or
  returned "not found". Three such answers (North Dakota, South Carolina, West Virginia) were
  thrown out. A no-rule state is counted as checked only where the page's own title showed it
  was the right rule.
- **A second Codex pass confirmed six of the seven fixes and found one incomplete:** look-ahead
  could still count a day with no station record as a day in force. Fixed. It reproduced every
  headline number from the cached data. It also noted that the built-in self-check does not cover
  file parsing or station selection; that is still true.

## Prior work

Checked 2026-10-10, mostly through the same page-question tool.

- **Energy Justice Lab** (Indiana University; Carley and Konisky) reads every state's statute and
  tracks protections. Its June 2023 report counts 20 states with a hot-weather protection. Its 2024
  Nature Communications paper counts the days California's 100°F rule was in force, as an input to
  a study of disconnections. It has not published the count for every state that I found. Two of
  its papers were not read (paywalled).
- **National Consumer Law Center** (2024) recommends rules use heat index or weather-service
  alerts. No count.
- **ElectricRates.org** (August 2026) publishes a state table. No count, and it misses New York.

The gap is real and narrow. The Energy Justice Lab could close it quickly and holds better data.

## Is it worth presenting at a UN-linked conference?

**Yes, as a student policy analysis, on three conditions. Not as a research breakthrough.**

For it:
- It answers a clear question about a named Sustainable Development Goal target: 7.1, universal
  access to affordable and reliable energy. It also bears on 13.1 (resilience to climate hazards)
  and 3 (health).
- Every claim is checkable. Each state's rule is quoted and linked, and the numbers regenerate.
- It has concrete results a listener can repeat: half the country has no rule; four-fifths of the
  uncovered exposure is there; Delaware's and Mississippi's rules miss about three-quarters of
  alert days; California's 2026 change is measurable.
- The method transfers: take any rule meant to protect people from a climate hazard and test
  whether it is in force when the hazard actually occurs.

Against it:
- It is about one country. A UN audience will ask what it says about anywhere else.
- The main finding is the least novel one. That many states have no rule is already reported.
- It is a count of legal protection, with no evidence about actual disconnections or health.
- An error about a state's law, said in public, is embarrassing and easy to make here.

The three conditions:
1. **Tommy re-reads all 25 rules himself**, from the legal text, and signs off `rules.csv`. This
   analysis was built in one sitting with an AI assistant; it cannot be presented as his until he
   has done that pass and can defend each row. This is the ground rule in the main README:
   never inflate a role.
2. **One person who knows this field looks at the rule table.** The Energy Justice Lab or the
   National Consumer Law Center are the obvious asks. A short email with `rules.csv` attached.
3. **The remaining 8 no-rule states are confirmed:** Michigan, Montana, New Hampshire, North Dakota, South Carolina, South Dakota, Vermont, Wyoming. All eight
   no-rule states with the most alert days are now checked; Kansas and Pennsylvania rest on news
   reports rather than the code, and Idaho on one section of its rules.

And the standing rule from the main README applies: nothing about a UN conference is claimed
anywhere until a specific named event has accepted it.
