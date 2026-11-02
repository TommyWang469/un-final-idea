// To add someone, copy a block and change it. Keep the commas.
// photo is optional: put a 3:4 image in this folder and give its filename. Without one, the card shows initials.
const TEAM = [
  {
    name: "Zhaitong (Tommy) Wang",
    role: "President",
    photo: "tommy-wang.jpg",
    bio: "Zhaitong (Tommy) Wang is a high school junior in California. He leads this project's work testing whether state shut-off rules protect people on the days the heat is dangerous. He also leads the wiki and design subteam of Theranova, an iGEM synthetic biology team. He has written a research paper on what predicts the severity of cryptocurrency crashes and released his own video game, Threefold Arsenal. Outside of class, he runs hurdles on his school's track and field team.",
  },
];

document.getElementById("team").innerHTML = TEAM.map(p => {
  const esc = t => String(t).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
  const initials = p.name.split(/\s+/).map(w => w[0]).slice(0, 2).join("");
  const face = p.photo ? `<img class="face" src="${esc(p.photo)}" alt="${esc(p.name)}">` : `<span class="face" aria-hidden="true">${esc(initials)}</span>`;
  return `<li>${face}<div><h3>${esc(p.name)}</h3><p class="role">${esc(p.role)}</p>${p.bio ? `<p>${esc(p.bio)}</p>` : ""}</div></li>`;
}).join("");
