// API 문서 및 실습 대시보드.
// 명세는 /make_api_doc으로 만든 API.md와 같은 내용이다. 백엔드가 바뀌면 API.md를 다시 만들고 이 목록도 함께 고친다.
// 외부 문자열은 모두 textContent로만 넣는다(innerHTML 사용 금지).

const API_SPEC = [
  {
    method: "GET",
    path: "/api/curriculum",
    summary: "8주 커리큘럼을 주차 순으로 돌려줍니다.",
    note: "알 수 없는 track 값은 오류 없이 전체 목록으로 처리됩니다.",
    query: [
      { name: "track", type: "string", required: false, desc: "worker 또는 owner. 주면 공통과 해당 트랙만, 생략하면 전체" },
    ],
    body: [],
    success: {
      status: "200 OK",
      example: [{ id: 1, week_start: 1, week_end: 1, title: "AI와 첫 대화", track: "common", deliverable: "첫 대화 기록" }],
      fields: [
        ["id", "integer", "항목 번호"],
        ["week_start / week_end", "integer", "시작·끝 주차"],
        ["title", "string", "강의 제목"],
        ["track", "string", "common, worker, owner 중 하나"],
        ["deliverable", "string | null", "실습 결과물"],
      ],
    },
    errors: [],
    // 실습에서 쓸 입력 칸. 실습 가능한 API만 가진다.
    practice: { inputs: [{ key: "track", label: "트랙(선택)", options: [["", "전체"], ["worker", "직장인"], ["owner", "자영업자"]] }] },
  },
  {
    method: "GET",
    path: "/api/cohorts",
    summary: "수강 신청이 가능한 기수 목록을 돌려줍니다.",
    note: "일정과 정원은 아직 미정이라 start_date와 capacity가 null일 수 있습니다.",
    query: [],
    body: [],
    success: {
      status: "200 OK",
      example: [{ id: 1, name: "파일럿 1기", start_date: null, capacity: null }],
      fields: [
        ["id", "integer", "기수 번호"],
        ["name", "string", "기수 이름"],
        ["start_date", "string | null", "시작일(미정이면 null)"],
        ["capacity", "integer | null", "정원(null이면 제한 없음)"],
      ],
    },
    errors: [],
    practice: { inputs: [] },
  },
  {
    method: "POST",
    path: "/api/enroll",
    summary: "수강 신청을 접수합니다. 한 트랜잭션이라 실패하면 아무것도 저장되지 않습니다.",
    note: "같은 이메일은 한 명의 수강생으로 보며, 같은 기수 중복 신청은 거절합니다.",
    query: [],
    body: [
      { name: "name", type: "string", required: true, desc: "이름. 앞뒤 공백은 제거됩니다." },
      { name: "email", type: "string", required: true, desc: "이메일. 소문자로 바뀌어 저장됩니다." },
      { name: "phone", type: "string", required: false, desc: "연락처" },
      { name: "persona", type: "string", required: false, desc: "worker 또는 owner" },
      { name: "cohort_id", type: "integer", required: true, desc: "신청할 기수 번호(숫자여야 함)" },
    ],
    success: {
      status: "201 Created",
      example: { message: "홍길동님, 파일럿 1기 수강 신청이 접수되었습니다." },
      fields: [["message", "string", "접수 안내 문구"]],
    },
    errors: [
      ["400", "이름이 비었거나 이메일 형식이 틀림", "이름과 올바른 이메일을 입력해 주세요."],
      ["400", "persona가 허용 값이 아님", "유형 값이 올바르지 않습니다."],
      ["400", "cohort_id가 정수가 아님", "기수를 선택해 주세요."],
      ["404", "없는 기수", "존재하지 않는 기수입니다."],
      ["409", "정원 마감", "정원이 마감된 기수입니다."],
      ["409", "같은 기수에 중복 신청", "이미 이 기수에 신청하셨습니다."],
    ],
    // 실제 신청이 DB에 저장되므로 대시보드에서는 호출하지 않는다.
    practice: null,
  },
];

const COMMON_ERROR = '{ "error": "한국어 오류 메시지" }';

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function makeTable(headers, rows) {
  const table = el("table", "doc-table");
  const head = el("tr");
  headers.forEach(h => head.append(el("th", "", h)));
  const thead = el("thead");
  thead.append(head);
  table.append(thead);
  const bodyEl = el("tbody");
  rows.forEach(cells => {
    const tr = el("tr");
    cells.forEach(c => tr.append(el("td", "", c)));
    bodyEl.append(tr);
  });
  table.append(bodyEl);
  return table;
}

function makeJson(value) {
  return el("pre", "doc-json", JSON.stringify(value, null, 2));
}

// 실습 영역: GET API만 실제로 호출해 응답을 보여 준다.
function makePractice(api) {
  const box = el("div", "practice");
  box.append(el("h4", "", "직접 호출해 보기"));
  if (api.practice === null) {
    box.append(el("p", "doc-note", "실제 신청이 저장되기 때문에 여기서는 호출하지 않습니다. 위의 '수강 신청' 양식을 이용해 주세요."));
    return box;
  }
  const values = {};
  api.practice.inputs.forEach(input => {
    const label = el("label", "", input.label);
    const select = document.createElement("select");
    input.options.forEach(([value, text]) => select.append(new Option(text, value)));
    select.addEventListener("change", () => { values[input.key] = select.value; });
    values[input.key] = select.value;
    label.append(select);
    box.append(label);
  });
  const run = el("button", "btn", "호출하기");
  run.type = "button";
  const status = el("p", "practice-status");
  status.setAttribute("role", "status");
  const out = el("pre", "doc-json", "아직 호출하지 않았습니다.");
  run.addEventListener("click", async () => {
    const params = new URLSearchParams();
    Object.entries(values).forEach(([k, v]) => { if (v) params.set(k, v); });
    const url = api.path + (params.toString() ? "?" + params : "");
    status.className = "practice-status";
    status.textContent = "불러오는 중...";
    try {
      const res = await fetch(url);
      const data = await res.json();
      status.className = "practice-status " + (res.ok ? "ok" : "err");
      status.textContent = `${api.method} ${url} → ${res.status}`;
      out.textContent = JSON.stringify(data, null, 2);
    } catch {
      status.className = "practice-status err";
      status.textContent = "서버에 연결하지 못했습니다. 잠시 후 다시 시도해 주세요.";
    }
  });
  box.append(run, status, out);
  return box;
}

function makeApi(api) {
  const details = el("details", "api-item");
  const summary = el("summary");
  summary.append(el("span", "method m-" + api.method.toLowerCase(), api.method), el("code", "", api.path));
  details.append(summary);

  const body = el("div", "api-body");
  body.append(el("p", "", api.summary));
  if (api.note) body.append(el("p", "doc-note", api.note));

  const params = [...api.query.map(p => ({ ...p, where: "쿼리" })), ...api.body.map(p => ({ ...p, where: "본문" }))];
  if (params.length) {
    body.append(el("h4", "", "요청"));
    body.append(makeTable(["위치", "이름", "타입", "필수", "설명"],
      params.map(p => [p.where, p.name, p.type, p.required ? "예" : "아니오", p.desc])));
  }

  body.append(el("h4", "", "성공 응답 " + api.success.status));
  body.append(makeJson(api.success.example));
  body.append(makeTable(["필드", "타입", "설명"], api.success.fields));

  if (api.errors.length) {
    body.append(el("h4", "", "오류"));
    body.append(makeTable(["상태", "조건", "메시지"], api.errors));
  }
  body.append(makePractice(api));
  details.append(body);
  return details;
}

function renderApiDocs() {
  const root = document.getElementById("api-docs-list");
  if (!root) return;
  const intro = el("div", "doc-common");
  intro.append(el("p", "", "오류 응답은 모든 API에서 아래 형식입니다. 예상하지 못한 서버 오류는 500과 일반 안내 문구로만 응답합니다."));
  intro.append(el("pre", "doc-json", COMMON_ERROR));
  root.replaceChildren(intro, ...API_SPEC.map(makeApi));
}

renderApiDocs();

// ---- 실행 및 테스트 ----
// 실제 DB에 데이터를 남기지 않는 요청만 쓴다. POST 테스트는 모두 검증 단계(400)나 기수 확인(404)에서
// 끝나므로 저장되지 않는다. 성공(201)과 중복(409) 확인은 데이터가 남아 여기에 넣지 않는다.
const VALID_BODY = { name: "테스트", email: "test@example.com", phone: "", persona: "", cohort_id: 1 };

const API_TESTS = [
  {
    name: "기수 목록 조회", method: "GET", path: "/api/cohorts", expect: 200,
    check: data => (Array.isArray(data) ? "" : "응답이 목록이 아닙니다."),
  },
  {
    name: "전체 커리큘럼 조회", method: "GET", path: "/api/curriculum", expect: 200,
    check: data => (Array.isArray(data) && data.length > 0 ? "" : "커리큘럼이 비어 있습니다."),
  },
  {
    name: "직장인 트랙은 공통과 직장인만", method: "GET", path: "/api/curriculum?track=worker", expect: 200,
    check: data => (Array.isArray(data) && data.every(i => i.track === "common" || i.track === "worker")
      ? "" : "다른 트랙의 강의가 섞여 있습니다."),
  },
  {
    name: "알 수 없는 트랙은 전체 목록", method: "GET", path: "/api/curriculum?track=zzz", expect: 200,
    check: data => (Array.isArray(data) ? "" : "응답이 목록이 아닙니다."),
  },
  {
    name: "잘못된 이메일은 거절", method: "POST", path: "/api/enroll", expect: 400,
    body: { ...VALID_BODY, email: "형식오류" },
    error: "이름과 올바른 이메일을 입력해 주세요.",
  },
  {
    name: "허용되지 않은 유형은 거절", method: "POST", path: "/api/enroll", expect: 400,
    body: { ...VALID_BODY, persona: "student" },
    error: "유형 값이 올바르지 않습니다.",
  },
  {
    name: "기수 번호가 숫자가 아니면 거절", method: "POST", path: "/api/enroll", expect: 400,
    body: { ...VALID_BODY, cohort_id: "abc" },
    error: "기수를 선택해 주세요.",
  },
  {
    name: "없는 기수는 404", method: "POST", path: "/api/enroll", expect: 404,
    body: { ...VALID_BODY, cohort_id: 999999 },
    error: "존재하지 않는 기수입니다.",
  },
];

async function runTest(test) {
  const options = { method: test.method };
  if (test.body) {
    options.headers = { "Content-Type": "application/json" };
    options.body = JSON.stringify(test.body);
  }
  try {
    const res = await fetch(test.path, options);
    const data = await res.json();
    if (res.status !== test.expect) return { pass: false, detail: `상태 ${test.expect}를 기대했지만 ${res.status}가 왔습니다.` };
    if (test.error && data.error !== test.error) return { pass: false, detail: `오류 메시지가 다릅니다: ${data.error}` };
    const problem = test.check ? test.check(data) : "";
    return problem ? { pass: false, detail: problem } : { pass: true, detail: `상태 ${res.status}` };
  } catch {
    return { pass: false, detail: "서버에 연결하지 못했거나 응답이 JSON이 아닙니다." };
  }
}

function renderTests() {
  const root = document.getElementById("api-tests");
  if (!root) return;
  const summary = el("p", "test-summary", "아직 실행하지 않았습니다.");
  summary.setAttribute("role", "status");
  const list = el("ul", "test-list");
  const rows = API_TESTS.map(test => {
    const item = el("li", "test-row");
    const mark = el("span", "test-mark", "대기");
    item.append(mark, el("span", "test-name", `${test.method} ${test.path} - ${test.name}`));
    const detail = el("span", "test-detail");
    item.append(detail);
    list.append(item);
    return { test, item, mark, detail };
  });
  const runAll = el("button", "btn", "전체 테스트 실행");
  runAll.type = "button";
  runAll.addEventListener("click", async () => {
    runAll.disabled = true;
    summary.textContent = "테스트 중...";
    let passed = 0;
    for (const row of rows) {
      row.mark.textContent = "실행 중";
      row.item.className = "test-row";
      const result = await runTest(row.test);
      row.mark.textContent = result.pass ? "통과" : "실패";
      row.detail.textContent = result.detail;
      row.item.className = "test-row " + (result.pass ? "ok" : "err");
      if (result.pass) passed += 1;
    }
    summary.textContent = `${rows.length}개 중 ${passed}개 통과, ${rows.length - passed}개 실패`;
    runAll.disabled = false;
  });
  root.append(el("p", "doc-note", "실제 신청이 저장되지 않는 요청만 보냅니다. 버튼을 누르면 8개의 확인이 차례로 실행됩니다."), runAll, summary, list);
}

renderTests();
