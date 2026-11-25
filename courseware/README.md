# myAIEdu 강의 자료 (courseware)

직장인을 위한 8주 생성형 AI 과정의 강사용 강의록, 수강생용 실습 가이드, 실습 예시 코드를 모아 둔 폴더다.
이 폴더는 웹 서버가 서빙하지 않으며 서버 코드(`src/`)와도 관계가 없다. (`architecture.md`의 승인된 예외)

## 구성

| 주차 | 주제 | 강의록 | 실습 가이드 | 예시 코드 |
|------|------|--------|-------------|-----------|
| 7주차 | 퍼스널 브랜딩 완성형 | [lecture.md](week07/lecture.md) | [lab-guide.md](week07/lab-guide.md) | [brand_profile.py](week07/examples/brand_profile.py), [profile_card.html](week07/examples/profile_card.html) |
| 8주차 | 나의 경험. AI를 만나 비즈니스가 되다 | [lecture.md](week08/lecture.md) | [lab-guide.md](week08/lab-guide.md) | [business_canvas.py](week08/examples/business_canvas.py), [landing_page.html](week08/examples/landing_page.html) |

- 7·8주차 주제는 서버 커리큘럼(`src/back/db/seed.py`)의 "개인 프로젝트", "발표와 수료 후 학습 계획"을 구체화한 것이다. 결과물(내 업무 해결 완성물, 발표 자료, 개인 학습 로드맵)도 자료 안에 담았다.
- 결과물 문구와 예시 인물은 인터뷰 전 예시다. 실제 수강생 정보를 넣지 않는다.

## 예시 코드 실행 방법

- 설치할 것이 없다. Python 3.10 이상만 있으면 된다.
- 예시 코드는 AI 서비스에 직접 접속하지 않는다. AI 채팅창(ChatGPT, Claude, Gemini 등)에 붙여 넣을 **프롬프트**와 **결과 HTML 파일**을 만든다. API 키나 결제가 필요 없다.

```bash
# 질문에 답하면서 만들기
python courseware/week07/examples/brand_profile.py

# 예시 인물로 바로 결과 보기
python courseware/week07/examples/brand_profile.py --demo
python courseware/week08/examples/business_canvas.py --demo
```

- 결과 파일은 스크립트 옆 `output/` 폴더에 생긴다(git에 올라가지 않음). `--out 폴더`로 위치를 바꿀 수 있다.
- `profile_card.html`, `landing_page.html`은 더블클릭해서 브라우저로 바로 열리는 완성 예시(정답 예시)다.
