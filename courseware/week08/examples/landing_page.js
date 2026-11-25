// 예시 페이지라 서버로 보내지 않고 입력 확인 흐름만 보여 준다.
// 수강생이 실제 서비스로 바꿀 때 이 부분을 구글 폼 링크 등으로 대체하도록 수업에서 안내한다.
const form = document.getElementById("inquiry");
const msg = document.getElementById("msg");

function show(text, kind) {
  // 입력값이 섞인 문구도 태그로 해석되지 않도록 textContent만 쓴다
  msg.textContent = text;
  msg.className = kind;
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const data = new FormData(form);
  const company = String(data.get("company") || "").trim();
  const phone = String(data.get("phone") || "").trim();

  if (!company) {
    show("회사 이름을 입력해 주세요.", "err");
    return;
  }
  // 하이픈 유무가 사람마다 달라 숫자만 남겨 자릿수로 확인한다
  const digits = phone.replace(/\D/g, "");
  if (digits.length < 9 || digits.length > 11) {
    show("전화번호를 다시 확인해 주세요. 예) 010-0000-0000", "err");
    return;
  }

  show(`${company}의 상담 신청이 접수되었다고 가정합니다. (예시 페이지라 실제로 전송되지 않았습니다)`, "ok");
  form.reset();
});
