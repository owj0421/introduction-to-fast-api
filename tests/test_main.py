import pytest
import pytest_asyncio
import httpx
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from api.db import get_db, Base
from api.main import app

import starlette.status

ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"


# 픽스처란, 테스트에서 반복적으로 사용되는 설정이나 데이터를 한 곳에 모아 관리하는 개념
# 테스트 함수의 전처리나 후처리를 정의하는 함수
# xUnit 테스트 프레임워크에서는 setUp, tearDown이라는 이름으로 사용
@pytest_asyncio.fixture
async def async_client():
    # 비동기식 DB접속용 engine과 session을 생성
    async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
    async_session = sessionmaker(
        autocommit=False, 
        autoflush=False, 
        bind=async_engine, 
        class_=AsyncSession
    )
    
    # 테스트용으로 온메모리 SQLite 테이블을 초기화(함수별로 재설정)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    # DI로 FastAPI가 사용하는 DB 연결 함수를 테스트용으로 오버라이드
    async def get_test_db():
        async with async_session() as session:
            yield session
            
    app.dependency_overrides[get_db] = get_test_db
    
    # 테스트용 FastAPI 클라이언트 생성
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client


# 실제 테스트 코드 ----------------------------------------------


@pytest.mark.asyncio
async def test_create_and_read(async_client):
    response = await async_client.post("/tasks", json={"title": "테스트작업"})
    assert response.status_code == starlette.status.HTTP_200_OK
    
    response_obj = response.json()
    assert response_obj["title"] == "테스트작업"
    
    response = await async_client.get(f"/tasks")
    assert response.status_code == starlette.status.HTTP_200_OK
    
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["title"] == "테스트작업"
    assert response_obj[0]["done"] == False
    

@pytest.mark.asyncio
async def test_done_flag(async_client):
    response = await async_client.post("/tasks", json={"title": "테스트작업2"})
    assert response.status_code == starlette.status.HTTP_200_OK
    
    response_obj = response.json()
    assert response_obj["title"] == "테스트작업2"
    
    # 완료 플래그를 설정
    response = await async_client.put(f"/tasks/{response_obj['id']}/done")
    assert response.status_code == starlette.status.HTTP_200_OK
    
    # 이미 완료된 작업에 대해 완료 플래그 설정 시도
    response = await async_client.put(f"/tasks/{response_obj['id']}/done")
    assert response.status_code == starlette.status.HTTP_400_BAD_REQUEST
    
    # 완료 플래그를 해제
    response = await async_client.delete(f"/tasks/{response_obj['id']}/done")
    assert response.status_code == starlette.status.HTTP_200_OK
    
    # 이미 완료되지 않은 작업에 대해 완료 플래그 해제 시도
    response = await async_client.delete(f"/tasks/{response_obj['id']}/done")
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND
    
    
# @pytest.mark.asyncio
# async def test_due_date(async_client):
#     input_param_list = [
#         '2024-12-01',
#         '2024-12-32',
#         '2024/12/01',
#         '2024-1201'
#     ]
#     expectation_list = [
#         starlette.status.HTTP_200_OK,
#         starlette.status.HTTP_422_UNPROCESSABLE_ENTITY,
#         starlette.status.HTTP_422_UNPROCESSABLE_ENTITY,
#         starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
#     ]
    
#     for idx, input_param in enumerate(input_param_list):
#         response = await async_client.post("/tasks", json={"title": "테스트작업3", "due_date": input_param})
#         assert response.status_code == expectation_list[idx]

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_param, expectation",
    [
        ('2024-12-01', starlette.status.HTTP_200_OK),
        ('2024-12-32', starlette.status.HTTP_422_UNPROCESSABLE_ENTITY),
        ('2024/12/01', starlette.status.HTTP_422_UNPROCESSABLE_ENTITY),
        ('2024-1201', starlette.status.HTTP_422_UNPROCESSABLE_ENTITY),
    ]
)
async def test_due_date(input_param, expectation, async_client):
    response = await async_client.post("/tasks", json={"title": "테스트작업3", "due_date": input_param})
    assert response.status_code == expectation