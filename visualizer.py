from bokeh.models import Div, ColumnDataSource, HoverTool
from bokeh.layouts import column
from bokeh.plotting import figure, output_file, save
from bokeh.models import BoxAnnotation

def plot_market_regime_to_html(filepath):
    import pandas as pd

    df = pd.read_excel(filepath, engine="openpyxl")

    # ✅ 엑셀에서 제공하는 날짜 컬럼 사용
    df['date'] = pd.to_datetime(df['date'])
    df['date_str'] = df['date'].dt.strftime('%Y.%m.%d')  # 툴팁용 포맷

    regime_colors = {
        "bull": "lightgreen",
        "bear": "lightcoral",
        "sideways": "lightgray",
        "volatile": "khaki",
        "none": "white"
    }

    source = ColumnDataSource(df)

    p = figure(title="Market Regime Zones with Price",
               x_axis_type="datetime", width=1200, height=500)

    hover = HoverTool(
        tooltips=[
            ("📅 날짜", "@date_str"),
            ("💰 주가", "@{current price}{0,0.00}"),
            ("📈 시황", "@market_regime")
        ],
        mode='vline',
        point_policy='follow_mouse',
    )
    p.add_tools(hover)

    p.line('date', 'current price', line_width=2, color='black',
           legend_label="Price", source=source)

    # ✅ 수정된 음영 색칠 코드
    start_idx = 0
    for i in range(1, len(df)):
        # 시황이 바뀌면 이전 구간을 색칠
        if df['market_regime'][i] != df['market_regime'][i - 1]:
            regime = df['market_regime'][i - 1]
            color = regime_colors.get(regime, 'white')
            p.add_layout(BoxAnnotation(
                left=df['date'][start_idx],
                right=df['date'][i],
                fill_color=color,
                fill_alpha=0.3
            ))
            start_idx = i  # 새 시황 시작 위치 갱신

    # 마지막 구간도 색칠
    regime = df['market_regime'].iloc[-1]
    color = regime_colors.get(regime, 'white')
    p.add_layout(BoxAnnotation(
        left=df['date'][start_idx],
        right=df['date'].iloc[-1],
        fill_color=color,
        fill_alpha=0.3
    ))

    html_legend = Div(text="""
        <div style="font-size:14px; padding-bottom:10px;">
            <b>Market Regime Legend:</b><br>
            <span style="background-color: lightgreen; padding: 3px 10px;">Bull</span>
            <span style="background-color: lightcoral; padding: 3px 10px;">Bear</span>
            <span style="background-color: lightgray; padding: 3px 10px;">Sideways</span>
            <span style="background-color: khaki; padding: 3px 10px;">Volatile</span>
        </div>
    """)

    layout = column(html_legend, p)

    output_file("market_regime.html")
    save(layout)
