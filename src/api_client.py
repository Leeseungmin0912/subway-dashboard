import os
import requests
from dotenv import load_dotenv

# .env 파일 로드 (최상위 경로에 있는 환경변수를 불러옴)
load_dotenv()


class SubwayAPIClient:
    """서울시 지하철 실시간 도착 정보 API 클라이언트"""

    def __init__(self):
        # .env에서 키를 가져오되, 없으면 기본 제공되는 'sample' 키 사용
        self.api_key = os.getenv("SUBWAY_API_KEY", "sample")
        # URL 구조: base_url + 시작인덱스/종료인덱스/역이름
        self.base_url = f"http://swopenapi.seoul.go.kr/api/subway/{self.api_key}/json/realtimeStationArrival/0/50/"

    def get_arrival_info(self, station_name: str) -> list:
        """
        특정 역의 실시간 도착 정보를 요청합니다.
        :param station_name: 지하철역 이름 (예: '강남', '서울')
        :return: 열차 도착 정보 딕셔너리 리스트 (실패 시 빈 리스트 반환)
        """
        url = f"{self.base_url}{station_name}"

        try:
            response = requests.get(url, timeout=5)  # 5초 이상 지연되면 에러 처리 (실무 팁!)
            response.raise_for_status()  # 200 OK가 아니면 예외 발생

            data = response.json()

            # API 자체에서 내려주는 에러 메시지 검증
            if 'errorMessage' in data and data['errorMessage']['status'] != 200:
                error_msg = data['errorMessage']['message']
                print(f"API 에러: {error_msg}")
                return []

            # 성공 시 도착 데이터 리스트 반환
            return data.get('realtimeArrivalList', [])

        except requests.exceptions.Timeout:
            print("요청 시간 초과: 서버 응답이 너무 늦습니다.")
        except requests.exceptions.RequestException as e:
            print(f"네트워크 오류 발생: {e}")
        except ValueError:
            print("데이터 파싱 오류: JSON 형식이 아닙니다.")

        return []


# ----------------- 테스트 실행 공간 -----------------
# 이 파일만 단독으로 실행했을 때만 작동하는 영역입니다.
if __name__ == "__main__":
    client = SubwayAPIClient()
    target_station = "강남"

    print(f"[{target_station}역 실시간 도착 정보 요청 중...]\n")
    arrival_data = client.get_arrival_info(target_station)

    if arrival_data:
        for train in arrival_data:
            # trainLineNm: 방면 (예: 성수행 - 교대방면)
            # arvlMsg2: 도착 메세지 (예: 2분 후 도착)
            print(f"🚆 {train['trainLineNm']} | ⏳ {train['arvlMsg2']}")
    else:
        print("열차 정보가 없거나 에러가 발생했습니다.")