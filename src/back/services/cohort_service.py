from ..repositories import cohort_repo


class CohortService:
    def __init__(self, database):
        self.database = database

    def list(self):
        with self.database.session() as conn:
            return cohort_repo.list_all(conn)
