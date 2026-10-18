# Nonprofit playbook: heat-wave power shut-offs

Written 2026-10-17. Every factual claim has a link. Numbers from this project's own analysis
come from `result.md`. Anything that couldn't be confirmed is marked **unverified**.

## Part 1. Is this a real problem that needs people to fix it?

**Verdict: yes, but the honest pitch is narrower than "no one is working on it."** People are
being disconnected in large numbers, and people have died. In 2024 the 24 states with no heat
rule cut off power 1.4 million times in June to August alone, while Arizona's summer pause cut
its summer shut-offs to 3,499. Half the states still have no heat rule. A bill is in conference
in Massachusetts now; Florida's and Vermont's stalled. But established groups already do research and lobbying on this. A student nonprofit adds
the most by bringing **volunteers in the states with no rule**, not by doing more research.

### 1.1 Scale: how many shut-offs

- **13,447,935 residential electric disconnections in 2024 ("13.4 million")**, plus 1.7 million
  gas disconnections. This is the first federal count, read directly from EIA's 2024 Residential
  Utility Disconnections Report (April 2026; saved as `raw/eia_disconnections_2024.pdf`;
  https://www.eia.gov/analysis/requests/residential/utility/). The Energy and Policy Institute
  rounds the same data to "13.5 million" electric and "1.6 million" gas; **use EIA's own
  figures.** EIA's survey response rate, weighted by residential customers, was 93.5% for
  electricity.
  - Careful with wording: 13.4 million is **disconnections, not households** ("Customer
    accounts may receive more than one disconnection in a year", EIA Table 5 note). The same home can
    be cut off more than once. The Energy Justice Lab says "approximately 15 million Americans",
    which is a different unit (people) (https://utilitydisconnections.org/). Pick one unit and
    cite its source.
- **Southern states account for about 71% of electric disconnections.** Texas, Florida and
  Oklahoma report the most (Energy and Policy Institute, same link). Of those three, Texas and
  Oklahoma have a heat rule in `rules.csv` and Florida does not.
- **Don't say "summer is the peak." Nationally it isn't.** In EIA's 2024 data, October had the
  most electric disconnections (1.5 million) and **July had the fewest (967,012)**. June to August
  was 22.9% of the year, against 25% if shut-offs were spread evenly. (An older Energy Justice Lab
  figure says "over 30%" were in summer 2022, from a different and smaller dataset. Don't mix
  the two.)
- **The honest claim is state by state. This is our own analysis:** `eia_check.py` reads EIA's
  Table 5 and groups states by `states.csv`.
  - **Rules visibly work where it's hot.** Arizona, where utilities may pause shut-offs from June
    1 to October 15, had **3,499** disconnections from June to August 2024, against **29,023** in
    December alone (3.1% of its year in summer).
  - **No-rule states keep cutting power all summer.** Florida, which has no rule:
    **524,907** disconnections from June to August 2024, including 186,202 in July alone. Alabama,
    no rule: 120,998 in summer.
  - **Across the 24 no-rule states: 1,412,514 summer disconnections in 2024**, out of about 3.1
    million nationally.
  - **A trap: don't compare the groups as wholes.** The no-rule group's summer share (pooled
    25.1%) is only somewhat above the full-rule group's (20.8%). That's because northern states
    with winter bans push shut-offs into summer: Minnesota 41.2%, Wisconsin 46.0%, Maine 42.5%.
    Those are mostly states whose heat rule depends on an alert. **Summer is when those households
    are cut off, and only on an alert day does the rule protect them.**
  - Limits: one year of data. EIA counts disconnection *events*, not households. Some state
    figures carry EIA's quality flags (R or Q). Rules are as of today, and New York (rule adopted
    2026) is set apart.
- **The same households get hit again.** "Half of all households whose power was disconnected
  dealt with disconnections multiple times" in a single year (same source; study
  https://doi.org/10.1088/1748-9326/ac90d7).

### 1.2 Who can't afford power

- 2020: **27% of US households (34 million)** had trouble paying energy bills or kept their
  home at an unsafe temperature (EIA, from the Residential Energy Consumption Survey).
  https://www.eia.gov/todayinenergy/detail.php?id=51979
- Census Household Pulse Survey, from a JAMA Network Open analysis: **22.4%** of adults were
  unable to pay an energy bill, and **22.0%** kept their home at an unsafe or unhealthy
  temperature because of cost. https://pmc.ncbi.nlm.nih.gov/articles/PMC12559964/
- "Over one in six households – more than 20 million families – are behind on their utility
  bills" (Rep. DelBene press release, 2024-07-25, quoting the national energy-assistance
  directors' group). https://delbene.house.gov/news/documentsingle.aspx?DocumentID=3901

### 1.3 Harm: what happens when the power goes off in heat

- **Stephanie Pullman**, 72, Sun City West, Arizona. Her utility, APS, cut her power in
  September 2018 on a 107°F day. She had a past-due bill of $176, and a $125 payment had been
  made days before, leaving $51. The medical examiner found "environmental heat exposure"
  combined with heart disease (AP, 2023-07-24).
  https://apnews.com/article/arizona-heat-death-legacy-3fce53af423293d9fb15d7889dee9e13
  - Note: an RMI article dates her death to "July 2024". That is wrong; AP says September 2018.
    Don't copy the RMI date.
- **Katherine Korman**, 82, an APS customer. APS remotely disconnected her power on 2024-05-13,
  a 99°F day, and she was found dead six days later. Arizona's rule lets each utility choose
  between a June 1 to October 15 pause and a 95°F forecast trigger. APS had dropped its
  temperature policy three days before cutting her off. In April 2026 APS agreed to a
  **$7 million settlement** with the Arizona Attorney General (Courthouse News, 2026-04-15).
  https://courthousenews.com/settlement-bars-arizona-utility-from-extreme-heat-disconnections/
  - This is the strongest single argument for the project's core method. **Having a rule on
    paper wasn't enough. What matters is whether the rule is in force on the day it's hot.**
- **Maricopa County (Phoenix): 608 heat deaths in 2024.** Of the indoor deaths, 88% had an air
  conditioner present, and 70% of those units weren't working (2024 report).
  https://www.maricopa.gov/ArchiveCenter/ViewFile/Item/5934. The county counted 645 in 2023 and
  430 in 2025 (https://www.maricopa.gov/m/newsflash/Home/Detail/3222 and the county's posts).
  - Don't overclaim. These reports don't say how many indoor deaths followed a utility
    shut-off. "No electricity" is a separate category (about 9% of one subgroup in the 2024
    slide), and it doesn't say why the power was off.
- **National heat deaths.** More than 2,300 death certificates mentioned heat in summer 2023,
  the most in 45 years of records. One researcher estimates the true number was about 11,000
  (AP analysis of CDC data).
  https://www.pbs.org/newshour/nation/2023-set-a-record-for-u-s-heat-deaths-why-2024-could-be-even-deadlier

### 1.4 The policy gap (from this project plus outside sources)

- **This project:** 24 of 49 jurisdictions have no heat rule, and 78.9% of uncovered
  person-alert-days fall in those states (`result.md`; the second figure is a scenario, not a
  measurement).
- Outside counts roughly agree, but each source counts differently. RMI: 42 states protect in
  extreme cold, 25 in extreme heat (2025-08-27,
  https://rmi.org/resources/summer-disconnections-make-the-living-less-easy/). Network for
  Public Health Law: "only half of states" (2026-07-22,
  https://www.networkforphl.org/resources/state-laws-to-prevent-utility-shutoffs-during-extreme-heat/).
  Energy Justice Lab (2024): "In 27 states, utilities can shut off electricity ... even in a heat
  wave."
- **The rules protect against cold far more often than heat**, even though bills peak in summer
  in most of the country. That's the Congressional Research Service's point
  (R47417, 2023-01-31, https://www.congress.gov/crs-product/R47417).

### 1.5 Who decides (this sets who the advocacy guide targets)

- "The federal role in utility disconnections is limited. Most aspects of electricity
  distribution are overseen by state or local regulators" (CRS R47417). **So the main targets
  are state legislators and state utility commissions.** That confirms what the README says.
- **There is a federal angle.** The PUDDLE Act (Preventing Unnecessary Deaths During
  Life-Threatening Events), introduced by Reps. DelBene and Blunt Rochester on 2024-07-25, would
  amend PURPA (a 1978 federal utility law) so that existing federal disconnection standards
  explicitly cover extreme heat and cold. Nearly 30 organizations backed it
  (https://delbene.house.gov/news/documentsingle.aspx?DocumentID=3901). Earlier versions were
  H.R. 9300 (117th Congress) and H.R. 9122 (118th). **No 119th-Congress PUDDLE Act was found** in
  searches of congress.gov and DelBene's site on 2026-10-17. A related current bill is
  **S. 1214, the Heating and Cooling Relief Act (March 2025)**, which states that 29 states have
  no summer shut-off protection
  (https://www.govinfo.gov/bulkdata/BILLS/119/1/s/BILLS-119s1214is.xml). The federal ask is a
  side note. The guide should lead with the state level.
- Federal money is also under pressure. HHS fired the entire federal LIHEAP staff on 2025-04-01,
  and the president's FY2026 budget proposed $0 for LIHEAP (NEADA,
  https://neada.org/press/liheap-under-threat/). LIHEAP is the federal program that helps
  low-income households pay energy bills. Congress funded it anyway: the FY2026 total is
  $4,130,596,037 (https://liheapch.acf.gov/Funding/funding.htm). The LIHEAP Clearinghouse, the
  federal table this project found errors in, is still online.

### 1.6 It's winnable: rules are changing right now

Recent wins, which show the issue moves:
- **California, 2026-07-16.** The utility commission voted 4-0 to lower the trigger from 100°F
  to 90°F, and ordered region-specific heat standards within six months. The utilities had
  argued 90°F was "overbroad" (CalMatters,
  https://calmatters.org/environment/2026/07/california-utility-heat-shutoff-rules-cpuc/; Center
  for Biological Diversity and TURN release,
  https://biologicaldiversity.org/w/news/press-releases/california-strengthens-protections-against-disconnections-during-extreme-heat-2026-07-16/).
  Our numbers: uncovered alert days go from 4.0 to 1.1 a year (`result.md`).
- **Arizona.** The commission adopted a heat rule after Pullman died (AP), and it was tightened
  for APS by the 2026 settlement (Courthouse News).
- **Washington, 2023.** A heat shut-off law, backed by the state Attorney General
  (https://www.atg.wa.gov/news/news-releases/ag-ferguson-rep-mena-bill-protecting-washingtonians-utility-shutoffs-during-0).
- **New York (March 2026) and Illinois.** Both are already in `rules.csv`.

Live fights in states that have **no rule** in `rules.csv`. These are where chapters matter most:
- **Massachusetts** (7.9 alert days a year, no rule). Bill S.2612, "utility shutoff protections
  during periods of extreme heat", filed by Sen. Comerford. The committee reported it favorably
  on 2025-12-08. On 2026-06-25 it was folded into H5175, the energy-affordability bill. On
  2026-07-16 H5175 went to a conference committee, where negotiators from the two chambers
  settle the final text (https://malegislature.gov/Bills/194/S2612,
  https://malegislature.gov/Bills/194/H5175). **The Senate's version (S.3143, passed 32-8 on
  2026-07-01) bars shut-offs for households in financial hardship when temperatures are expected
  to exceed 85°F for three days in a row, from May 15 to September 15** (Senate press release,
  https://malegislature.gov/PressRoom/Detail?pressReleaseId=1428). Conferees first met on
  2026-07-29 (https://www.mma.org/energy-affordability-legislation-goes-to-conference-committee/),
  and no final bill had reached the governor as of mid-October (WBUR, 2026-10-14). **This is
  the live, winnable fight. Whether the House keeps the heat provision is the open question.**
  If it passes, `rules.csv` needs a new row.
- **Vermont** (3.5 alert days, no rule). H.88 would bar disconnections at 92°F or above,
  introduced by Rep. Kate McCann (WCAX, 2025-02-28). **Its status page shows no action since it
  was referred to the House Energy and Digital Infrastructure Committee on 2025-01-24**
  (https://legislature.vermont.gov/bill/status/2026/H.88). The committee did take testimony,
  but the bill never left it.
- **Florida** (8.4 alert days, 20.2 days a year with heat index at or above 105°F, no rule). The
  PAUSE Act, H 419 / SB 330, backed by Food & Water Watch, **died in committee on 2025-06-16**
  (https://www.flhouse.gov/Sections/Bills/billsdetail.aspx?BillId=80992). Florida had 524,907
  summer disconnections in 2024 (EIA, above). **A dead bill plus the largest summer count in any
  no-rule state makes Florida the strongest case for a chapter.**
- **Pennsylvania** (9.4 alert days, no rule; 85,582 summer disconnections in 2024). The House
  version of the 2024 bill renewing Chapter 14 (Rep. Matzie) added a summer shut-off ban, but the
  Senate version (Sen. Boscola) left it out, and Chapter 14 lapsed on 2024-12-31 without being
  renewed. Chapter 14 is the state's law protecting utility customers, and it includes the winter
  ban (Spotlight PA, 2024-01 and 2024-12,
  https://www.spotlightpa.org/news/2024/12/pennsylvania-winter-utility-shutoff-consumer-protection-law-reauthorization/;
  WHYY, https://whyy.org/articles/pennsylvania-gas-electric-utility-shutoffs-protections-reauthorization-bill).
  In 2025–26 **SB 154** (Boscola, renewal) passed the Senate 41-7 on 2025-02-03, and **HB 2333**
  (Madsen, renewal plus notice and medical-certificate rules) passed the House on 2026-04-15. **No
  version had been signed as of these sources, and no summer ban appears in either one's
  published summary** (https://senatorboscola.com/boscolas-chapter-14-reenactment-bill-passes-senate-with-strong-bipartisan-support/,
  https://www.pahouse.com/madsen/InTheNews/NewsRelease/?id=143203). The utility commission is
  keeping winter protections in place for now (https://www.puc.pa.gov/pcdocs/1914863.pdf).
  **The opening:** both chambers are still negotiating renewal, so a summer ban can be pushed
  as an amendment.

### 1.7 The other side (know it before a legislator asks)

- **The debt doesn't disappear.** A pause doesn't cancel the bill. Arizona's commission says
  "charges for energy consumption will continue to accumulate during the moratorium"
  (https://azcc.gov/news/home/2024/06/03/acc-reminds-ratepayers-of-utility-disconnection-ban-during-extreme-heat).
  RMI argues pauses should come paired with programs that make bills affordable, so households
  don't land in a cycle of debt and disconnection (RMI link above).
- **Who pays.** The national association of state utility regulators said blanket COVID-era
  pauses left "customers and utilities alike ... unprepared for the massive arrearage burden."
  Regulators can make other customers cover unpaid bills through higher rates (CRS R47417).
  Expect utilities to raise this.
- **The threshold fight.** California's utilities called 90°F "overbroad" (CalMatters). This
  project's data answers that: a 100°F rule missed most dangerous days.
- **A pause isn't the whole fix.** Air conditioners break, as in Maricopa, where 70% of the
  indoor-death units weren't working. A shut-off rule covers only one way people end up without
  cooling.

### 1.8 Who already works on this (partners, not competitors)

| Group | What they do | Link |
|---|---|---|
| Energy Justice Lab (Indiana University) | Disconnection dashboard, state policy tracking, research | https://utilitydisconnections.org/ |
| Energy and Policy Institute | Utility watchdog; analyzed the EIA data | https://energyandpolicy.org/ |
| Center for Biological Diversity | Party to the California proceeding; "Powerless" reports | https://biologicaldiversity.org/ |
| TURN (The Utility Reform Network) | California ratepayer advocate; co-led the 90°F push | https://www.turn.org/ |
| National Consumer Law Center | Model rules (recommends a heat-index or alert trigger) | https://www.nclc.org/ |
| NEADA (energy-assistance directors) | LIHEAP funding; backed the PUDDLE Act | https://neada.org/ |
| RMI | Disconnections Handbook for regulators | https://rmi.org/insight/disconnections-handbook |
| Network for Public Health Law | 2026 state-law fact sheet | https://www.networkforphl.org/ |
| Food & Water Watch | Backed the Florida PAUSE Act | https://www.foodandwaterwatch.org/ |
| 350.org | Promotes the issue on social media; backed the PUDDLE Act | https://350.org/ |

No **student-led** group working on this issue turned up in searches. That gap is real but
narrow: the issue already has experts. **What's missing is organized volunteers in the no-rule
states.** That's the job a student chapter network can do.

---

## Part 2. Legal setup: how to be a nonprofit

Full detail with every source: `research/nonprofit-legal-setup.md`. The key figures below were
re-checked against the live official pages on 2026-10-17.

### 2.1 Three ways to be "a nonprofit"

| Option | What it is | Cost | When |
|---|---|---|---|
| **A. Fiscally sponsored project** | An existing 501(c)(3) takes the project in. Donations go to the sponsor, which controls the money and can give donors tax deductions. | A share of what you raise | **Now** |
| B. California nonprofit corporation + 501(c)(3) | Your own corporation, board and tax exemption | About $375 in filings (see 2.3) plus yearly filings | Once there's a team, money and a reason to be independent |
| C. 501(c)(4) | Lobbying can be the main activity, but donations aren't tax-deductible | $50 notice (Form 8976) | Only if paid lobbying for bills becomes the main work |

**Recommendation: Option A now, with Hack Club's fiscal-sponsorship program (HCB), if HCB
confirms in writing that it allows nonpartisan lobbying for bills (see the warning below).** That makes
this a real nonprofit project today, with a bank account, tax-deductible donations and a
501(c)(3) behind it, without a 16-year-old taking on a corporation's legal duties.
- HCB is built for "teenagers aged 13 to 18 who lead or organize mission-driven projects"
  (https://help.hcb.hackclub.com/en/articles/15409923-who-can-apply-for-fiscal-sponsorship).
- Fee: "7% of revenue", with no startup, transaction or card fees
  (https://hackclub.com/fiscal-sponsorship). It says it supports over 6,500 teen-led
  organizations.
- **Warning sign. Ask HCB in writing before building on it.** In March 2025, Hack Club's
  founder posted that "Hack Club does not fiscally sponsor any groups that engage in violence or
  political activity" (https://x.com/zachlatta/status/1899249078611169698). **HCB's official
  eligibility page is narrower.** Under "Who is not eligible" it lists only existing nonprofits
  and "projects that wouldn't qualify under 501(c)(3), such as for-profit ventures, political
  campaigns, or activities that mainly benefit private individuals". It says HCB "rarely
  restricts" categories and "When in doubt, apply"
  (https://help.hcb.hackclub.com/en/articles/15409923-who-can-apply-for-fiscal-sponsorship,
  read in full 2026-10-17). Election campaigns are banned for every 501(c)(3) anyway, while
  limited nonpartisan lobbying is allowed. **So HCB's published rules don't exclude this
  project.** But the founder's broader wording means you should still get the answer in
  writing. Email hcb@hackclub.com and ask about (1) asking state lawmakers to pass
  bills, (2) commenting to utility commissions, (3) teams in other states, and (4) who owns the
  name and website if you leave. If HCB says no to (1), use the backup below.
- Under 18: **a parent or guardian must co-sign HCB's fiscal sponsorship agreement**
  (https://intercom.help/hcb-v2/en/articles/15409924-what-is-the-fiscal-sponsorship-agreement).
- **Backup if HCB declines:** Social Good Fund, which publishes rates and takes community and
  environmental projects. Ask it the same four questions. The other option is incorporating
  (2.3) and making the 501(h) election, which lets you lobby on your own terms.
- Other sponsors: Social Good Fund (8%, or 6.5% under its more hands-off model, plus $29 a
  month), and Fractured Atlas (8% plus membership, aimed at arts projects, so a weak fit).
  **Open Collective Foundation shut down in 2024, so don't use it** (from the Codex report;
  sources are in the appendix).
- Codex also recommended *against* incorporating now. That fits your decision: under option A
  this is still a nonprofit. Incorporating (B) is the later step, not a different project.

### 2.2 Under 18: what you can and can't do

- **Can you be a director? The law doesn't say no, but it's murky.** California's nonprofit code
  requires directors to be "natural persons" and sets **no minimum age** (§§5047, 5120, 5213).
  The Digital Media Law Project's California guide says directors don't have to "be of a
  certain age" (https://www.dmlp.org/legal-guide/california/forming-nonprofit-corporation-california).
  Against that: the Civil Code says minors aren't capable of contracting (§1556), so whether a
  minor's director duties are binding is unclear. No court or state ruling on minor directors
  was found. Bylaws may set their own qualifications.
- **This doesn't block anything.** Under option A (fiscal sponsorship) there's no board for you
  to sit on. If you incorporate later, the setup below (adults as directors, you as founder or
  executive director, students on an advisory council) avoids the question completely. Only
  pay a lawyer to settle it if you specifically want a voting board seat before you turn 18.
- Minors in California can sign contracts but can generally cancel them later (Family Code
  §6710). That's why an **adult signs contracts and controls the bank account.**
- Recommended setup: **you lead as a student founder or executive director, and adults handle
  money, signatures and compliance.** If you incorporate later, put at least three adults on the
  board, with students on an advisory council.
- **Youth safety: California's AB 506 (Business and Professions Code §18975, in force since
  2022). Read from the enacted text** (Chapter 169, Statutes of 2021; a copy is posted by the Los
  Angeles city youth department:
  https://ydd.lacity.gov/sites/g/files/wph2236/files/2025-02/californiastateassemblybill506.pdf).
  Administrators, employees and "regular volunteers" of a "youth service organization" must:
  - complete training in spotting and reporting child abuse (a) (the state's free online
    mandated-reporter course counts);
  - undergo a background check under Penal Code §11105.3 (b), which in practice is a Live Scan
    fingerprint check;
  - follow written policies for reporting suspected abuse to people *outside* the
    organization (c)(1);
  - follow a policy requiring, "to the greatest extent possible, the presence of at least two
    mandated reporters whenever administrators, employees, or volunteers are in contact with, or
    supervising, children" (c)(2).

  Definitions, from (e):
  - **"Regular volunteer":** 18 or older, with direct contact with or supervision of children
    for more than 16 hours a month or 32 hours a year.
  - **"Youth service organization":** one that "employs or utilizes the services of persons
    who... are mandated reporters pursuant to paragraph (7) of subdivision (a) of Section
    11165.7 of the Penal Code." That paragraph covers staff of youth organizations. (Secondary
    summaries describe this as a "primary purpose" test. The statute itself works through that
    mandated-reporter cross-reference.)
  - **What this means here:** whether a student advocacy project counts depends on whether its
    adults count as youth-organization mandated reporters. That's a legal call, so ask the
    sponsor. **The practical answer doesn't change. Comply from day one:** the training is
    free, the background check is one-time, and two adults at any in-person chapter event with
    minors meets (c)(2). Insurers are allowed to ask for proof (d). In other states, follow that
    state's rules.
  - Chapter rules in every state: parental consent, an adult present at in-person events, no
    one-on-one private messages between adults and minors, permission before photos, and a
    reporting contact.

### 2.3 If you incorporate later (California)

1. Articles of Incorporation, form ARTS-PB-501(c)(3). **$30** (Secretary of State, verified).
2. Bylaws. California requires a president or chair, a secretary and a treasurer, and the
   secretary or treasurer can't also be president (Corporations Code §5213).
3. EIN, the federal tax ID number. Free from the IRS.
4. Statement of Information SI-100 within **90 days**, then every 2 years. **$20**.
5. Register with the California Attorney General (form CT-1) within **30 days of receiving any
   money**. **$50** (verified).
6. IRS Form 1023-EZ (**$275**) or Form 1023 (**$600**). The EZ version only works if yearly
   income stays at or under $50,000.
7. California tax exemption, Form 3500A, after the IRS approves.
8. Every year: IRS 990-N, California 199N, and the Attorney General's RRF-1 ($25 under $50,000).
   **Miss three years of IRS filings and the exemption is revoked automatically.**

### 2.4 Lobbying rules, which matter because advocacy is the core work

- A 501(c)(3) **may lobby**, but lobbying can't be a "substantial part" of what it does. Under
  the 501(h) election (Form 5768), the safe limit is **20% of spending** for organizations
  spending up to $500,000. Only a quarter of that limit can go to "grassroots" lobbying, meaning
  asking the public to contact lawmakers (IRS, verified).
- **Asking a utility commission for a rule is not "legislation" for IRS purposes.** It counts as
  administrative advocacy (IRS lobbying page). The commission route is the freer one.
- What each activity counts as:
  - The state-by-state data site is **education**.
  - "Here's how to contact your legislator", with no bill named, is **education**.
  - "Tell your legislator to pass S.2612" is **grassroots lobbying**.
  - A student meeting a legislator about a specific bill is **direct lobbying**.
- **Under 501(h), unpaid volunteer time generally doesn't count against the limit.** Money spent
  training or equipping volunteers can (Bolder Advocacy, cited in the appendix). Under HCB, the
  limits are HCB's, so follow its rules.
- California registration: an organization must file Form 645 if it spends **$5,000 or more in
  a calendar quarter** to influence legislation or regulators. A student-volunteer project
  should stay far below that.
- **Never support or oppose candidates.** That is banned outright for a 501(c)(3).

### 2.5 Chapters: legal structure

- **Start with chapters as internal teams of the one project**, not separate organizations.
  Money goes through the central HCB account, and chapters get budgets and reimbursements
  against receipts.
- The IRS "group exemption" (Rev. Proc. 2026-8, verified) needs **at least five subordinate
  organizations** and only matters when chapters are separate legal entities. Skip it for now.
- Raising money from people in other states can trigger charity registration in those states.
  Check before any chapter fundraises.
- Name: check for trademark conflicts before choosing a name. Registering a trademark with the
  US Patent and Trademark Office costs **$350 per class**. Hold off until the name is settled.

---

## Part 3. How other groups run chapters

Full detail: `research/chapters-advocacy-marketing.md`.

| Group | How you start one | What the national group gives chapters | How chapters are held accountable |
|---|---|---|---|
| Sunrise Movement | New Hubs program. Student hubs "typically" have at least 5 members at one school; a chapter has 30 or more (verified) | Member portal, style guide. **Strike Circles** gave 6 meeting agendas, videos and a coach; about 600 groups launched and more than 300 kept going | HubHub directory updates |
| March for Our Lives | A signed affiliation agreement | Coaching, training, license to use the name and logo | **1-year term**; national can end it immediately, a chapter can leave with 30 days' notice; positions on bills coordinated with state leaders |
| Students Demand Action | One student fills in a form plus a volunteer agreement, and **parental consent if under 18** | Toolkits, leadership calls, Canva templates, regional organizers | Event registration, recruit check-in forms |
| Girl Up | Club registration; the 2018 guide required 5 core members | Girl Up 101, branding toolkit | **Monthly activity report to stay active** (verified); **adult adviser required** for under-18 clubs (2020 policy) |
| Citizens' Climate Lobby | Group-start workshops and a group leader | Meeting plans, lobbying-notes forms, op-ed and press templates | Action reports covering meetings, media and endorsements |
| RESULTS | Orientation, then joining a group | 90-day conversation guide, group-leader handbook, "laser talk" training | Volunteers report media, lobbying and outreach meetings |
| Zero Hour | Interest form | 7 weekly Zoom trainings | Not found. It's fiscally sponsored, a precedent for option A |

**How well each row is checked:** these were re-checked live on 2026-10-17: Sunrise hub sizes,
Sunrise Strike Circles (6 agendas, videos and a coach; 600 groups; more than 300 kept going),
Girl Up's monthly report, and CPUC's comment steps. **Students Demand Action is confirmed
from its current May 2026 toolkit.** One student submits the start form; the group is recognized
once one member completes the volunteer agreement "and parental consent form, if they are
under 18"; approval comes within a week
(https://studentsdemandaction.org/wp-content/uploads/2026/05/SDA-High-School-Organizing-Toolkit-050826A.pdf).
**March for Our Lives' terms (1-year term, 30-day exit) can't be confirmed.** The posted
agreement link opens only a sign-up form, and no other public copy was found. Treat that row as
an example of what an agreement covers, not as March for Our Lives' current rules. Your own
agreement doesn't depend on theirs.

**Lessons for this project:**
1. **A chapter is a person with a job, not a form submission.** Sunrise found that online
   interest didn't turn into groups until it gave people agendas and a coach. Give every new lead
   a kit: a state brief, a first-meeting agenda, and one real action.
2. **Sign a short agreement.** Cover the mission, how the name may be used, who may speak for
   the project, who owns the social accounts, the code of conduct, and how affiliation ends.
   March for Our Lives' agreement is the model; yours should fit on one page.
3. **Require a monthly check-in, as Girl Up does.** A chapter that misses it is listed as
   inactive. That keeps the "N chapters" count honest.
4. **Require an adult adviser and parental consent** for under-18 chapters, as Girl Up and SDA
   do.
5. **Plan for graduation.** Each chapter needs a named successor and shared records. SDA and
   Moms Demand Action both had to restart groups that went dormant.
6. **Failure modes to plan for:** online interest that never becomes a team; a local chapter
   statement that embarrasses the national group (Sunrise DC, 2021); chapters going dormant.

---

## Part 4. How advocacy actually works

### 4.1 What moves lawmakers

Congressional Management Foundation surveys asked **Congressional staff** how much each kind of
contact would influence an undecided member of Congress (2015 survey, "some" or "a lot" of
influence):

| Method | Influence |
|---|---:|
| In-person visit from constituents | **94%** |
| Individualized email | **92%** |
| Individualized letter | **88%** |
| Local editorial on the issue | **87%** |
| Phone call | **84%** |
| Letter to the editor naming the lawmaker | **84%** |
| **Form (copy-paste) email** | **56%** |

(The 94% and 92% figures were independently verified; the full table is in CMF's
"Citizen-Centric Advocacy", linked in the appendix.)
**Careful:** these are about *Congress*, not state legislators. Use them as a guide, not as a
measurement of state lawmakers. **The design lesson for the site: don't build a one-click form
email.** Help people write a personal message and request a meeting with their own legislator.

### 4.2 The four channels, in the order the guide should teach them

1. **The state utility commission** (often the fastest route). Arizona's commission wrote
   emergency rules within a week in June 2019, and California's and New York's protections both
   came through commission proceedings. The public can comment online:
   - California (CPUC): search the docket card by proceeding number, then Public Comments, then
     Add Public Comment. **Your name and city are published unless you choose the private
     option.** Tell students this first.
   - New York (PSC): find the case in its document system, then Post Comments.
   - Also: public participation hearings, where you sign up to speak with no RSVP needed (CPUC).
   - Know the rules on private contact with commissioners. In California, "ex parte"
     communications are banned in some proceeding types, so don't lobby commissioners privately
     by default.
2. **State legislators.** Ask for a meeting as a constituent and bring a one-page state brief
   with one specific ask. Then follow up: record what they said, what they promised, and the
   next date. Washington State's guide to testifying at hearings is the clearest example: anyone
   may testify, sign-up closes an hour before the hearing, and written testimony is accepted up
   to 24 hours after it starts.
3. **Hearings on a live bill** (Massachusetts S.2612, Vermont H.88, Florida's PAUSE Act). Use
   written testimony or register a position.
4. **The media.** Letters to the editor and op-eds, then send what gets published to the
   legislator's office (RESULTS' practice).

### 4.3 Scripts to adapt

- **RESULTS "EPIC" talk, under 2 minutes.** **E**ngage with a hook, state the **P**roblem,
  **I**nform them of the solution, and end with a specific **C**all to action.
  > I'm a student in [city]. My state has no rule that stops power shut-offs in extreme heat,
  > and our state saw [N, from `result.md`] heat-alert days a year from 2015 to 2024. Other
  > states fixed this; California's 2026 change cut unprotected alert days from 4.0 to 1.1 a
  > year. Will you [co-sponsor X / ask the commission to open a rulemaking]? When should I
  > follow up?
- **Citizens' Climate Lobby meeting roles:** a leader, an asker, a note-taker, a timekeeper,
  and someone who sends the follow-up. Two or three students can split these.
- **Storytelling:** SDA's "Story of Self, Story of Us, Story of Now". Never imply a shut-off
  happened to you if it didn't.

### 4.4 Can minors do this?

Yes. Students have free-speech rights (Tinker v. Des Moines), anyone may petition government,
and Washington explicitly welcomes testimony from anyone. Lobbyist registration in California
applies to *paid* lobbyists, or to organizations spending $5,000 or more a quarter. Students
volunteering their time aren't affected.

---

## Part 5. Marketing and growth

From the Codex report, with sources in the appendix:
- **Platforms the youth groups use:** Instagram and TikTok first (SDA's 2026 Creator Program and
  its high-school toolkit). March for Our Lives is on everything, but no source shows which
  platform works best. **Start with one platform and do it well.**
- **Content that fits this project:** a 30-second state explainer ("Can your power be cut off in
  a heat wave in [state]? Here's the rule."), a screen-recording of filing a commission comment,
  behind-the-scenes clips from a legislator meeting, and the map.
- **Timing:** post state pages when the weather service issues heat alerts. That's when local
  reporters are writing heat stories. (This is a suggestion, not a sourced finding.)
- **Earned media:** pitch local reporters a researched story ("Your state is one of 24 with no
  rule"). Each state page is effectively a press kit.
- **Partners:** state consumer advocates, legal aid, public-health researchers, and the groups
  in 1.8. Those groups have the expertise and you supply the student volunteers. **Ask the Energy
  Justice Lab or NCLC to review `rules.csv`.** That was already condition 2 in the README.
- **What to track, counted separately:** active volunteers, chapter leaders, subscribers,
  personal contacts sent, meetings held, comments filed, media pieces, official responses, and
  rules changed. Never mix "signed up" with "active."

---

## Part 6. Plan: the first 90 days

| When | Do | Done when |
|---|---|---|
| Weeks 1–2 | Re-read all 25 rules and sign off `rules.csv` (README condition 1). Email the Energy Justice Lab and NCLC for review. Recruit an adult adviser. | Rules signed off; review emails sent; adviser named |
| Weeks 1–2 | Email HCB the three questions in 2.1 | Written answer from HCB |
| Weeks 3–4 | Confirm the last 8 no-rule states (README condition 3). Update Massachusetts if H5175 passed. | 24 no-rule states checked |
| Weeks 3–6 | Deploy the website: map, state pages and a corrections contact. Add a "Take action" page for 3 pilot states. | Live URL |
| Weeks 5–8 | Pilot states: **Massachusetts** (bill in conference now), **Pennsylvania** (a summer ban was in the House version; 85,582 summer shut-offs), **Florida** (bill died in 2025; 524,907 summer shut-offs, the most of any no-rule state; 20.2 high-heat-index days a year). Find one student lead in each, through school clubs and Citizens' Climate Lobby or Sunrise contacts. | 3 named leads with signed agreements |
| Weeks 6–10 | Each pilot lead does one real action: a meeting request, a written testimony or a commission comment | Action logged |
| Week 12 | Review: what worked, then decide whether to open sign-ups for chapters | Written review |

Pilot picks are recommendations from the data plus the live bills. Kansas has the most alert
days of any no-rule state (14.2), but no live bill was found there, so it's a later target.

## Part 7. Open items (re-checked 2026-10-17)

**Resolved in this pass:**
- The EIA summer pattern: read from EIA's own PDF. July was the lowest month nationally, and the
  state-by-state picture is in 1.1, from `eia_check.py`. **This corrected an earlier framing.**
- The PUDDLE Act: no 119th-Congress version found. S. 1214 is the related live federal bill.
- Massachusetts: the Senate version has the heat provision (85°F for three days); the bill is in
  conference with no final bill as of mid-October.
- Vermont H.88: stuck in House committee since 2025-01-24. Florida PAUSE Act: died 2025-06-16.
- HCB: a parent must co-sign. The founder's March 2025 "no political activity" statement is a
  warning sign (2.1).

- HCB's published eligibility rules exclude only "political campaigns", not lobbying (2.1).
- Minor directors: no age bar in the code, and the recommended setup avoids the question (2.2).
- AB 506 / §18975: read from the enacted statute text, including the two-adults policy and
  the volunteer threshold. Plan: comply from day one (2.2).
- Pennsylvania: renewal bills SB 154 and HB 2333 each passed one chamber; no summer ban in
  either summary (1.6).
- Students Demand Action: confirmed from its May 2026 toolkit (Part 3).

**Nothing blocks starting. Two things to do, plus two to watch:**
1. **Email hcb@hackclub.com** and get written confirmation that nonpartisan lobbying for state
   bills is fine. It's a step in week 1–2 of the plan, not a blocker: the published rules already
   allow it.
2. **Watch two bills:** Massachusetts H5175 (conference) and Pennsylvania SB 154 / HB 2333. Both
   change which states have a rule, and so what `rules.csv` and the state pages should say.
3. March for Our Lives' exact agreement terms: unconfirmable from public sources, and not needed.
   Your own one-page agreement is in Part 3.
