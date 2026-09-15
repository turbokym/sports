import os
import json
import urllib.request

SUPABASE_URL = os.environ.get("SUPABASE_URL")
# 데이터 수정/삭제 권한이 있는 service_role 키를 사용합니다.
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

def upsert_supabase(table_name, payload):
    url = f"{SUPABASE_URL}/rest/v1/{table_name}"
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates" # 중복 시 갱신(UPSERT)
    }
    
    data_bytes = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req) as response:
            print(f"[{table_name}] 동기화 성공: {response.status}")
    except Exception as e:
        print(f"[{table_name}] 동기화 실패:", e)

# 최신 구단 데이터 갱신 샘플 (승격/강등/팀명 변경 반영)
latest_teams = [
    {"id": 1, "league_id": 1, "name": "울산 HD FC", "stadium": "울산문수축구경기장", "founded_year": 1983},
    {"id": 2, "league_id": 1, "name": "포항 스틸러스", "stadium": "포항스틸야드", "founded_year": 1973},
    # 변경되거나 추가된 팀 정보를 이 배열로 수집하여 보내게 됩니다.
]

if __name__ == "__main__":
    upsert_supabase("teams", latest_teams)
