# 🚇 서울시 실시간 지하철 도착 정보 대시보드

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

서울열린데이터광장의 OpenAPI를 활용하여 특정 역의 실시간 열차 도착 정보를 한눈에 확인할 수 있는 웹 대시보드입니다. 

## 🚀 주요 기능
- **실시간 도착 정보 조회:** 서울시 내 모든 지하철역의 실시간 상/하행 열차 위치 데이터 시각화
- **멀티 호선 필터링:** 환승역 검색 시 사용자가 원하는 호선만 선택해서 볼 수 있는 기능 (Pandas 활용)
- **반응형 UI:** Streamlit을 활용하여 검색창과 결과 화면을 깔끔하게 구성

## 🛠️ 기술적 해결 과제 (Troubleshooting)
- **데이터 누락 이슈 해결:** 서울역과 같은 대형 환승역에서 특정 호선(4호선 등)이 표시되지 않던 문제를 분석하여, API 호출 범위를 확대(5개 -> 50개)함으로써 데이터 완전성 확보
- **보안 가이드 준수:** API Key와 같은 민감 정보를 코드에 직접 노출하지 않고, `.env` 및 `Streamlit Secrets`를 활용하여 환경 변수 방식으로 안전하게 관리
- **UI 정렬 개선:** 텍스트 입력창과 버튼의 높이가 맞지 않는 Streamlit의 기본 레이아웃 문제를 CSS 마진 조절을 통해 정밀하게 수정

## 📂 프로젝트 구조
- `src/app.py`: 웹 대시보드 메인 UI 및 인터랙션 로직
- `src/api_client.py`: 지하철 API 호출 및 JSON 데이터 수집
- `src/processor.py`: 수집된 데이터를 Pandas 데이터프레임으로 변환 및 가공
- `.gitignore`: 보안을 위해 민감한 설정 파일(`.env`, `.idea/`)을 관리 대상에서 제외

## 💻 실행 방법
1. 저장소 클론: `git clone https://github.com/Leeseungmin0912/subway-dashboard.git`
2. 패키지 설치: `pip install -r requirements.txt`
3. 실행: `streamlit run src/app.py`
혹은 https://subway-arrived-nanfu.streamlit.app/ ( 2026.04.28 서비스 중)