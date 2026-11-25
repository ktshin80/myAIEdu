"""초기 데이터. 커리큘럼을 바꾸려면 CURRICULUM을 고치고 data/academy.db를 지운다."""

# 기획서의 8주 커리큘럼. 결과물은 인터뷰 후 조정할 예시다.
CURRICULUM = [
    (1, 1, "AI 기초와 안전 사용", "common", "내 업무 안전 사용 체크리스트"),
    (2, 2, "프롬프트 기초", "common", "내 업무용 프롬프트 3개"),
    (3, 4, "직장인 실무: 보고서·데이터", "worker", "보고서 초안, 메일 템플릿, 데이터 요약"),
    (5, 6, "자영업자 실무: 홍보·고객 응대·자동화", "owner", "홍보 문구, 응대 문구집, 자동화 흐름"),
    (7, 7, "개인 프로젝트", "common", "내 업무 해결 완성물"),
    (8, 8, "발표와 수료 후 학습 계획", "common", "발표 자료, 개인 학습 로드맵"),
]


def seed(conn):
    if conn.execute("SELECT COUNT(*) FROM curriculum").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO curriculum (week_start, week_end, title, track, deliverable) "
            "VALUES (?, ?, ?, ?, ?)",
            CURRICULUM,
        )
    if conn.execute("SELECT COUNT(*) FROM cohorts").fetchone()[0] == 0:
        conn.execute("INSERT INTO cohorts (name) VALUES (?)", ("파일럿 1기",))
