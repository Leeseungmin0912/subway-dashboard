import pandas as pd


class SubwayDataProcessor:
    """API에서 가져온 실시간 도착 데이터를 Pandas로 가공하는 클래스"""

    def __init__(self, raw_data):
        # API에서 받은 원본 데이터(리스트 형태)를 Pandas 데이터프레임으로 변환
        self.raw_data = raw_data
        self.df = pd.DataFrame(raw_data)

    def process_data(self) -> pd.DataFrame:
        """필요한 컬럼만 추출하고 한글로 보기 좋게 정제합니다."""
        if self.df.empty:
            return pd.DataFrame()

        columns_to_keep = ['subwayId', 'trainLineNm', 'bstatnNm', 'arvlMsg2', 'arvlMsg3']
        existing_columns = [col for col in columns_to_keep if col in self.df.columns]
        df_filtered = self.df[existing_columns].copy()

        line_dict = {
            '1001': '1호선', '1002': '2호선', '1003': '3호선',
            '1004': '4호선', '1005': '5호선', '1006': '6호선',
            '1007': '7호선', '1008': '8호선', '1009': '9호선',
            '1075': '수인분당선', '1077': '신분당선', '1065': '공항철도'
        }

        # 코드를 실제 호선 이름으로 변환 (없는 코드는 '기타 호선'으로 처리)
        if 'subwayId' in df_filtered.columns:
            df_filtered['subwayId'] = df_filtered['subwayId'].map(line_dict).fillna('기타 호선')

        # 컬럼 이름 직관적으로 변경
        rename_dict = {
            'subwayId': '호선',
            'trainLineNm': '방면',
            'bstatnNm': '종착역',
            'arvlMsg2': '도착 정보',
            'arvlMsg3': '현재 위치'
        }
        df_cleaned = df_filtered.rename(columns=rename_dict)

        return df_cleaned

        # 데이터가 비어있는 경우 (막차 끊김 등) 에러 방지
        if self.df.empty:
            return pd.DataFrame()

        # 1. API 응답 중 우리가 대시보드에 띄울 핵심 컬럼만 선택
        # trainLineNm: 방면 (예: 성수행 - 교대방면)
        # bstatnNm: 종착역 (예: 성수)
        # arvlMsg2: 도착 메세지 (예: 2분 후 도착)
        # arvlMsg3: 현재 위치 (예: 역삼)
        columns_to_keep = ['trainLineNm', 'bstatnNm', 'arvlMsg2', 'arvlMsg3']

        # 만약 API 응답이 바뀌어 컬럼이 없을 경우를 대비한 안전한 필터링 (실무 팁!)
        existing_columns = [col for col in columns_to_keep if col in self.df.columns]
        df_filtered = self.df[existing_columns].copy()

        # 2. 컬럼 이름을 직관적인 한글로 변경
        rename_dict = {
            'trainLineNm': '방면',
            'bstatnNm': '종착역',
            'arvlMsg2': '도착 정보',
            'arvlMsg3': '현재 열차 위치'
        }
        df_cleaned = df_filtered.rename(columns=rename_dict)

        return df_cleaned


# ----------------- 테스트 실행 공간 -----------------
# api_client.py에서 데이터를 가져와서 여기서 가공이 잘 되는지 테스트합니다.
if __name__ == "__main__":
    from api_client import SubwayAPIClient

    # 1. 데이터 가져오기 (api_client 활용)
    client = SubwayAPIClient()
    target_station = "강남"
    print(f"[{target_station}역 데이터 호출 중...]")
    raw_data = client.get_arrival_info(target_station)

    # 2. 데이터 가공하기 (Pandas 활용)
    if raw_data:
        processor = SubwayDataProcessor(raw_data)
        processed_df = processor.process_data()

        print("\n✨ [Pandas로 예쁘게 가공된 데이터프레임] ✨")
        print(processed_df)
    else:
        print("처리할 데이터가 없습니다.")