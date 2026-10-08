// Build the Thai art & architecture knowledge site into dist/ (npm run build).
// Human pages: dist/* · AI: dist/llms.txt, dist/llms-full.txt, dist/md/*.md, dist/knowledge.json, dist/glossary.json
// Published images: images/photos (freely licensed Wikimedia Commons photos, credited automatically from
// images/photos/manifest.json) and images/renders (our own model renders, case study only). Photos without a free
// licence (images/reference, images/annotated) are replaced by their caption.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { marked } from "marked";
import { PAGES, GROUPS } from "./pages.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const DIST = path.join(ROOT, "dist");
const SITE = process.env.SITE_URL || "https://thai-art-knowledge.pages.dev";
const TITLE = "ความรู้ลายไทย ศิลปะไทย และสถาปัตยกรรมไทย";
const TITLE_EN = "Thai Art, Lai Thai & Thai Architecture Knowledge Base";
const PUBLIC_IMG = ["images/photos/", "images/renders/"];
const PHOTOS = JSON.parse(fs.readFileSync(path.join(ROOT, "images/photos/manifest.json"), "utf8"));
const credit = (name, md) => {
  const m = PHOTOS[name];
  if (!m) return "";
  const who = (m.author || "ไม่ระบุ").replace(/\s+/g, " ").slice(0, 80);
  return md ? `

*ภาพ: ${who} · ${m.license} · ${m.source}*`
            : `

<sub>ภาพ: ${who} · <a href="${m.license_url || m.source}">${m.license}</a> · <a href="${m.source}">Wikimedia Commons</a></sub>`;
};
const today = new Date().toISOString().slice(0, 10);

fs.rmSync(DIST, { recursive: true, force: true });
fs.mkdirSync(path.join(DIST, "md"), { recursive: true });
for (const dir of PUBLIC_IMG) fs.cpSync(path.join(ROOT, dir), path.join(DIST, dir), { recursive: true });

const bySource = Object.fromEntries(PAGES.map((p) => [p.file, p]));
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

/** Clean a source Markdown file for publication. mode "html" links to  pages, "md" to /md/*.md. */
function clean(src, mode) {
  let s = src;
  // third-party photos -> caption only
  s = s.replace(/!\[([^\]]*)\]\((images\/(?:reference|annotated)\/[^)]+)\)/g, (_, alt) =>
    `*[ภาพอ้างอิงจากแหล่งภายนอก ไม่เผยแพร่บนเว็บ: ${alt || "ภาพถ่าย"}]*`);
  // published images -> absolute paths; Commons photos get their credit line
  s = s.replace(/(!\[[^\]]*\])\((images\/photos\/([^)]+)\.jpg)\)/g, (_, a, p, name) =>
    `${a}(${mode === "md" ? SITE : ""}/${p})${credit(name, mode === "md")}`);
  s = s.replace(/\]\((images\/renders\/[^)]+)\)/g, (_, p) => `](${mode === "md" ? SITE : ""}/${p})`);
  // links to other pages
  s = s.replace(/\]\(([^)#\s]+\.md)(#[^)]*)?\)/g, (m, f, h) => {
    const p = bySource[decodeURIComponent(f)];
    if (!p) return m;
    return mode === "md" ? `](${SITE}/md/${p.slug}.md${h || ""})` : `](/${p.slug}${h || ""})`;
  });
  s = s.replace(/`images\/(?:reference|annotated)\/[^`]*`/g, "(คลังภาพภายใน ไม่เผยแพร่)");
  // local research/ paths are not published
  s = s.replace(/`research\/[^`]+`/g, "(ข้อความต้นฉบับเก็บในคลังภายใน)");
  return s;
}

const pages = PAGES.map((p, i) => {
  const src = fs.readFileSync(path.join(ROOT, p.file), "utf8");
  const title = (src.match(/^#\s+(.+)$/m) || [, p.file])[1].trim();
  const headings = [...src.matchAll(/^##+\s+(.+)$/gm)].map((m) => m[1].trim());
  const images = [...src.matchAll(/!\[([^\]]*)\]\((images\/(?:photos|renders)\/([^)]+?)(?:\.jpg)?)\)/g)].map((m) => {
    const ph = PHOTOS[m[3]];
    return ph ? { url: `${SITE}/${m[2]}`, caption: ph.caption, author: ph.author, license: ph.license, source: ph.source }
              : { url: `${SITE}/${m[2]}`, caption: m[1], note: "model render (not a reference)" };
  });
  return { ...p, i, title, headings, images, md: clean(src, "md"), htmlMd: clean(src, "html") };
});

// ---------------------------------------------------------------- layout
const CSS = `
:root{--bg:#fbf8f2;--panel:#ffffff;--ink:#2a2118;--muted:#6b5f52;--line:#e6dccb;--accent:#a8321f;--gold:#b8860b;--code:#f3ece0}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#17130f;--panel:#201a14;--ink:#efe6d8;--muted:#b4a692;--line:#3a3026;--accent:#e0785f;--gold:#e0b44a;--code:#2a221a}}
:root[data-theme="dark"]{--bg:#17130f;--panel:#201a14;--ink:#efe6d8;--muted:#b4a692;--line:#3a3026;--accent:#e0785f;--gold:#e0b44a;--code:#2a221a}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.75 "Sarabun","Noto Sans Thai",system-ui,sans-serif}
a{color:var(--accent)}header.top{border-bottom:1px solid var(--line);background:var(--panel);position:sticky;top:0;z-index:5}
header.top .in{max-width:1200px;margin:0 auto;padding:10px 16px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}
header.top a.brand{font-weight:700;color:var(--ink);text-decoration:none}header.top nav a{margin-right:12px;font-size:15px}
.wrap{max-width:1200px;margin:0 auto;padding:16px;display:grid;grid-template-columns:270px minmax(0,1fr);gap:28px}
aside{font-size:15px;line-height:1.5}aside h4{margin:18px 0 6px;color:var(--muted);font-size:13px;letter-spacing:.04em;text-transform:uppercase}
aside a{display:block;padding:3px 0;text-decoration:none;color:var(--ink)}aside a.on{color:var(--accent);font-weight:700}
main{min-width:0;overflow-wrap:anywhere}aside{min-width:0;overflow-wrap:anywhere}main img{max-width:100%;height:auto;border:1px solid var(--line);border-radius:6px;background:#fff}
table{border-collapse:collapse;width:100%;display:block;overflow-x:auto;font-size:15px}th,td{border:1px solid var(--line);padding:6px 9px;vertical-align:top}
th{background:var(--code)}blockquote{margin:12px 0;padding:8px 14px;border-left:4px solid var(--gold);background:var(--code)}
code{background:var(--code);padding:1px 5px;border-radius:4px}h1{line-height:1.3}h2{margin-top:2em;border-bottom:1px solid var(--line);padding-bottom:4px}
.en{color:var(--muted);font-size:15px;margin-top:-10px}.pager{display:flex;justify-content:space-between;gap:12px;margin:40px 0 10px;flex-wrap:wrap}
.hero{padding:28px 0 8px}.hero h1{font-size:34px;margin:0}.hero p{color:var(--muted);max-width:760px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px;text-decoration:none;color:var(--ink);display:block}
.card b{display:block;color:var(--accent)}.card span{font-size:14px;color:var(--muted)}
.gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px}.gallery img{width:100%}
.ai{background:var(--panel);border:1px dashed var(--gold);border-radius:10px;padding:14px}
footer{max-width:1200px;margin:30px auto;padding:16px;color:var(--muted);font-size:14px;border-top:1px solid var(--line)}
@media (max-width:860px){.wrap{grid-template-columns:minmax(0,1fr)}.hero h1{font-size:26px}aside{order:2;border-top:1px solid var(--line)}}
`;

function sidebar(active) {
  let h = "";
  for (const [g, name] of Object.entries(GROUPS)) {
    h += `<h4>${name.th}</h4>`;
    for (const p of pages.filter((q) => q.group === g))
      h += `<a href="/${p.slug}"${p.slug === active ? ' class="on"' : ""}>${esc(p.title.replace(/^\d+\s*/, ""))}</a>`;
  }
  return h;
}

// GitHub Pages serves the site under /<repo>/: prefix every root-relative link (BASE_PATH=/thai-art-knowledge).
const BASE = (process.env.BASE_PATH || "").replace(/\/$/, "");
const withBase = (h) => (BASE ? h.replace(/(href|src)="\/(?!\/)/g, `$1="${BASE}/`) : h);

function layout({ title, desc, body, active = "", canonical = "/" }) {
  return withBase(`<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(title)}</title><meta name="description" content="${esc(desc)}">
<link rel="canonical" href="${SITE}${canonical}"><link rel="alternate" type="text/plain" href="/llms.txt" title="llms.txt">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap" rel="stylesheet">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cpath d='M16 2 L28 28 H4 Z' fill='%23a8321f'/%3E%3C/svg%3E">
<style>${CSS}</style></head><body>
<header class="top"><div class="in"><a class="brand" href="/">${TITLE}</a>
<nav><a href="/lai-thai-catalogue">ลายไทย</a><a href="/roofs">หลังคา</a><a href="/spires">เครื่องยอด</a><a href="/glossary">ศัพท์</a><a href="/for-ai">สำหรับ AI</a></nav></div></header>
<div class="wrap"><aside>${sidebar(active)}</aside><main>${body}</main></div>
<footer>${TITLE_EN} · ปรับปรุง ${today} · เนื้อหาเขียนจากแหล่งอ้างอิงใน <a href="/sources">แหล่งอ้างอิง</a> ข้อที่ยังไม่ยืนยันมีเครื่องหมาย (ควรตรวจ) · ภาพถ่ายของผู้อื่นไม่เผยแพร่ แผนภาพและภาพโมเดลเป็นงานของโครงการนี้</footer>
</body></html>`);
}

// ---------------------------------------------------------------- topic pages
marked.setOptions({ gfm: true });
for (const p of pages) {
  const prev = pages[p.i - 1], next = pages[p.i + 1];
  const body = `<p class="en">${esc(p.en)}</p>${marked.parse(p.htmlMd)}
<div class="pager">${prev ? `<a href="/${prev.slug}">← ${esc(prev.title)}</a>` : "<span></span>"}${next ? `<a href="/${next.slug}">${esc(next.title)} →</a>` : ""}</div>
<p><a href="/md/${p.slug}.md">Markdown ของหน้านี้</a></p>`;
  fs.writeFileSync(path.join(DIST, `${p.slug}.html`), layout({ title: `${p.title} · ${TITLE}`, desc: p.en, body, active: p.slug, canonical: `/${p.slug}` }));
  fs.writeFileSync(path.join(DIST, "md", `${p.slug}.md`),
    `---\ntitle: ${JSON.stringify(p.title)}\ntitle_en: ${JSON.stringify(p.en)}\nurl: ${SITE}/${p.slug}\nupdated: ${today}\n---\n\n${p.md}\n`);
}

// ---------------------------------------------------------------- home
const groupsHtml = Object.entries(GROUPS).map(([g, name]) =>
  `<h2>${name.th} <small class="en">${name.en}</small></h2><div class="cards">` +
  pages.filter((p) => p.group === g).map((p) => `<a class="card" href="/${p.slug}"><b>${esc(p.title)}</b><span>${esc(p.en)}</span></a>`).join("") +
  "</div>").join("");
const photoNames = Object.keys(PHOTOS);
const home = `<section class="hero"><h1>${TITLE}</h1>
<p>คลังความรู้สำหรับคนและ AI: ปรัชญาและคติ ลายไทย จิตรกรรม พระพุทธรูป สัตว์หิมพานต์ และสถาปัตยกรรมไทย ตั้งแต่ฐาน ย่อมุม หลังคาซ้อน–ลด เครื่องลำยอง ไปจนถึงเครื่องยอด ภาพประกอบเป็นภาพถ่ายและภาพร่างจริงจาก Wikimedia Commons ที่ใช้สัญญาอนุญาตเสรี ระบุผู้ถ่ายทุกภาพ และอ้างแหล่งข้อมูลทุกข้อ รวมกฎที่ตรวจแก้จากการทำโมเดลจริง</p>
<p class="en">${TITLE_EN}. Thai-language reference with English page titles, credited real photographs (Wikimedia Commons) and cited sources, built for both people and AI agents.</p></section>
<div class="ai"><b>สำหรับ AI / For AI agents:</b> <a href="/llms.txt">/llms.txt</a> (index) · <a href="/llms-full.txt">/llms-full.txt</a> (all content, one file) · <a href="/knowledge.json">/knowledge.json</a> (structured) · <a href="/glossary.json">/glossary.json</a> · <a href="/md/philosophy.md">/md/*.md</a> per page</div>
<h2>เริ่มที่นี่ <small class="en">Start here</small></h2><div class="cards">
<a class="card" href="/philosophy"><b>ทรงมาก่อนเครื่องประดับ</b><span>ปรัชญา คติ ไตรภูมิ ทรงจอมแห</span></a>
<a class="card" href="/design-rules"><b>กฎการออกแบบ</b><span>Checklist ที่ตรวจแก้จากงานจริง</span></a>
<a class="card" href="/lai-thai-catalogue"><b>พจนานุกรมลายไทย</b><span>4 ตระกูล แม่ลาย 9 แบบ และลายตามชื่อ</span></a></div>
${groupsHtml}
<h2>ภาพอ้างอิง <small class="en">Reference photographs (credited)</small></h2><div class="gallery">${photoNames.map((n) => `<a href="/credits#${n}" title="${esc(PHOTOS[n].caption)}"><img loading="lazy" src="/images/photos/${n}.jpg" alt="${esc(PHOTOS[n].caption)}"></a>`).join("")}</div>
<p><a href="/credits">ที่มาและสัญญาอนุญาตของทุกภาพ</a></p>
<h2>ผลงานโมเดล (ไม่ใช่ภาพอ้างอิง): มณฑปทิศวัดอรุณ ไม้ตัด <small class="en">Our model renders — output, not a reference</small></h2><div class="gallery">
${fs.readdirSync(path.join(ROOT, "images/renders")).sort().map((d) => `<a href="/case-wat-arun-mondop"><img loading="lazy" src="/images/renders/${d}" alt="${d}"></a>`).join("")}</div>`;
fs.writeFileSync(path.join(DIST, "index.html"), layout({ title: TITLE, desc: TITLE_EN, body: home }));

// ---------------------------------------------------------------- for-ai page
const forAi = `<h1>สำหรับ AI และนักพัฒนา</h1><p class="en">How to consume this knowledge base</p>
<ul><li><a href="/llms.txt">/llms.txt</a>: ดัชนีตามมาตรฐาน llms.txt มีลิงก์ Markdown ทุกหน้า</li>
<li><a href="/llms-full.txt">/llms-full.txt</a>: เนื้อหาทั้งหมดในไฟล์เดียว (Markdown)</li>
<li><a href="/knowledge.json">/knowledge.json</a>: JSON array {slug, title, title_en, group, url, markdown_url, headings, images, markdown}</li>
<li><a href="/glossary.json">/glossary.json</a>: อภิธานศัพท์ {term, english, pages}</li>
<li><code>/md/&lt;slug&gt;.md</code>: Markdown รายหน้า มี front matter</li></ul>
<h2>ข้อกำหนดในการใช้</h2><ul><li>รหัส <code>[S#]</code> อ้างถึง <a href="/sources">แหล่งอ้างอิง</a> ข้อความที่มีเครื่องหมาย (ควรตรวจ) หรือ ◇ ยังไม่ได้ยืนยันกับแหล่งหลัก</li>
<li>"กฎที่ผู้ดูแลยืนยัน" มาจากการตรวจแก้โมเดลจริง ให้ใช้เหนือข้อสันนิษฐานทั่วไปและเหนือโมเดลสแกน 3 มิติ</li>
<li>ภาพประกอบเป็นภาพจริงจาก Wikimedia Commons (CC BY / CC BY-SA / PD) มีชื่อผู้ถ่ายและลิงก์ที่มาในทุกภาพ ดู <a href="/credits">/credits</a> และ <a href="/photos.json">/photos.json</a> ภาพโมเดลของเราเป็นผลลัพธ์ ไม่ใช่ภาพอ้างอิง</li>
<li>ภาพถ่ายที่ไม่มีสัญญาอนุญาตเสรีไม่ได้เผยแพร่ เหลือไว้เฉพาะคำบรรยาย</li></ul>`;
fs.writeFileSync(path.join(DIST, "for-ai.html"), layout({ title: `สำหรับ AI · ${TITLE}`, desc: "Machine-readable endpoints", body: forAi, canonical: "/for-ai" }));

// ---------------------------------------------------------------- credits
const creditsHtml = `<h1>ที่มาของภาพ</h1><p class="en">Photo credits — all images from Wikimedia Commons under free licences</p>` +
  photoNames.map((n) => { const m = PHOTOS[n]; return `<div id="${n}" style="display:grid;grid-template-columns:minmax(0,220px) minmax(0,1fr);gap:14px;margin:18px 0">
<img loading="lazy" src="/images/photos/${n}.jpg" alt="${esc(m.caption)}"><div><b>${esc(m.caption)}</b><br>
<small>${esc(m.title)} · ${esc((m.author || "").slice(0, 120))} · <a href="${m.license_url || m.source}">${esc(m.license)}</a> · <a href="${m.source}">หน้าต้นฉบับ</a></small>
${m.description ? `<br><small class="en">${esc(m.description.slice(0, 300))}</small>` : ""}</div></div>`; }).join("");
fs.writeFileSync(path.join(DIST, "credits.html"), layout({ title: `ที่มาของภาพ · ${TITLE}`, desc: "Photo credits", body: creditsHtml, canonical: "/credits" }));
fs.writeFileSync(path.join(DIST, "photos.json"), JSON.stringify(Object.entries(PHOTOS).map(([n, m]) => ({ id: n, url: `${SITE}/images/photos/${n}.jpg`, ...m, file: undefined })), null, 1));

// ---------------------------------------------------------------- llms.txt, llms-full.txt, json
const llms = [`# ${TITLE_EN} (${TITLE})`, "",
  "> Thai-language knowledge base on Thai traditional architecture, Lai Thai ornament, painting, Buddha images, Himmapan creatures and crafts. Each page cites sources as [S#] (see Sources); items marked (ควรตรวจ) or ◇ are unverified. 'กฎที่ผู้ดูแลยืนยัน' are rules verified while building a physical model of Wat Arun's mondop and override general assumptions and 3D-scan models.",
  "", "Key rules: form (ทรง) before ornament; outlines follow the concave chom hae curve; in layered roofs (ซ้อน/ลด) the rear gable is wider and higher at the same pitch with parallel bargeboards; every gable has its own chofa and hang hong; a spire's body starts inside the roof and the ridges run into it; bases follow projecting porches with redented corners.", ""];
for (const [g, name] of Object.entries(GROUPS)) {
  llms.push(`## ${name.en} (${name.th})`, "");
  for (const p of pages.filter((q) => q.group === g)) llms.push(`- [${p.title}](${SITE}/md/${p.slug}.md): ${p.en}`);
  llms.push("");
}
llms.push("## Optional", "", `- [Photo list with captions, authors, licences](${SITE}/photos.json)`, `- [All content in one file](${SITE}/llms-full.txt)`, `- [Structured JSON](${SITE}/knowledge.json)`, `- [Glossary JSON](${SITE}/glossary.json)`, "");
fs.writeFileSync(path.join(DIST, "llms.txt"), llms.join("\n"));
fs.writeFileSync(path.join(DIST, "llms-full.txt"),
  `# ${TITLE_EN}\n# ${TITLE}\nSource: ${SITE} · updated ${today}\n\n` +
  pages.map((p) => `\n\n<!-- page: ${p.slug} | ${p.en} -->\n\n${p.md}`).join("\n\n---\n"));
fs.writeFileSync(path.join(DIST, "knowledge.json"), JSON.stringify({
  title: TITLE, title_en: TITLE_EN, updated: today, site: SITE,
  pages: pages.map((p) => ({ slug: p.slug, title: p.title, title_en: p.en, group: p.group, url: `${SITE}/${p.slug}`,
    markdown_url: `${SITE}/md/${p.slug}.md`, headings: p.headings, images: p.images, markdown: p.md })),
}, null, 1));

// glossary.json from the glossary table
const gl = fs.readFileSync(path.join(ROOT, "อภิธานศัพท์.md"), "utf8").split("\n")
  .filter((l) => /^\|/.test(l) && !/^\|\s*-/.test(l) && !/ศัพท์\s*\|/.test(l))
  .map((l) => l.split("|").slice(1, -1).map((c) => c.trim()))
  .filter((c) => c.length >= 3)
  .map(([term, english, files]) => ({ term, english, pages: files.split(/[,\s]+/).filter(Boolean).map((n) => {
    const p = PAGES.find((q) => q.file.startsWith(n.padStart(2, "0") + "_"));
    return p ? `${SITE}/${p.slug}` : n;
  }) }));
fs.writeFileSync(path.join(DIST, "glossary.json"), JSON.stringify(gl, null, 1));

fs.writeFileSync(path.join(DIST, "robots.txt"), `User-agent: *\nAllow: /\nSitemap: ${SITE}/sitemap.xml\n`);
fs.writeFileSync(path.join(DIST, "sitemap.xml"), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n` +
  ["/", "/for-ai", "/credits", ...pages.map((p) => `/${p.slug}`)].map((u) => `<url><loc>${SITE}${u}</loc><lastmod>${today}</lastmod></url>`).join("\n") + "\n</urlset>\n");
fs.writeFileSync(path.join(DIST, "_headers"), "/*.md\n  Content-Type: text/markdown; charset=utf-8\n/llms*.txt\n  Content-Type: text/plain; charset=utf-8\n/*.json\n  Access-Control-Allow-Origin: *\n");
console.log(`built ${pages.length} pages, ${gl.length} glossary terms -> dist/`);
