"""SQLite 연결과 트랜잭션 경계. 경로는 생성자로 받아 테스트에서 임시 DB를 쓸 수 있다."""
import os
import sqlite3
from contextlib import contextmanager

from .schema import SCHEMA
from .seed import seed


class Database:
    def __init__(self, path):
        self.path = path

    def _connect(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def init(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        conn = self._connect()
        try:
            conn.executescript(SCHEMA)
            with conn:
                seed(conn)
        finally:
            conn.close()

    @contextmanager
    def session(self):
        """조회 전용 연결."""
        conn = self._connect()
        try:
            yield conn
        finally:
            conn.close()

    @contextmanager
    def transaction(self):
        """쓰기 트랜잭션. 블록에서 예외가 나면 모두 롤백한다.

        BEGIN IMMEDIATE로 시작해 '정원 확인 후 삽입' 사이에 다른 요청이 끼어들지 못하게 한다.
        """
        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            yield conn
            conn.commit()
        except BaseException:
            conn.rollback()
            raise
        finally:
            conn.close()
