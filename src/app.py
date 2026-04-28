import streamlit as st
from api_client import SubwayAPIClient
from processor import SubwayDataProcessor

# 1. 웹 페이지 기본 설정
st.set_page_config(page_title="지하철 실시간 대시보드", page_icon="🚇", layout="wide")

st.title("🚇 실시간 지하철 도착 정보 대시보드")
st.markdown("**Python, Pandas, Streamlit**을 활용한 공공데이터 API 연동 포트폴리오입니다.")
st.markdown("---")

# 2. 사용자 입력 섹션 (UI 구성)
col1, col2 = st.columns([2, 1])

with col1:
    # 강남역으로 고정된 것을 풀고, 사용자가 직접 입력할 수 있게 만듭니다.
    # 1호선을 보고 싶다면 여기에 '서울', '부평', '종로3가' 등을 입력하면 됩니다.
    station_name = st.text_input("🔍 검색할 역 이름을 입력하세요 (예: 서울, 부평, 신도림)", value="서울")

with col2:
    st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
    search_button = st.button("도착 정보 조회", use_container_width=True)

# 3. 데이터 조회 및 화면 출력 로직
if search_button or station_name:
    with st.spinner(f"'{station_name}'역 데이터를 불러오는 중..."):

        # 백엔드: API 호출
        client = SubwayAPIClient()
        raw_data = client.get_arrival_info(station_name)

        if not raw_data:
            st.error("데이터를 불러오지 못했습니다. 역 이름을 다시 확인해주세요. (예: '서울역' 대신 '서울')")
        else:
            # 백엔드: Pandas 데이터 정제
            processor = SubwayDataProcessor(raw_data)
            df = processor.process_data()

            if df.empty:
                st.warning("현재 도착 예정인 열차가 없습니다.")
            else:
                st.success(f"✨ '{station_name}'역 실시간 도착 정보입니다!")

                # 💡 프론트엔드: 호선 필터링 기능 (1호선만 골라보기!)
                available_lines = df['호선'].unique().tolist()

                # 환승역일 경우 호선을 선택할 수 있는 필터 제공
                if len(available_lines) > 1:
                    selected_lines = st.multiselect("보려는 호선을 선택하세요:", available_lines, default=available_lines)
                    # 사용자가 선택한 호선만 데이터프레임에 남기기
                    display_df = df[df['호선'].isin(selected_lines)]
                else:
                    display_df = df

                # 최종 데이터 웹 화면에 표출
                st.dataframe(display_df, use_container_width=True, hide_index=True)