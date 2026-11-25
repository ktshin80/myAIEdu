# myAIEdu 아키텍처 규칙 (실무 밸런스형)

이 프로젝트의 모든 코드는 아래 구조와 규칙을 따른다. 규칙과 충돌하는 요청을 받으면 먼저 어느 규칙과 충돌하는지 알리고, 사용자가 예외를 승인한 경우에만 어긴다. 승인된 예외는 이 파일에 기록한다.

"밸런스형"이란 계층은 분리하되 과한 추상화는 하지 않는다는 뜻이다. 인터페이스, 추상 클래스, DI 컨테이너, 외부 프레임워크는 만들지 않는다.

## 1. 디렉터리 구조 (강제)

```
myAIEdu/
├─ server.py          # 진입점. src.back.main.main() 호출만. 로직 금지
├─ data/              # 런타임 데이터(academy.db). 코드 금지
└─ src/
   ├─ back/           # 모든 백엔드 코드
   │  ├─ config.py        설정과 경로 (__file__ 기준)
   │  ├─ main.py          조립 지점(composition root)
   │  ├─ errors.py        AppError 계열
   │  ├─ models/          dataclass, 입력 검증
   │  ├─ repositories/    SQL
   │  ├─ services/        업무 규칙, 트랜잭션
   │  ├─ routers/         HTTP 요청 ↔ 서비스 연결
   │  ├─ web/             http.server 어댑터, Router, 정적 파일
   │  └─ db/              Database, schema, seed
   └─ front/          # 모든 프론트엔드 코드
      ├─ index.html
      ├─ css/
      └─ js/
```

- 백엔드 코드는 `src/back/`, 프론트엔드 코드는 `src/front/` 밖에 두지 않는다. 프로젝트 루트에는 `server.py`만 `.py`로 허용한다.
- 새 폴더가 필요하면 위 계층 중 어디에 속하는지 먼저 정한다. 어디에도 속하지 않으면 만들기 전에 사용자에게 묻는다.
- `src/front/`는 서버가 그대로 서빙하는 정적 파일이다. 백엔드 코드를 import하거나 참조하지 않는다.

## 2. 의존 방향 (강제)

```
routers → services → repositories → models, errors
routers → web/router.py (Route, Response 값 객체만)
web → errors (AppError 변환용). routers, services, repositories, models는 import하지 않는다
main.py → 모든 계층 (조립 전용)
```

- 의존은 위 화살표 방향으로만 흐른다. 역방향 import 금지: `services`가 `routers`나 `web`을, `repositories`가 `services`를 import하면 안 된다. `web/`은 도메인 코드를 모른 채 `main.py`가 넘겨준 Router만 쓴다.
- `models`와 `errors`는 `http`, `sqlite3`, `json`을 import하지 않는다. 예외로 `models`는 `errors`를 import할 수 있다.
- 구현체를 만들고 서로 연결하는 일(`Database(...)`, `XxxService(database)`)은 `main.py`에서만 한다. 다른 파일에서 서비스나 `Database`를 직접 생성하지 않는다.
- 상대 import(`from ..models.cohort import Cohort`)만 쓴다. `src.back...` 절대 import는 `server.py`에서만 허용한다.

## 3. 계층별 책임

### models/
- 데이터 모양은 `@dataclass(frozen=True)`로 쓴다.
- 입력 형식 검증은 `from_payload` 같은 클래스 메서드에서 끝낸다. 실패하면 `ValidationError`를 raise한다.
- 그 모델만으로 판단되는 순수 규칙은 메서드로 둔다(예: `Cohort.is_full`). DB를 읽어야 하는 규칙은 서비스에 둔다.

### repositories/
- SQL은 이 계층에만 둔다. 다른 계층에 SQL 문자열을 쓰지 않는다.
- 파일 하나는 테이블 하나다(`xxx_repo.py`). 함수는 `conn`을 첫 인자로 받고 모델(dataclass)을 돌려준다. `sqlite3.Row`나 dict를 밖으로 내보내지 않는다.
- 값은 항상 `?` 파라미터로 바인딩한다. f-string이나 `%`로 값을 SQL에 끼워 넣지 않는다. f-string은 고정된 컬럼 목록 상수에만 허용한다.
- `commit`, `rollback`, `close`를 호출하지 않는다. 트랜잭션은 서비스가 정한다.
- `sqlite3` 예외는 여기서 `errors.py`의 업무 오류로 바꿔 올린다(예: `DuplicateEnrollmentError`).

### services/
- 업무 규칙과 트랜잭션 경계를 맡는다. 클래스 하나는 도메인 하나이며 `Database`를 생성자로 받는다(`XxxService`).
- 쓰기는 `with self.database.transaction() as conn:`, 읽기는 `with self.database.session() as conn:`만 쓴다. 직접 `connect()`하지 않는다.
- 규칙 위반은 응답을 만들지 않고 `AppError` 하위 예외를 raise한다. 트랜잭션 안에서 raise하면 전부 롤백된다는 점을 이용한다. 쓰기 도중 `return`으로 오류를 돌려주지 않는다.
- HTTP 개념(상태 코드, 헤더, `Request`, `Response`)을 모른다. 반환값은 모델이나 결과 dataclass다.

### routers/
- 파일 하나는 도메인 하나이며 `build_routes(service) -> list[Route]`를 제공한다.
- 하는 일은 세 가지뿐이다: 요청에서 값을 꺼내 모델로 만든다 → 서비스를 호출한다 → `Response`로 감싼다. 업무 규칙, SQL, 트랜잭션을 두지 않는다.
- 응답 본문은 `dataclasses.asdict`로 만든 dict나 list다. 사용자에게 보이는 성공 메시지는 이 계층에서 만든다.
- 새 라우트는 `main.py`의 `build_router`에 `router.include(...)`를 한 줄 추가해야 활성화된다.

### web/
- `http.server`와 정적 파일 서빙만 맡는다. 도메인 이름(수강생, 기수)이 나오면 잘못된 위치다.
- `AppError`는 `{"error": 메시지}`와 `e.status`로, 그 외 예외는 로그를 남기고 500으로 바꾼다. 스택 트레이스를 응답 본문에 넣지 않는다.
- 정적 파일은 `StaticFiles.read`의 `realpath` 검사를 통해서만 읽는다. 사용자 입력 경로로 직접 `open()`하지 않는다.

### db/
- 스키마는 `schema.py`(`CREATE TABLE IF NOT EXISTS`), 초기 데이터는 `seed.py`에만 둔다. 연결과 트랜잭션은 `Database`가 독점한다.
- 마이그레이션 도구는 없다. 스키마를 바꾸면 `schema.py`를 고치고, 기존 데이터를 지켜야 하면 변환 방법을 사용자에게 먼저 묻는다. `data/academy.db`를 임의로 삭제하거나 덮어쓰지 않는다.

## 4. 새 기능 추가 절차

1. `models/`: dataclass와 입력 검증을 만든다.
2. `repositories/`: SQL 함수를 만든다.
3. `services/`: 업무 규칙과 트랜잭션을 만든다. 필요한 오류는 `errors.py`에 추가한다.
4. `routers/`: `build_routes`를 만든다.
5. `main.py`: 서비스를 만들어 `build_router`에 등록한다.
6. `src/front/`: 화면과 `fetch` 호출을 추가한다.
7. 검증하고 `CLAUDE.md`의 구조 설명이 바뀌었으면 함께 고친다.

## 5. 코딩 규칙

### 공통
- **표준 라이브러리만 쓴다.** 새 패키지를 설치하거나 `requirements`를 만들지 않는다. 필요해 보이면 구현하기 전에 사용자에게 묻는다.
- 사용자에게 보이는 모든 문구(화면, 오류 메시지, 로그 안내)는 한국어다. 식별자(변수, 함수, 클래스, 파일명)는 영어 `snake_case`/`PascalCase`다.
- 주석과 docstring은 한국어로 쓰고, 코드만 봐서는 알 수 없는 이유(왜)만 적는다.
- 타입 힌트는 dataclass 필드에 필수다. 함수 시그니처는 선택이며, 쓰려면 파일 안에서 일관되게 쓴다. `X | None` 문법을 쓴다.
- 파일 인코딩은 UTF-8이다. JSON 출력은 `ensure_ascii=False`다.
- 파일을 읽고 쓰는 경로는 `config.py`나 `__file__`에서 계산한다. 현재 작업 디렉터리에 의존하지 않는다.
- 요청한 범위를 넘는 리팩토링, 미사용 코드, 만약을 위한 추상화를 추가하지 않는다.

### 백엔드
- API 경로는 `/api/` 접두사와 소문자 복수 명사나 동작 이름을 쓴다(`/api/cohorts`, `/api/enroll`). 기존 경로는 승인 없이 바꾸지 않는다.
- 응답 코드: 조회 200, 생성 201, 형식 오류 400, 없음 404, 상태 충돌(중복, 정원) 409, 서버 오류 500.
- 오류 응답 본문은 항상 `{"error": "한국어 메시지"}`다. 성공 응답에는 `error` 키를 쓰지 않는다.
- 외부 입력(쿼리, 본문)은 신뢰하지 않는다. 타입과 범위를 모델에서 검증한 뒤에만 서비스로 넘긴다.
- 개인정보(이름, 이메일, 전화번호)를 로그나 오류 메시지에 그대로 남기지 않는다.
- `print`는 서버 시작 안내에만 쓴다. 디버깅용 출력은 커밋 전에 지운다.

### 프론트엔드
- 서버가 보내거나 사용자가 입력한 문자열은 `textContent`나 `createTextNode`로만 화면에 넣는다. `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `eval`에 외부 문자열을 쓰지 않는다.
- 파일은 역할별로 둔다: HTML은 `src/front/` 루트, CSS는 `css/`, JS는 `js/`. 인라인 `<style>`, `<script>`, `style=""`, `onclick=""` 같은 인라인 핸들러를 쓰지 않는다.
- 자원 경로는 서버 루트 기준 절대 경로를 쓴다(`/css/style.css`, `/js/app.js`).
- API 호출은 `fetch`로 `/api/...`만 부른다. 응답의 `ok`를 확인하고, 실패하면 서버가 준 `error` 문구를 사용자에게 보여 준다.
- 빌드 도구, 번들러, 외부 CDN 스크립트를 쓰지 않는다. 브라우저 표준 기능만 쓴다.
- 화면 문구를 바꿀 때는 접근성(`label`, 의미 있는 태그, 충분한 글자 크기)을 유지한다. 대상 사용자는 4050이다.

## 6. 실행과 검증

- 서버는 프로젝트 루트에서 `python server.py`로 실행한다. `src/back/main.py`를 직접 실행하지 않는다(상대 import가 깨진다). `python -m src.back.main`은 허용한다.
- 코드를 바꾼 뒤에는 `python -m compileall -q src server.py`로 문법을 확인한다.
- API를 바꿨다면 **임시 DB**로 확인한다. `Database(임시경로)`와 `create_server(database, host, port)`로 8000이 아닌 포트에 서버를 띄운다. 실제 `data/academy.db`로 테스트 신청을 만들지 않는다. 만들었다면 반드시 지운다.
- 임시 검증 스크립트는 프로젝트 폴더가 아니라 세션 scratchpad에 둔다.
- 포트 8000에 이미 서버가 떠 있으면 사용자의 프로세스일 수 있다. 임의로 종료하지 않고 다른 포트로 검증한 뒤 알린다.
- 확인하지 못한 것(예: 브라우저에서 직접 열어 보지 않음)은 보고할 때 명시한다.

## 7. 금지 목록

- `src/back/` 밖의 백엔드 코드, `src/front/` 밖의 프론트 코드
- 계층 건너뛰기: 라우터에서 저장소 호출, 서비스에서 SQL 작성, 저장소에서 `commit`
- `main.py` 밖에서 서비스나 `Database` 생성
- SQL 문자열에 값을 직접 이어 붙이기
- 외부 문자열을 `innerHTML` 등으로 화면에 삽입
- 승인 없는 패키지 설치, 기존 API 경로 변경, `data/academy.db` 삭제나 덮어쓰기
- 영어로 된 사용자 노출 문구
