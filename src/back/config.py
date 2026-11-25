"""서버 설정과 경로. 경로는 현재 폴더가 아니라 이 파일 위치에서 계산한다."""
import os

HOST, PORT = "127.0.0.1", 8000
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(ROOT_DIR, "data", "academy.db")
FRONT_DIR = os.path.join(ROOT_DIR, "src", "front")
