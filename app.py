import streamlit as st
import pandas as pd

st.set_page_config(page_title="출점 분석 대시보드", layout="wide")

st.title("📊 출점 의사결정 대시보드 (Final)")

# ---------------------------
# 데이터 로드
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("location_data.csv")
    df = df.fillna(0)
    return df

df = load_data()

# ---------------------------
# 계산 함수
# ---------------------------
def calculate(row):
    expected_sales = 495 * (row["foot_traffic"] / 10000)
    roi = expected_sales / row["rent"] if row["rent"] > 0 else 0

    score = 0

    # 유동
    score += 3 if row["foot_traffic"] >= 40000 else 2 if row["foot_traffic"] >= 20000 else 1

    # ROI
    score += 3 if roi >= 0.5 else 2 if roi >= 0.35 else 1

    # 경쟁
    score += 3 if row["competition"] <= 7 else 2 if row["competition"] <= 12 else 1

    # 배달
    if row["delivery_ratio"] >= 40:
        score += 1

    return pd.Series([expected_sales, roi, score])

df[["expected_sales", "roi", "score"]] = df.apply(calculate, axis=1)

# ---------------------------
# 포트폴리오 분류
# ---------------------------
def classify(x):
    if x == "전통시장":
        return "수익형"
    elif x == "역세권":
        return "브랜드형"
    elif x == "유흥상권":
        return "매출형"
    elif x == "주거":
        return "안정형"
    else:
        return "실험형"

df["category"] = df["location_type"].apply(classify)

# ---------------------------
# 탭 구성
# ---------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["📍 개별 분석", "📊 전체 비교", "🏆 TOP5 추천", "📦 포트폴리오"]
)

# ---------------------------
# 1. 개별 분석
# ---------------------------
with tab1:
    st.subheader("입지 선택")

    selected = st.selectbox("후보지", df["name"])
    data = df[df["name"] == selected].iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("예상 일매출", f"{data['expected_sales']:,.0f}")
    col2.metric("ROI", f"{data['roi']:.2f}")
    col3.metric("점수", int(data["score"]))

    st.write("### 📌 분석 리포트")
    st.write(f"""
    - 유동인구: {data['foot_traffic']} → {'높음' if data['foot_traffic'] > 30000 else '보통'}
    - ROI: {data['roi']:.2f} → {'우수' if data['roi'] > 0.4 else '보통'}
    - 경쟁: {data['competition']} → {'과열' if data['competition'] > 10 else '안정'}
    - 유형: {data['category']}
    """)

# ---------------------------
# 2. 전체 비교
# ---------------------------
with tab2:
    st.subheader("전체 입지 비교")

    st.dataframe(
        df.sort_values("score", ascending=False),
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.write("### 점수 분포")
        st.bar_chart(df.set_index("name")["score"])

    with col2:
        st.write("### ROI vs 매출")
        st.scatter_chart(df[["expected_sales", "roi"]])

# ---------------------------
# 3. TOP5 추천
# ---------------------------
with tab3:
    st.subheader("🏆 TOP 5 입지")

    top5 = df.sort_values("score", ascending=False).head(5)

    st.dataframe(top5, use_container_width=True)

    st.write("### 🎯 추천 이유")
    for _, row in top5.iterrows():
        st.write(f"""
        **{row['name']}**
        - 점수: {row['score']}
        - ROI: {row['roi']:.2f}
        - 유형: {row['category']}
        """)

# ---------------------------
# 4. 포트폴리오 추천
# ---------------------------
with tab4:
    st.subheader("📦 최적 포트폴리오")

    portfolio = df.sort_values("score", ascending=False).groupby("category").head(1)

    st.dataframe(portfolio, use_container_width=True)

    st.write("### 📌 구성 전략")

    for _, row in portfolio.iterrows():
        st.write(f"""
        - {row['name']} ({row['category']})
        → 점수 {row['score']} / ROI {row['roi']:.2f}
        """)
