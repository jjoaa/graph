from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from plotly.offline import plot


app = Flask(__name__)

file_path = '8 의료용_마약류_효능별·성분별_처방_현황.csv'
df = pd.read_csv(file_path, encoding='cp949')

# 그래프용 설정
years = ['2019.4', '2020.4', '2021.4', '2022.4', '2023.4']
target_categories = [
    "진통제", "항불안제", "최면진정제", "마취제",
    "식욕억제제", "진해제", "항뇌전증제", "ADHD치료제", "항우울제"
]

# 🔹 메인 페이지: 막대그래프
@app.route('/')
def index():
    # 필터 및 처리
    mask = (df['효능및성분별(1)'].isin(target_categories)) & (df['효능및성분별(3)'] == '소계')
    df_summary = df[mask].copy()
    df_summary[years] = df_summary[years].replace('-', 0).astype(float)
    summary = df_summary.groupby('효능및성분별(1)')[years].sum().reset_index()

    fig = go.Figure()
    for _, row in summary.iterrows():
        fig.add_trace(go.Bar(
            x=years,
            y=row[years],
            name=row['효능및성분별(1)']
        ))

    fig.update_layout(
        barmode='stack',
        title=' ',
        xaxis_title='연도',
        yaxis_title='처방량',
        yaxis=dict(
            tickvals=[0, 1e9, 2e9, 3e9, 4e9],
            ticktext=['0억', '10억', '20억', '30억', '40억'],
            tickformat=",.0f",
        ),
        height=600
    )

    plot_html = pio.to_html(fig, full_html=False)
    return render_template('index.html', plot_html=plot_html)

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
from matplotlib.ticker import MaxNLocator, FuncFormatter

# 🔹 연령별 분석: 나이 그래프
@app.route('/', methods=["GET", "POST"])
def age():
   
    year = request.form.get('year', '2023')  
    plot_img_path = None

    if year:
      plot_img_path = generate_plot_for_year(year)
     return render_template('index.html', plot_img_path=plot_img_path, year=year)

def generate_plot_for_year(year):
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False 
    
    file_path = '7 환자_연령대별_의료용_마약류_처방_현황.csv'
    df = pd.read_csv(file_path, encoding='cp949')
    df_clean = df.drop(index=0)  
    df_year = df_clean[['성별(1)', '연령대별(1)', year, f'{year}.4']].copy()
    df_year = df_year[df_year['연령대별(1)'] != '소계']
    df_year[year] = pd.to_numeric(df_year[year].str.replace(',', '', regex=False), errors='coerce')
    df_year[f'{year}.4'] = pd.to_numeric(df_year[f'{year}.4'].str.replace(',', '', regex=False), errors='coerce')
    df_year[year] = df_year[year].fillna(0).astype(int)
    df_year[f'{year}.4'] = df_year[f'{year}.4'].fillna(0).astype(int)
    male_data = df_year[df_year['성별(1)'] == '남자']
    female_data = df_year[df_year['성별(1)'] == '여자']
    age_order = male_data['연령대별(1)'].tolist()
    male_data = male_data.set_index('연령대별(1)').loc[age_order]
    female_data = female_data.set_index('연령대별(1)').loc[age_order]
    
    x = range(len(age_order))
    bar_width = 0.2
    fig, ax1 = plt.subplots(figsize=(16, 8))
    ax2 = ax1.twinx()  # 오른쪽 y축
    ax1.bar([i - 1.5*bar_width for i in x], male_data[year], width=bar_width, label=f'남자 환자수 ', color='skyblue')
    ax1.bar([i + 0.5*bar_width for i in x], female_data[year], width=bar_width, label=f'여자 환자수 ', color='lightpink')
    ax1.set_ylabel('환자수 (명)')
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))

    ax2.bar([i - 0.5*bar_width for i in x], male_data[f'{year}.4'], width=bar_width, label=f'남자 처방량 ', color='green', alpha=0.7)
    ax2.bar([i + 1.5*bar_width for i in x], female_data[f'{year}.4'], width=bar_width, label=f'여자 처방량', color='orange', alpha=0.7)
    ax2.set_ylabel('처방량 (개/정)')
    ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x/1e8:.2f}억'))
    ax1.set_xticks(x)
    ax1.set_xticklabels(age_order, rotation=45)
    ax1.set_xlabel('연령대')
    ax1.grid(axis='y', linestyle='--', alpha=0.5)

    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

    plt.title(f'{year}년 연령대별 성별 의료용 마약류 환자수 및 처방량', fontsize=18)
    plt.tight_layout()
    plt.savefig(f'static/age_plot_{year}.png') 
    plt.close() 
    return f'age_plot_{year}.png'



# 🔹 파이 차트 페이지
@app.route('/pie_chart')
def pie_chart():
    year = request.args.get('year')
    ingredient = request.args.get('ingredient')
    return render_template('pie_chart.html', year=year, ingredient=ingredient)

@app.route('/get_pie_data')
def get_pie_data():
    year = request.args.get('year')
    ingredient = request.args.get('ingredient')

    drug_data = df[(df['효능및성분별(1)'] == ingredient) & (df['효능및성분별(3)'] != '소계')].copy()
    drug_data[year + '.4'] = pd.to_numeric(drug_data[year + '.4'].replace('-', 0), errors='coerce').fillna(0)

    if drug_data[year + '.4'].sum() == 0:
        return jsonify({'labels': [], 'values': []})

    total = drug_data[year + '.4'].sum()
    drug_data = drug_data[drug_data[year + '.4'] / total * 100 > 1.0]

    labels = drug_data['효능및성분별(3)'].tolist()
    values = drug_data[year + '.4'].tolist()

    return jsonify({'labels': labels, 'values': values})


# 🔹 산점도
@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/get_scatter_data')
def get_scatter_data():
    year = request.args.get('year')
    category = request.args.get('category')
    
    # CSV 이중 헤더 처리
    df_multi = pd.read_csv(file_path, header=[0, 1], encoding='cp949')
    df_multi.columns = ['_'.join(col).strip() for col in df_multi.columns.values]

    dose_col = f'{year}_처방량 (개/정)'
    patient_col = f'{year}_환자수 (명)'

    filtered = df_multi[
        (df_multi['효능및성분별(1)_효능및성분별(1)'] == category) &
        (df_multi['효능및성분별(3)_효능및성분별(3)'] != '소계')
    ].copy()

    filtered[dose_col] = pd.to_numeric(filtered[dose_col].replace('-', 0), errors='coerce').fillna(0)
    filtered[patient_col] = pd.to_numeric(filtered[patient_col].replace('-', 0), errors='coerce').fillna(0)

    filtered['평균 처방량'] = filtered[dose_col] / filtered[patient_col]
    filtered = filtered[(filtered[dose_col] > 0) & (filtered[patient_col] > 0)]

    scatter_data = [{
        'x': filtered[patient_col].tolist(),
        'y': filtered[dose_col].tolist(),
        'text': [
            f"{row['효능및성분별(3)_효능및성분별(3)']}<br>환자수: {int(row[patient_col])}명<br>처방량: {int(row[dose_col])}개<br>1인당: {row['평균 처방량']:.2f}개"
            for _, row in filtered.iterrows()
        ],
        'mode': 'markers',
        'type': 'scatter',
        'marker': {
            'size': 14,
            'color': filtered['평균 처방량'].tolist(),
            'colorscale': 'Viridis',
            'showscale': True,
            'colorbar': {'title': '1인당 평균 처방량'}
        },
        'hoverinfo': 'text'
    }]

    return jsonify(scatter_data)


if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

