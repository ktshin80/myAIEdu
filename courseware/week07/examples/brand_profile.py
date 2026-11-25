"""7주차 선택 실습: 질문에 답하면 브랜드 프로필 카드(HTML)와 AI 프롬프트 모음을 만든다.

AI 서비스에 직접 접속하지 않는 이유: 수강생마다 쓰는 서비스가 다르고 API 키 발급은 4050 입문자에게 큰 장벽이다.
그래서 이 스크립트는 채팅창에 붙여 넣을 프롬프트를 만들어 주는 데서 멈춘다.

실행: python courseware/week07/examples/brand_profile.py [--demo] [--out 폴더]
"""

import argparse
import html
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
# 결과 카드가 파일 하나로 열리도록 완성 예시와 같은 CSS를 읽어 HTML 안에 넣는다
CARD_CSS = HERE / "profile_card.css"


@dataclass(frozen=True)
class BrandProfile:
    name: str
    headline: str
    strengths: tuple[str, str, str]
    story_situation: str
    story_action: str
    story_result: str
    direction: str


# --demo용 가상 인물. 실존 인물이나 실제 회사가 아니다.
DEMO = BrandProfile(
    name="김영수",
    headline="불량 원인을 사흘 안에 찾아내는 25년 차 품질 해결사",
    strengths=("현장 데이터 읽기", "협력사 설득", "신입 교육"),
    story_situation="2019년 주력 제품의 반품률이 4%까지 올라 거래처 A사가 계약 재검토를 통보했다.",
    story_action="3년 치 검사 기록을 엑셀로 다시 묶어 불량이 특정 공정 야간조에 몰린다는 것을 찾고, 협력사와 공정 기준을 새로 만들었다.",
    story_result="6개월 만에 반품률을 1% 수준으로 낮추고 계약을 지켰다.",
    direction="중소 제조사가 품질 체계를 처음 만들 때 곁에서 돕고 싶다.",
)


def ask(question):
    # 빈 답을 그대로 두면 카드에 빈칸이 생기므로 답할 때까지 다시 묻는다
    while True:
        answer = input(f"{question}\n> ").strip()
        if answer:
            return answer
        print("한 글자 이상 입력해 주세요.")


def collect_profile():
    print("브랜드 프로필 카드를 만듭니다. 회사 이름, 동료 이름은 'A사', 'B팀장'처럼 바꿔서 입력하세요.\n")
    name = ask("1. 카드에 표시할 이름(또는 별명)은?")
    headline = ask("2. 한 줄 소개는? (대상 + 해결하는 문제 + 결과)")
    strengths = tuple(ask(f"3-{i}. 강점 {i}번은?") for i in (1, 2, 3))
    situation = ask("4. 대표 사례: 어떤 상황이었나요?")
    action = ask("5. 대표 사례: 내가 한 일은?")
    result = ask("6. 대표 사례: 결과는?")
    direction = ask("7. 이 경험을 앞으로 어디에 쓰고 싶나요?")
    return BrandProfile(name, headline, strengths, situation, action, result, direction)


def build_prompts(profile):
    strengths = ", ".join(profile.strengths)
    draft = (
        f"한 줄 소개: {profile.headline}\n"
        f"강점: {strengths}\n"
        f"사례: {profile.story_situation} {profile.story_action} {profile.story_result}\n"
        f"앞으로의 방향: {profile.direction}"
    )
    return [
        (
            "검토자 프롬프트 (과장 찾기)",
            "깐깐한 검토자 역할을 해 주세요. 아래 프로필에서 과장된 표현, 누구에게나 해당하는 뻔한 표현, "
            "50대 직장인이 직접 말하기 어색한 표현을 찾아 '원래 문장 → 고친 문장'으로 보여 주세요. "
            "제가 말하지 않은 사실은 추가하지 마세요.\n\n" + draft,
        ),
        (
            "자기소개 30초 버전",
            "아래 프로필로 모임이나 면접에서 말할 30초 자기소개를 써 주세요. "
            "소리 내어 읽기 쉽게 짧은 문장으로, 존댓말로 써 주세요.\n\n" + draft,
        ),
        (
            "8주차 준비: 비즈니스 아이디어",
            "아래 프로필의 강점 중 다른 사람이 돈을 내고 도움을 받을 만한 것을 골라, "
            "퇴근 후나 주말에 시작할 수 있는 작은 서비스 아이디어를 3개 제안해 주세요. "
            "각각 누가 고객인지, 무엇을 해 주는지 한 줄로 써 주세요.\n\n" + draft,
        ),
    ]


def render_card(profile):
    # 사용자가 입력한 문자열이 HTML 태그로 해석되지 않도록 모두 escape한다
    e = html.escape
    strengths = "\n".join(f"        <li>{e(s)}</li>" for s in profile.strengths)
    css = CARD_CSS.read_text(encoding="utf-8")
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(profile.name)} 프로필 카드</title>
  <style>
{css}
  </style>
</head>
<body>
  <main class="card">
    <header>
      <p class="label">퍼스널 브랜드 프로필</p>
      <h1>{e(profile.name)}</h1>
      <p class="headline">{e(profile.headline)}</p>
    </header>
    <section>
      <h2>나의 강점</h2>
      <ul class="strengths">
{strengths}
      </ul>
    </section>
    <section>
      <h2>대표 사례</h2>
      <dl class="story">
        <dt>상황</dt><dd>{e(profile.story_situation)}</dd>
        <dt>내가 한 일</dt><dd>{e(profile.story_action)}</dd>
        <dt>결과</dt><dd>{e(profile.story_result)}</dd>
      </dl>
    </section>
    <section>
      <h2>앞으로의 방향</h2>
      <p>{e(profile.direction)}</p>
    </section>
  </main>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="브랜드 프로필 카드와 AI 프롬프트를 만듭니다.")
    parser.add_argument("--demo", action="store_true", help="가상 인물로 바로 결과를 만듭니다.")
    parser.add_argument("--out", type=Path, default=HERE / "output", help="결과 파일을 저장할 폴더")
    args = parser.parse_args()

    profile = DEMO if args.demo else collect_profile()
    args.out.mkdir(parents=True, exist_ok=True)

    card_path = args.out / "my_profile_card.html"
    card_path.write_text(render_card(profile), encoding="utf-8")

    prompt_path = args.out / "my_prompts.txt"
    blocks = [f"=== {title} ===\n{body}\n" for title, body in build_prompts(profile)]
    prompt_path.write_text("\n".join(blocks), encoding="utf-8")

    print("\n완성했습니다.")
    print(f"- 프로필 카드: {card_path}  (더블클릭해서 브라우저로 여세요)")
    print(f"- 프롬프트 모음: {prompt_path}  (AI 채팅창에 붙여 넣어 더 다듬으세요)")


if __name__ == "__main__":
    main()
