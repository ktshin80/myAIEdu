from ..models.curriculum import CurriculumItem


def list_by_track(conn, track=None):
    """track이 있으면 공통과 해당 트랙만, 없으면 전체를 주차 순으로."""
    sql = "SELECT * FROM curriculum"
    args = []
    if track:
        sql += " WHERE track IN ('common', ?)"
        args.append(track)
    rows = conn.execute(sql + " ORDER BY week_start", args)
    return [CurriculumItem(**dict(r)) for r in rows]
