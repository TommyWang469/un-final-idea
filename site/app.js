const $ = id => document.getElementById(id);
const esc = t => String(t).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const list = a => a.length < 2 ? a.join("") : a.slice(0, -1).join(", ") + " and " + a[a.length - 1];
const still = matchMedia("(prefers-reduced-motion:reduce)").matches;
// for an ordinary household: a rule that covers only some customers leaves every alert day uncovered
const open = s => s.covers === "all" ? s.alert_open : s.alert;
const kind = s => s.covers === "none" ? "dark" : s.covers === "all" && open(s) <= 0.1 * s.alert ? "lit" : "gap";
const none = STATES.filter(s => s.covers === "none");
const byAbbr = Object.fromEntries(STATES.map(s => [s.abbr, s]));

if ($("n-none")) $("n-none").textContent = none.length;

// highlighter marks draw once when they scroll into view
if ("IntersectionObserver" in window) {
  const mo = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add("in"); mo.unobserve(e.target); } }), {threshold:.8});
  document.querySelectorAll(".mark").forEach(m => mo.observe(m));
} else document.querySelectorAll(".mark").forEach(m => m.classList.add("in"));

// live fights and recent changes, as of October 2026 (sources: nonprofit-playbook.md 1.6)
const NEWS = {
  MA: `<b>A bill is in play.</b> The Senate's version (S.3143, passed July 2026) would stop shut-offs for households in financial hardship when it is expected to pass 85°F three days in a row, May 15 to September 15. The final bill (H5175) was still with a conference committee in mid-October 2026. <a href="https://malegislature.gov/Bills/194/H5175" rel="noopener">Bill page</a>`,
  PA: `<b>An opening.</b> The state's utility-customer law (Chapter 14) lapsed at the end of 2024 and is being renewed. A 2024 House version added a summer shut-off ban. Neither current renewal bill (SB 154, HB 2333) includes one in its summary, so a ban could still be pushed as an amendment. <a href="https://www.spotlightpa.org/news/2024/12/pennsylvania-winter-utility-shutoff-consumer-protection-law-reauthorization/" rel="noopener">Spotlight PA</a>`,
  FL: `<b>A bill died.</b> The PAUSE Act (H 419 / SB 330) died in committee on June 16, 2025. <a href="https://www.flhouse.gov/Sections/Bills/billsdetail.aspx?BillId=80992" rel="noopener">Bill page</a>`,
  VT: `<b>A bill is stuck.</b> H.88 would stop shut-offs at 92°F or hotter. It has sat in a House committee since January 2025. <a href="https://legislature.vermont.gov/bill/status/2026/H.88" rel="noopener">Bill page</a>`,
  CA: `<b>Changed in July 2026.</b> The utility commission lowered the trigger from 100°F to 90°F. On the same weather, uncovered alert days fall from 4.0 to 1.1 a year. The 2024 shut-off count above was under the old rule.`,
  IL: `<b>Changed in 2023.</b> A law lowered the trigger from 95°F to 90°F and added weather-service alerts. On the same weather, uncovered alert days fall from 0.9 to 0.0 a year.`,
  NY: `<b>New in March 2026.</b> The state utility commission adopted this rule. It did not exist in 2024, when the shut-off count above was taken.`,
};
if ($("stage")) initCheck();
if ($("rank")) initFindings();

function initCheck() {
  const GRID = {ME:[0,11],VT:[1,10],NH:[1,11],WA:[2,1],ID:[2,2],MT:[2,3],ND:[2,4],MN:[2,5],IL:[2,6],WI:[2,7],MI:[2,8],NY:[2,9],MA:[2,10],RI:[2,11],
    OR:[3,1],NV:[3,2],WY:[3,3],SD:[3,4],IA:[3,5],IN:[3,6],OH:[3,7],PA:[3,8],NJ:[3,9],CT:[3,10],
    CA:[4,1],UT:[4,2],CO:[4,3],NE:[4,4],MO:[4,5],KY:[4,6],WV:[4,7],VA:[4,8],MD:[4,9],DE:[4,10],
    AZ:[5,2],NM:[5,3],KS:[5,4],AR:[5,5],TN:[5,6],NC:[5,7],SC:[5,8],DC:[5,9],
    OK:[6,4],LA:[6,5],MS:[6,6],AL:[6,7],GA:[6,8],TX:[7,4],FL:[7,9]};
  const NUDGE = {FL:[24,20], LA:[-10,-8], MI:[16,22]};   // these centroids fall on a coast or in a lake
  const NOLABEL = new Set(["VT","NH","MA","RI","CT","NJ","DE","MD","DC"]);
  const OUTSIDE = {AK:"Alaska", HI:"Hawaii", PR:"Puerto Rico"};
  const label = s => `${esc(s.state)}: ${esc(s.rule)}, ${open(s).toFixed(1)} uncovered alert days a year`;
  const stAttrs = s => `class="st ${kind(s)}" data-s="${s.abbr}" role="button" tabindex="0" aria-pressed="false" aria-label="${label(s)}"`;

  // real map; DC is too small to click, so it gets a dot
  $("mapView").innerHTML = `<svg viewBox="0 0 975 610" role="group" aria-label="Map of states. Choose a state to see its rule.">
    ${STATES.map(s => s.abbr === "DC"
      ? `<circle cx="${SHAPES.DC.x}" cy="${SHAPES.DC.y}" r="7" ${stAttrs(s)}/>`
      : `<path d="${SHAPES[s.abbr].d}" ${stAttrs(s)}/>`).join("")}
    ${STATES.filter(s => !NOLABEL.has(s.abbr)).map(s => `<text class="lab ${kind(s) === "dark" ? "" : "onlight"}" x="${SHAPES[s.abbr].x + (NUDGE[s.abbr] || [0, 0])[0]}" y="${SHAPES[s.abbr].y + (NUDGE[s.abbr] || [0, 0])[1]}">${s.abbr}</text>`).join("")}
  </svg>`;
  $("winView").innerHTML = STATES.map(s => {
    const [r, c] = GRID[s.abbr];
    return `<button class="win ${kind(s)}" style="grid-row:${r + 1};grid-column:${c + 1}" data-s="${s.abbr}" aria-pressed="false" aria-label="${label(s)}">${s.abbr}<small>${open(s).toFixed(0)}</small></button>`;
  }).join("");
  $("states").innerHTML = STATES.map(s => `<option value="${esc(s.state)}">`).join("");

  // the one load moment: every state lit, then a blackout rolls west to east
  const stage = $("stage");
  if (still) stage.classList.remove("pre");
  else {
    const fall = STATES.filter(s => kind(s) !== "lit").sort((a, b) => SHAPES[a.abbr].x - SHAPES[b.abbr].x);
    fall.forEach((s, i) => setTimeout(() => {
      stage.querySelector(`.st[data-s="${s.abbr}"]`).classList.add("off", "cut");
      const t = [...stage.querySelectorAll(".lab")].find(l => l.textContent === s.abbr);
      if (t) t.classList.add("off");
    }, 600 + i * 75));
    setTimeout(() => stage.classList.remove("pre"), 600 + fall.length * 75 + 600);
  }

  // Map or Windows view
  document.querySelectorAll(".views button").forEach(b => b.addEventListener("click", () => {
    const map = b.dataset.view === "map";
    $("mapView").hidden = !map; $("winView").hidden = map;
    document.querySelectorAll(".views button").forEach(x => x.setAttribute("aria-pressed", x === b));
  }));

  // hover label
  const tip = $("tip");
  $("mapView").addEventListener("pointermove", e => {
    const t = e.target.closest("[data-s]");
    tip.hidden = !t || e.pointerType === "touch";
    if (t) { const s = byAbbr[t.dataset.s]; tip.textContent = `${s.state}: ${open(s).toFixed(1)} uncovered days`; tip.style.left = Math.min(e.clientX + 14, innerWidth - 250) + "px"; tip.style.top = e.clientY + 14 + "px"; }
  });
  $("mapView").addEventListener("pointerleave", () => tip.hidden = true);

  // search: state name, abbreviation or ZIP
  function find(raw) {
    const q = raw.trim().toLowerCase();
    if (!q) return {msg: "Enter a state name or a 5-digit ZIP code."};
    if (/^\d+$/.test(q)) {
      if (q.length !== 5) return {msg: "A ZIP code has 5 digits."};
      const a = ZIPX[q] || ZIP3[q.slice(0, 3)];
      if (!a) return {msg: `ZIP ${q} is not in the Census list. Try your state name.`};
      if (OUTSIDE[a]) return {msg: `ZIP ${q} is in ${OUTSIDE[a]}, which this check does not cover.`};
      return {abbr: a, msg: `ZIP ${q} is in ${a === "DC" ? "the " : ""}${byAbbr[a].state}. ZIP areas can cross state lines; search by name if this looks wrong.`};
    }
    const hit = STATES.filter(s => s.state.toLowerCase() === q || s.abbr.toLowerCase() === q);
    const near = hit.length ? hit : STATES.filter(s => s.state.toLowerCase().startsWith(q));
    if (near.length === 1) return {abbr: near[0].abbr, msg: ""};
    if (near.length > 1) return {msg: `Did you mean ${list(near.map(s => s.state))}?`};
    if (/^(alaska|ak|hawaii|hi|puerto rico|pr)$/.test(q)) return {msg: "This check covers 48 states and DC, not Alaska, Hawaii or Puerto Rico."};
    return {msg: `No state matches "${raw.trim()}". Enter a state name or a 5-digit ZIP code.`};
  }
  $("find").addEventListener("submit", e => {
    e.preventDefault();
    const r = find($("q").value);
    $("msg").textContent = r.msg;
    if (r.abbr) detail(r.abbr); else $("detail").hidden = true;
  });
  $("q").addEventListener("input", e => { if (STATES.some(s => s.state === e.target.value)) $("find").requestSubmit(); });

  let selected = null;
  function detail(abbr, focus) {
    selected = abbr;
    const s = byAbbr[abbr], d = $("detail"), o = open(s);
    d.className = kind(s);
    d.hidden = false;
    d.style.animation = "none"; d.offsetWidth; d.style.animation = "";
    const name = (s.abbr === "DC" ? "the " : "") + esc(s.state);
    const src = {primary: "Read from the state's own legal text.", secondary: "Read from a secondary source, not the legal text itself.", "own code": "No rule: checked against the state's own code.", "own code (one section)": "No rule: one section of the state's shut-off rules was checked.", "regulator page": "No rule: checked against the state regulator's own list of protections.", "news report": "No rule: per a news report."}[s.verified] || "Two separate national lists show no hot-weather rule. Not yet confirmed from the state's own code.";
    const alertRule = /weather-service/.test(s.rule);
    const ask = s.covers === "none"
        ? `<b>Ask for a rule.</b> No state rule stops a utility in ${name} from cutting off power for an unpaid bill on a dangerously hot day. A rule that turns on whenever the weather service issues a heat alert would cover every alert day. Texas, Louisiana and Minnesota already use one.`
      : s.covers === "subset"
        ? `<b>Ask for a rule that covers every household.</b> Today it protects only some people (${esc(s.note.replace(/^Only /, "").toLowerCase())}). Everyone else is unprotected on every alert day.`
      : kind(s) === "gap"
        ? `<b>Ask for a better trigger.</b> The rule misses ${o.toFixed(1)} of ${s.alert.toFixed(1)} alert days a year. Adding weather-service heat alerts as a trigger, as Illinois did in 2023, closes that gap.`
        : `<b>Protect what you have.</b> The rule covers almost every alert day${alertRule ? ", because it turns on with the alert itself" : ""}. Ask lawmakers to keep it, and check that it reaches city-owned utilities and co-ops, which many rules leave out.`;
    const summer = typeof SUMMER !== "undefined" && SUMMER[s.state];
    d.innerHTML = `<h3>${esc(s.state)}</h3>
      <p class="rule">${s.covers === "none" ? "<b>No hot-weather rule.</b>" : `Rule: <b>${esc(s.rule)}</b>`}</p>
      <div class="cols">
        <div>
          <h4>On dangerous days</h4>
          <div class="split" title="${(s.alert - o).toFixed(1)} covered, ${o.toFixed(1)} uncovered"><i class="s" style="width:${s.alert ? 100 * (s.alert - o) / s.alert : 0}%"></i><i class="o" style="width:${s.alert ? 100 * o / s.alert : 0}%"></i></div>
          <p>The weather service warned of dangerous heat on <b>${s.alert.toFixed(1)} days a year</b>. On <b>${o.toFixed(1)}</b> of them, ${s.covers === "subset" ? "most households" : "a household"} had no protection.${s.covers === "none" ? "" : ` The rule is on ${s.on.toFixed(1)} days a year.`}</p>
          ${summer ? `<p>Utilities here cut off home electricity <b>${summer.toLocaleString("en-US")} times</b> from June to August 2024.</p>` : ""}
          ${NEWS[s.abbr] ? `<p>${NEWS[s.abbr]}</p>` : ""}
        </div>
        <div>
          <h4>What to ask for</h4>
          <p>${ask}</p>
          <p>Who decides: your <b>state legislators</b> (<a href="https://openstates.org/find_your_legislator/" rel="noopener">find yours</a>) and your <b>state utility commission</b>.</p>
          <a class="act" href="act.html">How to ask: our step-by-step guide</a>
        </div>
      </div>
      ${!s.quote ? "" : s.covers === "none" ? `<p class="fine" style="margin-top:18px">What we found in the state's rules: ${esc(s.quote)}</p>` : `<blockquote>${esc(s.quote)}</blockquote>`}
      ${s.covers === "all" && s.note ? `<p class="fine">${esc(s.note)}.</p>` : ""}
      <p class="fine">${src} ${/^https?:/.test(s.source) ? `<a href="${esc(s.source)}" rel="noopener">Source</a>.` : ""} Rules as of October 2026. Shut-off count: <a href="https://www.eia.gov/analysis/requests/residential/utility/" rel="noopener">US Energy Information Administration</a>.</p>`;
    document.querySelectorAll(".st, .win").forEach(w => w.setAttribute("aria-pressed", w.dataset.s === abbr));
    history.replaceState(null, "", "#" + abbr);
    render();
    const row = document.querySelector(`#rows tr[data-s="${abbr}"]`); if (row) row.classList.add("arrive");
    if (focus) d.focus(); else d.scrollIntoView({block:"nearest"});
  }

  const triggers = s => { const r = s.rule, t = [];
    if (/weather-service/.test(r)) t.push("alert");
    if (/heat index/.test(r)) t.push("index");
    if (/\d+°F/.test(r.replace(/heat index( at or)?( above)? \d+°F/g, ""))) t.push("temp");
    return t; };
  function render() {
    const key = $("sort").value, show = $("show").value, trig = $("trig").value, text = $("tfind").value.trim().toLowerCase();
    const top = Math.max(...STATES.map(x => x.alert));
    const val = s => key === "alert_open" ? open(s) : s[key];
    const shown = STATES.filter(s => (show === "all" || (show === "none" ? s.covers === "none" : show === "lit" ? kind(s) === "lit" : show === "subset" ? s.covers === "subset" : s.covers === "all" && kind(s) === "gap"))
        && (trig === "all" || triggers(s).includes(trig))
        && (!text || s.state.toLowerCase().includes(text) || s.rule.toLowerCase().includes(text)))
      .sort((a, b) => key === "state" ? a.state.localeCompare(b.state) : val(b) - val(a));
    $("count").innerHTML = shown.length ? `Showing ${shown.length} of ${STATES.length}` : `No states match these filters. <button class="link-btn" id="clear" type="button">Clear filters</button>`;
    $("rows").innerHTML = shown.map(s => {
      const o = open(s), w = 100 * s.alert / top;
      return `<tr class="${s.abbr === selected ? "sel" : ""}" data-s="${s.abbr}" tabindex="0">
        <td>${esc(s.state)}</td><td>${esc(s.rule)}${s.covers === "subset" ? ' <span class="tag">some customers only</span>' : ""}${s.verified === "secondary" ? ' <span class="tag">secondary source</span>' : ""}</td>
        <td>${s.covers === "none" ? "–" : s.on.toFixed(1)}</td><td>${s.alert.toFixed(1)}</td>
        <td><b>${o.toFixed(1)}</b><div class="bar" style="width:${w.toFixed(0)}px" title="${(s.alert - o).toFixed(1)} covered, ${o.toFixed(1)} uncovered"><div class="s" style="width:${s.alert ? 100 * (s.alert - o) / s.alert : 0}%"></div><div class="o" style="width:${s.alert ? 100 * o / s.alert : 0}%"></div></div></td>
        <td>${s.hot95.toFixed(1)}</td></tr>`;
    }).join("");
  }
  document.addEventListener("click", e => {
    if (e.target.id === "clear") { $("show").value = "all"; $("trig").value = "all"; $("tfind").value = ""; render(); return; }
    const t = e.target.closest("[data-s]");
    if (t) { $("msg").textContent = ""; detail(t.dataset.s, t.tagName === "TR"); }
  });
  document.addEventListener("keydown", e => {
    const t = e.target.closest && e.target.closest("[data-s]");
    if (t && (e.key === "Enter" || (e.key === " " && t.tagName !== "BUTTON"))) { e.preventDefault(); detail(t.dataset.s, t.tagName === "TR"); }
  });
  ["sort", "show", "trig"].forEach(id => $(id).addEventListener("change", render));
  $("tfind").addEventListener("input", render);
  render();
  const open1 = () => { const a = location.hash.slice(1).toUpperCase(); if (byAbbr[a]) detail(a); };
  addEventListener("hashchange", open1);
  open1();
}

function initFindings() {
  const worst = [...none].sort((a, b) => b.alert - a.alert).slice(0, 3);
  const subset = STATES.filter(s => s.covers === "subset");
  $("fix-none").textContent = `${none.length} states have no rule. The most heat-alert days among them fall in ${list(worst.map(s => `${s.state} (${s.alert.toFixed(1)} a year)`))}.`;
  $("fix-subset").textContent = `${list(subset.map(s => s.state))} protect only some customers, such as older or disabled residents or those on energy assistance. Everyone else is uncovered on every alert day.`;

  const top = [...STATES].sort((a, b) => open(b) - open(a)).slice(0, 15), max = open(top[0]);
  $("rank").innerHTML = top.map(s => {
    const o = open(s);
    return `<div class="row"><a href="index.html#${s.abbr}">${esc(s.state)}</a><div class="track" style="--w:${100 * o / max}%;width:var(--w)"><i class="o" style="width:100%"></i></div><span class="val">${o.toFixed(1)}</span></div>`;
  }).join("");

  // bars grow once, when scrolled into view
  const charts = document.querySelectorAll(".chart");
  if (!still && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }), {threshold:.2});
    charts.forEach(c => { c.classList.add("anim"); c.querySelectorAll(".track").forEach(t => t.style.removeProperty("width")); io.observe(c); });
  }
}
