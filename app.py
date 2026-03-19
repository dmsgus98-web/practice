
import streamlit as st
import pandas as pd

st.set_page_config(page_title="출점 분석 앱", layout="wide")

st.title("📊 메가커피 출점 의사결정 앱 (Prototype)")

# ---------------------------
# 입력 영역
# ---------------------------
st.sidebar.header("입지 정보 입력")

foot_traffic = st.sidebar.number_input("유동인구 (명)", value=20000)
rent = st.sidebar.number_input("월세 (만원)", value=300)
competition = st.sidebar.slider("경쟁점수", 1, 20, 8)
delivery_ratio = st.sidebar.slider("배달 비중 (%)", 0, 100, 20)

location_type = st.sidebar.selectbox(
    "입지 유형",
    ["역세권", "전통시장", "유흥상권", "주거", "공원/기타"]
)

# ---------------------------
# 계산 로직 (핵심)
# ---------------------------
# 예상 매출 (간단 모델)
expected_sales = foot_traffic * 0.05  # 단순화된 가정

# ROI 계산
roi = expected_sales / rent if rent > 0 else 0

# 점수화
score = 0

# 유동인구
if foot_traffic >= 40000:
    score += 3
elif foot_traffic >= 20000:
    score += 2
else:
    score += 1

# ROI
if roi >= 0.5:
    score += 3
elif roi >= 0.35:
    score += 2
else:
    score += 1

# 경쟁
if competition <= 7:
    score += 3
elif competition <= 12:
    score += 2
else:
    score += 1

# ---------------------------
# 결과 출력
# ---------------------------
st.subheader("📌 분석 결과")

col1, col2, col3 = st.columns(3)

col1.metric("예상 일매출", f"{expected_sales:,.0f}")
col2.metric("ROI", f"{roi:.2f}")
col3.metric("종합 점수", score)

# ---------------------------
# 추천 로직
# ---------------------------
st.subheader("🧠 전략 추천")

if score >= 8:
    st.success("✅ 강력 추천 입지 (즉시 출점 검토)")
elif score >= 6:
    st.warning("⚠️ 조건부 추천 (전략 필요)")
else:
    st.error("❌ 비추천 입지")

# 입지별 전략
if location_type == "역세권":
    st.write("👉 브랜드 인지도 확보 전략 추천")
elif location_type == "전통시장":
    st.write("👉 저비용 고수익 운영 전략 추천")
elif location_type == "유흥상권":
    st.write("👉 야간 매출 극대화 전략")
elif location_type == "주거":
    st.write("👉 배달 중심 운영")
else:
    st.write("👉 감성형/브랜딩 전략")

# ---------------------------
# 확장 영역
# ---------------------------
st.subheader("📈 향후 확장 아이디어")

st.markdown("""
- 실제 CSV 데이터 연결
- 지도 기반 시각화
- Top5 자동 추천
- 배달 vs 홀 매출 시뮬레이션
""")
