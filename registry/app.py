from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

# 여기에 Docker Registry 주소를 입력
REGISTRY_URL = "http://10.0.100.208:5000"

@app.get("/")
def root():
    return {"message": "Docker Registry API"}

@app.get("/images")
def list_images():
    """
    전체 저장소(repository) 목록을 가져온다.
    """
    try:
        response = requests.get(f"{REGISTRY_URL}/v2/_catalog")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/images/{repo}/tags")
def list_tags(repo: str):
    """
    특정 이미지(repository)의 태그 목록을 가져온다.
    """
    try:
        response = requests.get(f"{REGISTRY_URL}/v2/{repo}/tags/list")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/all")
def get_all_images_with_tags():
    """
    모든 이미지와 각 이미지의 태그 목록을 반환한다.
    """
    try:
        result = {}
        catalog = requests.get(f"{REGISTRY_URL}/v2/_catalog").json()
        for repo in catalog.get("repositories", []):
            tags = requests.get(f"{REGISTRY_URL}/v2/{repo}/tags/list").json()
            result[repo] = tags.get("tags", [])
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})