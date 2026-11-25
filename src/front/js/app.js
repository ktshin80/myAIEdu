const TRACK_LABEL = { common: "공통", worker: "직장인", owner: "자영업자" };
const weeksEl = document.getElementById("weeks");
const form = document.getElementById("form");
const msg = document.getElementById("msg");

function makeWeek(c) {
  const box = document.createElement("article");
  box.className = "week";
  const when = document.createElement("div");
  when.className = "when";
  when.textContent = c.week_start === c.week_end ? `${c.week_start}주차` : `${c.week_start}~${c.week_end}주차`;
  const badge = document.createElement("span");
  badge.className = "badge";
  badge.textContent = TRACK_LABEL[c.track];
  when.append(badge);
  const title = document.createElement("h3");
  title.textContent = c.title;
  const out = document.createElement("p");
  out.className = "out";
  out.textContent = c.deliverable ? `실습 결과물: ${c.deliverable}` : "";
  box.append(when, title, out);
  return box;
}

async function loadCurriculum(track) {
  try {
    const res = await fetch("/api/curriculum?track=" + encodeURIComponent(track));
    const rows = await res.json();
    weeksEl.replaceChildren(...rows.map(makeWeek));
  } catch {
    weeksEl.textContent = "커리큘럼을 불러오지 못했습니다. 새로고침해 주세요.";
  }
}

async function loadCohorts() {
  const select = form.elements.cohort_id;
  try {
    const rows = await (await fetch("/api/cohorts")).json();
    select.replaceChildren(...rows.map(c => new Option(c.name + (c.start_date ? ` (${c.start_date} 시작)` : " (일정 미정)"), c.id)));
  } catch {
    select.replaceChildren(new Option("기수를 불러오지 못했습니다", ""));
  }
}

document.querySelectorAll(".tab").forEach(btn => btn.addEventListener("click", () => {
  document.querySelectorAll(".tab").forEach(b => b.classList.toggle("active", b === btn));
  loadCurriculum(btn.dataset.track);
}));

form.addEventListener("submit", async e => {
  e.preventDefault();
  const f = form.elements;
  const body = {
    name: f.name.value, email: f.email.value, phone: f.phone.value,
    persona: f.persona.value, cohort_id: parseInt(f.cohort_id.value, 10),
  };
  msg.className = "";
  msg.textContent = "접수 중...";
  try {
    const res = await fetch("/api/enroll", {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
    });
    const data = await res.json();
    msg.className = res.ok ? "ok" : "err";
    msg.textContent = data.message || data.error;
    if (res.ok) form.reset();
  } catch {
    msg.className = "err";
    msg.textContent = "서버에 연결하지 못했습니다. 잠시 후 다시 시도해 주세요.";
  }
});

loadCurriculum("");
loadCohorts();
