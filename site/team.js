// To add someone, copy a line and change it. Keep the commas. bio is optional.
const TEAM = [
  {name: "Tommy Wang", role: "President", bio: ""},
];

document.getElementById("team").innerHTML = TEAM.map(p => {
  const esc = t => String(t).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
  const initials = p.name.split(/\s+/).map(w => w[0]).slice(0, 2).join("");
  return `<li><span class="face" aria-hidden="true">${esc(initials)}</span><div><h3>${esc(p.name)}</h3><p class="role">${esc(p.role)}</p>${p.bio ? `<p>${esc(p.bio)}</p>` : ""}</div></li>`;
}).join("");
