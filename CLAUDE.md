# CLAUDE.md

4050 AI 교육 서비스의 MVP. 8주 커리큘럼 조회와 수강 신청을 제공하는 웹 서버다. 표준 라이브러리(`http.server`, `sqlite3`)만 쓰며 설치할 패키지가 없다. 사용자에게 보이는 문구는 모두 한국어로 쓴다.

## 실행

`myAIEdu/` 폴더에서 `python server.py`를 실행하고 http://127.0.0.1:8000 을 연다. 처음 실행하면 `data/academy.db`가 만들어지고 커리큘럼과 "파일럿 1기"가 들어간다. 데이터를 초기화하려면 서버를 끄고 `data/academy.db`를 지운다. `src/back/main.py`를 직접 실행하면 상대 import가 깨지므로, 항상 루트의 `server.py`(또는 `python -m src.back.main`)로 실행한다.

## 구조

- `server.py`: 진입점. `src.back.main.main()`만 호출한다.
- `src/back/`: 계층형 구조. 의존 방향은 `routers → services → repositories → models/errors` 한쪽뿐이다.
  - `config.py`: HOST, PORT와 경로(`DB_PATH`, `FRONT_DIR`). 경로는 `__file__` 기준이다.
  - `main.py`: 조립 지점. `Database`, 서비스, 라우터를 만들어 연결한다(`build_router`, `create_server`).
  - `errors.py`: `AppError`(status, message)와 하위 오류. 업무 규칙 위반은 응답 대신 이 오류를 raise한다.
  - `models/`: 불변 dataclass(`Cohort`, `Student`, `Enrollment`, `CurriculumItem`)와 입력 검증(`EnrollRequest.from_payload`).
  - `repositories/`: SQL은 여기에만 둔다. 함수는 `conn`을 첫 인자로 받아 모델을 돌려준다.
  - `services/`: 업무 규칙과 트랜잭션 경계. `Database`를 생성자로 주입받는다. 쓰기는 `database.transaction()`(예외 시 롤백), 읽기는 `database.session()`.
  - `routers/`: 요청을 서비스 호출로, 결과를 JSON 응답으로 바꾼다. `build_routes(service)`가 `Route` 목록을 돌려준다.
  - `web/`: HTTP 어댑터. `router.py`(Router, Request, Response), `handler.py`(`http.server` 연결, `AppError` → JSON), `static.py`(정적 파일).
  - `db/`: `database.py`(연결, 트랜잭션, init), `schema.py`, `seed.py`. 커리큘럼 내용은 `seed.py`의 `CURRICULUM`을 고치고 `data/academy.db`를 지운다.
- `src/front/`: `index.html`, `css/style.css`, `js/app.js`. 사용자 입력은 `textContent`로만 화면에 넣는다.
- `data/`: SQLite 파일(`academy.db`).

## 알아둘 점

- API 추가 순서: 모델, 저장소, 서비스, 라우터를 만들고 `main.py`의 `build_router`에 한 줄 등록한다.
- 수강 신청은 한 트랜잭션이다. 정원 초과나 중복이면 새로 만든 수강생 행도 함께 취소된다.
- 같은 이메일은 한 명의 수강생으로 보고, 같은 기수 중복 신청은 거절한다. 정원(`capacity`)이 NULL이면 제한이 없다.
- 날짜, 정원, 수강료는 아직 미정이라 비워 두었다. 정해지면 `cohorts` 행과 화면 문구를 갱신한다.
- 기획서의 결과물 문구는 인터뷰 전 예시다.
