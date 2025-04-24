import pandas as pd
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, BoxAnnotation
from bokeh.palettes import Category20
import datetime

def plot_market_regime_to_html(filepath):
    df = pd.read_excel(filepath, engine="openpyxl")

    if 'current price' not in df.columns or 'market_regime' not in df.columns:
        raise ValueError("❗Required columns 'current price' and 'market_regime' not found.")

    df['date'] = pd.date_range(start='2022-01-01', periods=len(df), freq='B')  # 평일 기준 날짜 생성

    source = ColumnDataSource(df)

    # 색상 매핑
    regime_colors = {
        "bull": "lightgreen",
        "bear": "lightcoral",
        "sideways": "lightgray",
        "volatile": "khaki",
        "none": "white"
    }

    p = figure(title="Market Regime Zones with Price",
               x_axis_type="datetime", width=1200, height=500)
    
    p.line('date', 'current price', source=source, line_width=2, color='black', legend_label="Price")

    # 레짐 색상 음영 박스 추가
    start_idx = 0
    for i in range(1, len(df)):
        prev = df['market_regime'][i - 1]
        curr = df['market_regime'][i]
        if curr != prev or i == len(df) - 1:
            start_date = df['date'][start_idx]
            end_date = df['date'][i]
            color = regime_colors.get(prev, 'white')
            box = BoxAnnotation(left=start_date, right=end_date, fill_color=color, fill_alpha=0.3)
            p.add_layout(box)
            start_idx = i

    p.legend.location = "top_left"
    p.xaxis.axis_label = "Date"
    p.yaxis.axis_label = "Price"

    output_file("market_regime.html")
    save(p)
