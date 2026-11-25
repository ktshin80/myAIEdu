"""8주차 선택 실습: 질문에 답하면 한 장 비즈니스 캔버스(HTML), 월 예상 수익, 실습용 AI 프롬프트를 만든다.

7주차 brand_profile.py와 같은 이유로 AI 서비스에 직접 접속하지 않고 프롬프트만 만든다.
수익 계산은 수강생이 입력한 가정값으로만 하며, 세금과 비용은 사람마다 달라 빼고 계산한다.

실행: python courseware/week08/examples/business_canvas.py [--demo] [--out 폴더]
"""

import argparse
import html
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
# 결과 HTML이 파일 하나로 열리도록 소개 페이지 예시와 같은 CSS를 읽어 넣는다
PAGE_CSS = HERE / "landing_page.css"

# 캔버스 칸 순서는 lab-guide.md 실습 1의 3단계와 같아야 수업 중에 헷갈리지 않는다
FIELDS = [
    ("customer", "고객", "정확히 누구인가요? (나이, 상황, 직업)"),
    ("problem", "고객의 문제", "고객은 지금 무엇 때문에 곤란한가요?"),
    ("solution", "해결책", "내가 무엇을 해 주나요?"),
    ("edge", "나만의 강점", "왜 다른 사람이 아니라 나인가요?"),
    ("channel", "고객을 만나는 곳", "어디서 처음 알릴 건가요?"),
    ("pricing", "가격과 방식", "얼마를 어떻게 받나요? (가정)"),
    ("needs", "필요한 것", "시작하는 데 드는 시간, 돈, 도구는?"),
    ("unknowns", "확인할 것", "아직 모르는 것, 고객에게 물어봐야 할 것은?"),
]


@dataclass(frozen=True)
class Canvas:
    title: str
    cells: dict[str, str]
    price_per_session: int
    hours_per_session: float
    sessions_per_month: int

    def monthly_revenue(self):
        return self.price_per_session * self.sessions_per_month

    def monthly_hours(self):
        return self.hours_per_session * self.sessions_per_month

    def hourly_rate(self):
        # 준비 시간을 0으로 입력하면 0으로 나누게 되므로 시급을 계산하지 않는다
        if self.hours_per_session <= 0:
            return None
        return round(self.price_per_session / self.hours_per_session)


# --demo용 가상 아이디어. 7주차 예시 인물(김영수)과 이어지며 실존 인물, 회사가 아니다.
DEMO = Canvas(
    title="작은 공장 품질 주치의",
    cells={
        "customer": "품질 담당자가 따로 없는 직원 30명 이하 제조사 사장님",
        "problem": "거래처가 품질 기록을 요구하는데 무엇을 어떻게 남겨야 할지 몰라 계약이 불안하다.",
        "solution": "1회 현장 진단 후 불량 기록 엑셀 양식을 만들어 주고, 월 2회 방문해 기록을 함께 분석한다.",
        "edge": "제조 품질 25년 경력, 반품률 4%를 1%로 낮춘 경험(사례), 신입 교육 경험으로 쉽게 설명한다.",
        "channel": "지역 산업단지 협의회 모임, 예전 협력사 사장님 소개, 블로그에 품질 기록 팁 연재",
        "pricing": "1회 진단 30만 원(가정), 이후 월 자문 60만 원(가정)",
        "needs": "주말 하루, 노트북, 엑셀 양식 3종, 겸업 규정 확인",
        "unknowns": "사장님들이 진단에 30만 원을 낼지, 평일 방문이 필요한지, 겸업이 가능한지",
    },
    price_per_session=300_000,
    hours_per_session=6,
    sessions_per_month=2,
)


def ask(question):
    while True:
        answer = input(f"{question}\n> ").strip()
        if answer:
            return answer
        print("한 글자 이상 입력해 주세요.")


def ask_number(question, cast):
    # 금액에 쉼표나 '원'을 붙여 입력하는 경우가 많아 지운 뒤 숫자로 바꾼다
    while True:
        raw = ask(question).replace(",", "").replace("원", "").replace("시간", "").replace("회", "").strip()
        try:
            value = cast(raw)
        except ValueError:
            print("숫자로만 입력해 주세요. 예) 300000")
            continue
        if value < 0:
            print("0 이상으로 입력해 주세요.")
            continue
        return value


def collect_canvas():
    print("한 장 비즈니스 캔버스를 만듭니다. 숫자는 모두 가정이어도 괜찮습니다.\n")
    title = ask("서비스 이름은? (예: 작은 공장 품질 주치의)")
    cells = {key: ask(f"[{label}] {question}") for key, label, question in FIELDS}
    price = ask_number("1회 서비스 가격은 몇 원인가요? (가정)", int)
    hours = ask_number("1회에 드는 시간은 준비 포함 몇 시간인가요?", float)
    sessions = ask_number("한 달에 몇 번 할 수 있을 것 같나요?", int)
    return Canvas(title, cells, price, hours, sessions)


def won(amount):
    return f"{amount:,}원"


def build_prompts(canvas):
    summary = "\n".join(f"{label}: {canvas.cells[key]}" for key, label, _ in FIELDS)
    base = f"서비스 이름: {canvas.title}\n{summary}"
    return [
        (
            "실습 2-1. 약점 점검",
            "당신은 냉정한 투자 심사역입니다. 아래 캔버스를 보고 이 아이디어가 실패할 수 있는 이유 5가지와, "
            "각각을 30일 안에 확인할 작은 방법을 알려 주세요.\n\n" + base,
        ),
        (
            "실습 2-2. 고객 인터뷰 질문",
            "아래 서비스의 고객 후보와 15분 대화하려고 합니다. 판매하는 느낌 없이 고객이 실제로 겪은 문제를 알아내는 "
            "과거 경험 질문 5개를 만들어 주세요.\n\n" + base,
        ),
        (
            "실습 3. 3분 발표 대본",
            "아래 캔버스로 동료 4명 앞에서 3분 발표를 합니다. 슬라이드 5장(나는 누구인가 → 고객의 문제 → 해결책 → 왜 나인가 → "
            "다음 30일 계획)의 제목과 핵심 문장, 그리고 3분 분량 대본을 존댓말로 써 주세요. 숫자에는 (가정)을 붙여 주세요.\n\n" + base,
        ),
        (
            "실습 4. 90일 로드맵",
            "아래 캔버스를 바탕으로 수료 후 90일 계획을 표로 만들어 주세요. 1~30일은 고객 후보 5명과 대화, 31~60일은 시범 서비스 1회, "
            "61~90일은 가격과 서비스 개선이 목표입니다. 직장을 다니며 하루 30분 안에 할 수 있는 일로만 채워 주세요.\n\n" + base,
        ),
        (
            "선택. 소개 페이지 문구",
            "아래 서비스의 한 쪽짜리 소개 페이지 문구를 써 주세요. 큰 제목 1개, 고객의 고민 3개, 제공 내용 3단계, "
            "자주 묻는 질문 3개로 구성하고, 50~60대 사장님이 읽기 쉬운 말로 써 주세요.\n\n" + base,
        ),
    ]


def render_canvas(canvas):
    # 수강생 입력이 HTML로 해석되지 않도록 화면에 넣는 모든 값을 escape한다
    e = html.escape
    cells = "\n".join(
        f'      <article class="cell"><h3>{e(label)}</h3><p>{e(canvas.cells[key])}</p></article>'
        for key, label, _ in FIELDS
    )
    rate = canvas.hourly_rate()
    rate_text = won(rate) if rate is not None else "계산할 수 없음 (시간을 0으로 입력함)"
    css = PAGE_CSS.read_text(encoding="utf-8")
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(canvas.title)} 비즈니스 캔버스</title>
  <style>
{css}
  </style>
</head>
<body>
  <header class="hero">
    <p class="eyebrow">한 장 비즈니스 캔버스</p>
    <h1>{e(canvas.title)}</h1>
  </header>
  <main>
    <section class="canvas" aria-label="캔버스 8칸">
{cells}
    </section>
    <section>
      <h2>월 예상 수익 (가정)</h2>
      <table class="numbers">
        <tr><th scope="row">1회 가격</th><td>{won(canvas.price_per_session)}</td></tr>
        <tr><th scope="row">한 달 횟수</th><td>{canvas.sessions_per_month}회</td></tr>
        <tr><th scope="row">월 매출</th><td>{won(canvas.monthly_revenue())}</td></tr>
        <tr><th scope="row">월 투입 시간</th><td>{canvas.monthly_hours():g}시간</td></tr>
        <tr><th scope="row">시간당 금액</th><td>{rate_text}</td></tr>
      </table>
      <p class="note">세금, 교통비, 재료비는 빠진 금액입니다. 고객 인터뷰 후 다시 계산하세요.</p>
    </section>
  </main>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="한 장 비즈니스 캔버스와 AI 프롬프트를 만듭니다.")
    parser.add_argument("--demo", action="store_true", help="가상 아이디어로 바로 결과를 만듭니다.")
    parser.add_argument("--out", type=Path, default=HERE / "output", help="결과 파일을 저장할 폴더")
    args = parser.parse_args()

    canvas = DEMO if args.demo else collect_canvas()
    args.out.mkdir(parents=True, exist_ok=True)

    canvas_path = args.out / "my_business_canvas.html"
    canvas_path.write_text(render_canvas(canvas), encoding="utf-8")

    prompt_path = args.out / "my_prompts.txt"
    blocks = [f"=== {title} ===\n{body}\n" for title, body in build_prompts(canvas)]
    prompt_path.write_text("\n".join(blocks), encoding="utf-8")

    print("\n완성했습니다.")
    print(f"- 월 매출(가정): {won(canvas.monthly_revenue())}, 월 투입 시간: {canvas.monthly_hours():g}시간")
    print(f"- 캔버스: {canvas_path}  (더블클릭해서 브라우저로 여세요)")
    print(f"- 프롬프트 모음: {prompt_path}  (실습 2~4에서 AI 채팅창에 붙여 넣으세요)")


if __name__ == "__main__":
    main()
