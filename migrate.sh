# ENTRYPOINT와 RUN의 차이
# ENTRYPOINT는 컨테이너가 시작될 때 실행되는 명령어를 지정하는 것이고,
# RUN은 이미지를 빌드할 때 실행되는 명령어를 지정하는 것이다.

# 로컬에서 작업이 이루어진다면, 단순히 작업하는 시간에만 차이가 있는 것이지만,
# 이 작업에서는
# 로컬에서 이미지를 빌드하고, 클라우드 플랫폼에서 실행하므로
# DB 마이그래이션은 "DB가 존재"하는 클라우드 플랫폼에서 수행해야한다. -> ENTRYPOINT

# !/bin/bash

# DB Migration 실행
poetry run python -m api.migrate_cloud_db

# 서버 실행
poetry run python -m api.main:app --host 0.0.0.0 --reload