from bokeh.models import Div
from bokeh.layouts import column
from bokeh.plotting import figure, output_file, save
from bokeh.models import BoxAnnotation

def plot_market_regime_to_html(filepath):
    import pandas as pd

    df = pd.read_excel(filepath, engine="openpyxl")
    df['date'] = pd.date_range(start='2022-01-01', periods=len(df), freq='B')

    regime_colors = {
        "bull": "lightgreen",
        "bear": "lightcoral",
        "sideways": "lightgray",
        "volatile": "khaki",
        "none": "white"
    }

    p = figure(title="Market Regime Zones with Price",
               x_axis_type="datetime", width=1200, height=500)

    # 가격 선
    p.line(df['date'], df['current price'], line_width=2, color='black', legend_label="Price")

    # 영역 색상
    start_idx = 0
    for i in range(1, len(df)):
        if df['market_regime'][i] != df['market_regime'][i-1] or i == len(df) - 1:
            regime = df['market_regime'][i-1]
            color = regime_colors.get(regime, 'white')
            p.add_layout(BoxAnnotation(left=df['date'][start_idx], right=df['date'][i],
                                       fill_color=color, fill_alpha=0.3))
            start_idx = i

    # ✅ HTML용 범례 수동 삽입
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
