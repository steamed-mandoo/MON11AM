import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import folium
import base64

# 데이터 불러오기
file = pd.read_csv('data/fin_file.csv', encoding='utf-8', header=0)

# 이미지 파일들을 Base64로 인코딩하여 딕셔너리에 저장
image_dict = {}
image_paths = ['data/강문해변.png', 'data/경포해변.png', 'data/아르떼뮤지엄강릉.png', 
               'data/낙산사.png', 'data/서피비치.png', 'data/안목해변.png', 
               'data/강릉중앙시장.png', 'data/휴휴암.png', 'data/하슬라아트월드.png', 
               'data/정동진.png', 'data/주문진항.png', 'data/양양전통시장.png', 
               'data/죽도해변.png', 'data/하조대전망대.png', 'data/하조대해변.png', 
               'data/범바우막국수.png', 'data/설악케이블카.png', 'data/청초수물회속초본점.png', 
               'data/영광정메밀국수.png', 'data/속초관광수산시장.png', 'data/오죽헌.png', 
               'data/테라로사커피공장강릉본점.png', 'data/강릉커피거리.png', 
               'data/경포아쿠아리움.png','data/차현희순두부청국장본점.png','data/송정해변.png',
               'data/엔드투앤드.png','data/엄지네포장마차본점.png','data/테라로사경포호수점.png',
               'data/순두부젤라또1호점.png','data/카페툇마루.png','data/갤러리밥스.png',
               'data/동화가든본점.png', 'data/정동진해변.png', 'data/감나무식당.png', 
               'data/곳.png', 'data/망상해수욕장.png','data/낙산해변.png', 
               'data/남애항.png', 'data/모래시계공원.png', 'data/순두부젤라또2호점.png', 
               'data/심곡항.png', 'data/아들바위공원.png', 'data/헌화로.png',
               'data/정동심곡바다부채길.png', 'data/주문진수산시장.png', 'data/주문진해변.png', 
               'data/큰기와집.png', 'data/파머스키친2호점.png', 'data/하조대.png', 
               ]

for path in image_paths:
    with open(path, 'rb') as img_file:
        encoded_image = base64.b64encode(img_file.read()).decode('utf-8')
        image_dict[path.split("/")[-1].split(".")[0]] = encoded_image  # 파일명을 키로 사용

# 대시보드 애플리케이션 생성
app = dash.Dash(__name__)

# 드롭다운 메뉴의 스타일 설정을 위한 딕셔너리
dropdown_style = {'width': '50%', 'color': '#000000', 'margin': '10px'}

# 지도 초기 설정
initial_map = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 여행 계획 탭 생성 함수
def travel_planner_tab():
    return dcc.Tab(label='여름여행 플래너', children=[
                html.H1("🥔여행코스 짜드립니다. 단돈 이찬원...~ᕕ( ᐛ )ᕗ"),
                html.Div([

                # 드롭다운 메뉴 생성 (다중 선택 가능)
                dcc.Dropdown(
                    id='region-dropdown',
                    options=[{'label': region, 'value': region} for region in file['region_nm'].unique()],
                    value=[],  # 기본값은 전체 지역
                    multi=True,
                    style={'width': '50%'},
                    placeholder='지역을 선택해주십시오.'  # 첫 번째 드롭다운 박스의 플레이스홀더
                ),

                # 비교 할 지역 선택 (강릉/양양) - 강릉과 양양의 geojson 파일 뽑아내서 분석 할 지역 위치 선정
                html.Div([
                    html.P("*비교 할 지역 선택 (강릉/양양) - 강릉과 양양의 geojson 파일 뽑아내서 분석 할 지역 위치 선정",
                           style={'color': 'blue', 'margin': '10px'})
                ], id='compare-region-comment-div'),  # 추가된 부분

                dcc.Dropdown(
                    id='age-dropdown',
                    options=[{'label': str(age), 'value': age} for age in file['age'].unique()],
                    value=[],  # 기본값은 전체 연령대
                    multi=True,
                    style={'width': '50%'},
                    placeholder='귀하의 연령대를 선택해주십시오.'  # 첫 번째 드롭다운 박스의 플레이스홀더
                ),

                # 실제 관광객 데이터 활용 - 연령대별로 방문객 분류 (MZ/X/상관없음)
                html.Div([
                    html.P("*실제 관광객 데이터 활용 - 연령대별로 방문객 분류 (MZ/X/상관없음)",
                           style={'color': 'blue', 'margin': '10px'})
                ], id='compare-age-comment-div'),  # 추가된 부분

                dcc.Dropdown(
                    id='type-dropdown',
                    options=[{'label': keyword, 'value': keyword} for keyword in file['type'].unique()],
                    value=[],  # 기본값은 전체 키워드
                    multi=True,
                    style={'width': '50%'},
                    placeholder='동행을 선택해주십시오.'  # 첫 번째 드롭다운 박스의 플레이스홀더
                ),

                # 방문객의 동행을 임의로 범주화하여 분류 (친구 또는 연인과/모두와/가족과)
                html.Div([
                    html.P("*방문객의 동행을 임의로 범주화하여 분류 (친구 또는 연인과/모두와/가족과)",
                           style={'color': 'blue', 'margin': '10px'})
                ], id='compare-type-comment-div'),  # 추가된 부분

                dcc.Dropdown(
                    id='activity-dropdown',
                    options=[{'label': keyword, 'value': keyword} for keyword in file['activity'].unique()],
                    value=[],  # 기본값은 전체 키워드
                    multi=True,
                    style={'width': '50%'},
                    placeholder='가장 선호하는 활동을 선택해주십시오.'  # 첫 번째 드롭다운 박스의 플레이스홀더
                ),

                # 실제 데이터 활용 - 관광객들이 하는 행동을 임의로 범주화 (맛집투어/해수욕/문화생활/.../)
                html.Div([
                    html.P("*실제 데이터 활용 - 관광객들이 하는 행동을 임의로 범주화 (맛집투어/해수욕/문화생활/.../)",
                           style={'color': 'blue', 'margin': '10px'})
                ], id='compare-activity-comment-div'),  # 추가된 부분

                # 버튼
                html.Button('검색', id='search-button', n_clicks=0),

                # 결과 출력용 엘리먼트
                html.Div([
                    html.P("선택된 중심관광지:"),
                    html.P(id='selected-center-output'),
                    html.P("연관된 관광지:"),
                    dcc.Textarea(id='related-places-output', value='', readOnly=True)
                ]),

                # 지도를 표시하는 Div
                html.Div([
                    html.Iframe(id='map-container', width='100%', height='600'),
                ])
            ]),
        ])
# 추가 기능 탭 생성 함수
def additional_features_tab():
    return dcc.Tab(label='추가 설명', children=[
        html.H1("Additional Features"),
        html.Div([
            html.P("데이터 출처:", style={'color': 'blue', 'margin': '10px'}),
            html.P("지방 인허가 로컬 데이터, 이동통신 데이터, 신용카드 데이터, 네비게이션 데이터, 관광객 방문 데이터 등의 다양한 데이터 소스를 활용하였습니다."),
            html.P("또한 한국 관광 데이터 랩과 구글 키워드 분석도 활용하였습니다."),
        ], style={'margin': '20px'}),

        html.Div([
            html.P("가설:", style={'color': 'blue', 'margin': '10px'}),
            html.P("강릉은 X세대들을 위한 고전적인 여름 휴양 관광지이고 양양은 MZ세대들을 위한 신생 여름 휴양 관광지이다. 실제로도 그럴까?"),
        ], style={'margin': '20px'}),

        html.Div([
            html.P("가설 확인 과정:", style={'color': 'blue', 'margin': '10px'}),
            html.P("1) 구글 키워드 분석을 통해 양양의 관심도가 2019년부터 상승하는 경향을 확인"),
            html.P("2) 이동통신 데이터, 신용카드 데이터, 네비게이션 데이터, 관광객 방문 데이터 등을 전처리하여 강릉과 양양 부분만 추출"),
            html.P("3) 이 데이터를 합쳐 각 지역별로 유명한 중심관광지를 12개로 도출했고 중심관광지에 대한 연관 관광지를 약 3~4개 정도로 도출"),
            html.P("4) 그 후 각 지방 인허가 로컬 데이터를 통해 좌표를 연계했고, 좌표가 없는 관광지는 google earth와 지오코딩을 통해 직접 좌표를 구해 표시"),
            html.P("5) 각 관광지에 대한 키워드를 주관적으로 고려하여 추출한 후 태그(#)를 통해 연령별, 일행별, 활동별 키워드를 만들어 각 중심관광지와 결합시켰습니다."),
            html.P("6) 드롭다운을 이용해 지도에 중심관광지를 중심으로 연관관광지가 표시될 수 있도록 코드를 구성했으며, 중심관광지와 연관관광지의 마커 색깔은 다르게 구성하여 구별하기 편리하게 했습니다."),
        ], style={'margin': '20px'}),

        html.Div([
            html.P("결론:", style={'color': 'blue', 'margin': '10px'}),
            html.P("결론적으로, 20대(MZ세대)와 40대(X세대)의 방문객들의 선호지가 엄격히 강릉 또는 양양으로 분류되지 않았습니다."),
            html.P("저희가 전처리 한 자료를 통해 양양과 강릉 두 지역 모두 다양한 연령층과 일행의 관광객들이 많이 방문하고 있음을 확인할 수 있었습니다."),
            html.P("또한, 관광지에서 선호하는 활동 또한 다양하게 나타났음을 확인 할 수 있었습니다."),
            html.P("특히, 강릉을 전통적인 관광지로 여기거나 양양을 신생 관광지로 간주하는 편견은 일부 존재 하지만 데이터 분석 결과 이는 일반적으로 성립되지 않는다는 결론을 도출하였습니다."),
            html.P("따라서 초기에 세운 가설과 완전히 맞는 결과는 아니지만 어느정도 유사한 결과를 갖는다는 사실을 도출해 낼 수 있었습니다."),
        ], style={'margin': '20px'}),

        html.Div([
            html.P("P.S.: 데이터 처리 속도가 느립니다.. 조금만 기다리면 뜨니까 기다려주세요!"),
        ], style={'margin': '20px'}),
    ])
                

# 앱 레이아웃 구성
app.layout = html.Div([
    dcc.Tabs([
        travel_planner_tab(),
        additional_features_tab()
    ])
])

# 콜백 함수 정의
@app.callback(
    [
        Output('selected-center-output', 'children'),
        Output('related-places-output', 'value'),
        Output('map-container', 'srcDoc')  # 추가된 부분
    ],
    [Input('search-button', 'n_clicks')],
    [Input('region-dropdown', 'value'),
     Input('age-dropdown', 'value'),
     Input('type-dropdown', 'value'),
     Input('activity-dropdown', 'value')]
)
def update_result(n_clicks, selected_regions, selected_ages, selected_types, selected_activities):
    # 버튼이 클릭되었을 때만 실행
    if n_clicks % 2 == 1:
        # 선택된 값에 따라 데이터 필터링
        filtered_data = file[(file['region_nm'].isin(selected_regions)) &
                             (file['age'].isin(selected_ages)) &
                             (file['type'].isin(selected_types)) &
                             (file['activity'].isin(selected_activities))]
        
        if not filtered_data.empty:
            selected_center = filtered_data.iloc[0]['cent_nm']
            related_places = file[file['cent_nm'] == selected_center]['related_nm'].unique()
            related_places_str = ', '.join(related_places)
            
            # 중심 관광지와 연관된 지도 표시
            map_obj = folium.Map(location=[filtered_data.iloc[0]['cent_y'], filtered_data.iloc[0]['cent_x']], zoom_start=12)
            
            # 중심 광지 마커 추가
            add_marker(map_obj, filtered_data.iloc[0]['cent_y'], filtered_data.iloc[0]['cent_x'],
                       filtered_data.iloc[0]['cent_nm'], filtered_data.iloc[0]['activity'], central=True, popup=True, image=image_dict.get(filtered_data.iloc[0]['cent_nm'], None))

            # 연관 광지 마커 추가
            for _, row in filtered_data.iterrows():
                add_marker(map_obj, row['related_y'], row['related_x'], row['related_nm'], row['text'], central=False, popup=True, image=image_dict.get(row['related_nm'], None))

            # HTML 코드로 변환하여 반환
            map_html = map_obj._repr_html_()

            return selected_center, related_places_str, map_html
        else:
            # No selected places, return '엥'
            return '엥?٩( ᐛ )', '', ''
    else:
        # Return empty values for all outputs if the button is not clicked
        return '', '', ''

# 마커를 추가하는 함수
def add_marker(map_obj, lat, lon, title, text, central=False, popup=False, image=None):
    if central:
        marker_color = 'blue'
    else:
        marker_color = 'green'

    marker = folium.Marker([lat, lon], popup=f"{title}\n{text}", icon=folium.Icon(color=marker_color, icon='info-sign'))
    marker.add_to(map_obj)

    if popup and image:
        # 이미지를 Base64로 디코딩하여 팝업에 추가
        decoded_image = base64.b64decode(image)
        
        # 팝업에 이미지 추가
        encoded_image = base64.b64encode(decoded_image).decode('utf-8')
        image_tag = f'<img src="data:image/png;base64,{encoded_image}" style="width:100%;height:100%;">'
        popup_html = f'{title}\n{text}<br>{image_tag}'
        
        popup = folium.Popup(popup_html, max_width=300)
        marker.add_child(popup)

# 애플리케이션 실행
if __name__ == '__main__':
    app.run_server(debug=True, port=8096)
