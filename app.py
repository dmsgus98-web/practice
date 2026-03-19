import streamlit as st
import pandas as pd

st.set_page_config(page_title="출점 분석 대시보드", layout="wide")

st.title("📊 출점 의사결정 대시보드")

# ---------------------------
# 데이터 로드
# ---------------------------
@st.cache_data
def load_data():
    return pd.read_csv("location_data.csv")

df = load_data()

# ---------------------------
# 점수 계산 함수
# ---------------------------
def calculate_score(row):
    score = 0

    # 유동인구
    if row["foot_traffic"] >= 40000:
        score += 3
    elif row["foot_traffic"] >= 20000:
        score += 2
    else:
        score += 1

    # 예상 매출
    expected_sales = 495 * (row["foot_traffic"] / 10000)

    # ROI
    roi = expected_sales / row["rent"] if row["rent"] > 0 else 0

    if roi >= 0.5:
        score += 3
    elif roi >= 0.35:
        score += 2
    else:
        score += 1

    # 경쟁
    if row["competition"] <= 7:
        score += 3
    elif row["competition"] <= 12:
        score += 2
    else:
        score += 1

    # 배달
    if row["delivery_ratio"] >= 40:
        score += 1

    return score, expected_sales, roi


# ---------------------------
# 데이터 전처리
# ---------------------------
results = df.apply(lambda row: calculate_score(row), axis=1)
df[["score", "expected_sales", "roi"]] = pd.DataFrame(results.tolist(), index=df.index)

# 포트폴리오 분류
def classify(row):
    if row["location_type"] == "전통시장":
        return "수익형"
    elif row["location_type"] == "역세권":
        return "브랜드형"
    elif row["location_type"] == "유흥상권":
        return "매출형"
    elif row["location_type"] == "주거":
        return "안정형"
    else:
        return "실험형"

df["category"] = df.apply(classify, axis=1)

# ---------------------------
# 탭 구성
# ---------------------------
tab1, tab2, tab3 = st.tabs(["📍 개별 분석", "📊 전체 비교", "📦 포트폴리오"])

# ---------------------------
# 1. 개별 분석
# ---------------------------
with tab1:
    st.subheader("입지 선택")

    selected = st.selectbox("후보지 선택", df["name"])

    data = df[df["name"] == selected].iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("예상 일매출", f"{data['expected_sales']:,.0f}")
    col2.metric("ROI", f"{data['roi']:.2f}")
    col3.metric("점수", data["score"])

    st.write("### 📌 분석 요약")
    st.write(f"""
    - 유동인구: {data['foot_traffic']} → {'높음' if data['foot_traffic'] > 30000 else '보통'}
    - ROI: {data['roi']:.2f} → {'우수' if data['roi'] > 0.4 else '보통'}
    - 경쟁: {data['competition']} → {'과열' if data['competition'] > 10 else '안정'}
    """)

    st.write("### 🧠 추천 전략")
    st.write(f"👉 {data['category']} 전략 적용 필요")

# ---------------------------
# 2. 전체 비교
# ---------------------------
with tab2:
    st.subheader("전체 입지 비교")

    st.dataframe(df.sort_values("score", ascending=False), use_container_width=True)

    st.write("### 📈 점수 분포")
    st.bar_chart(df.set_index("name")["score"])

    st.write("### 💰 ROI vs 매출")
    st.scatter_chart(df[["expected_sales", "roi"]])

# ---------------------------
# 3. 포트폴리오 추천
# ---------------------------
with tab3:
    st.subheader("포트폴리오 추천")

    portfolio = df.sort_values("score", ascending=False).groupby("category").head(1)

    st.dataframe(portfolio, use_container_width=True)

    st.write("### 🎯 추천 구성")
    for _, row in portfolio.iterrows():
        st.write(f"""
        - {row['name']} ({row['category']})
        → 점수 {row['score']} / ROI {row['roi']:.2f}
        """)
