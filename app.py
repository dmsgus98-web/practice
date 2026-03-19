import streamlit as st

st.set_page_config(page_title="출점 분석 앱", layout="wide")

st.title("📊 출점 의사결정 엔진 (v1)")

# ---------------------------
# 입력
# ---------------------------
st.sidebar.header("입지 정보 입력")

foot_traffic = st.sidebar.number_input("유동인구", value=20000)
rent = st.sidebar.number_input("월세", value=300)
competition = st.sidebar.slider("경쟁점수", 1, 20, 8)
delivery_ratio = st.sidebar.slider("배달 비중 (%)", 0, 100, 20)

location_type = st.sidebar.selectbox(
    "입지 유형",
    ["역세권", "전통시장", "유흥상권", "주거", "공원/기타"]
)

# ---------------------------
# 1. 매출 모델 (보고서 반영)
# ---------------------------
expected_sales = 495 * (foot_traffic / 10000)

# ---------------------------
# 2. 입지 유형 보정 (핵심)
# ---------------------------
if location_type == "전통시장":
    rent *= 0.8   # 임대 효율 좋음
elif location_type == "역세권":
    competition += 2
elif location_type == "유흥상권":
    expected_sales *= 1.2
elif location_type == "주거":
    delivery_ratio += 10

# ---------------------------
# 3. ROI
# ---------------------------
roi = expected_sales / rent if rent > 0 else 0

# ---------------------------
# 4. 점수 계산
# ---------------------------
score = 0

# 유동
score += 3 if foot_traffic >= 40000 else 2 if foot_traffic >= 20000 else 1

# ROI
score += 3 if roi >= 0.5 else 2 if roi >= 0.35 else 1

# 경쟁
score += 3 if competition <= 7 else 2 if competition <= 12 else 1

# 배달 보정
if delivery_ratio >= 40:
    score += 1

# ---------------------------
# 5. 포트폴리오 분류 (핵심)
# ---------------------------
if location_type == "전통시장":
    category = "수익형"
elif location_type == "역세권":
    category = "브랜드형"
elif location_type == "유흥상권":
    category = "매출형"
elif location_type == "주거":
    category = "안정형"
else:
    category = "실험형"

# ---------------------------
# 6. 결과 출력
# ---------------------------
st.subheader("📌 핵심 지표")

col1, col2, col3 = st.columns(3)
col1.metric("예상 일매출", f"{expected_sales:,.0f}")
col2.metric("ROI", f"{roi:.2f}")
col3.metric("포트폴리오", category)

# ---------------------------
# 7. 의사결정 로직 (차별화 포인트)
# ---------------------------
st.subheader("🧠 최종 판단")

decision = ""

if category == "수익형":
    if roi >= 0.45:
        decision = "✅ 즉시 출점 (수익형 핵심 입지)"
    else:
        decision = "⚠️ 보류 (수익성 부족)"

elif category == "브랜드형":
    if foot_traffic >= 35000:
        decision = "✅ 출점 (브랜드 확보 목적)"
    else:
        decision = "❌ 비추천 (유동 부족)"

elif category == "매출형":
    if expected_sales >= 1800:
        decision = "✅ 공격적 출점 (고매출 가능)"
    else:
        decision = "⚠️ 경쟁 대비 매출 부족"

elif category == "안정형":
    if delivery_ratio >= 35:
        decision = "✅ 안정 출점 (배달 기반 확보)"
    else:
        decision = "⚠️ 배달 전략 필요"

else:
    decision = "⚠️ 테스트 입지 (파일럿 운영 권장)"

st.write(decision)

# ---------------------------
# 8. 전략 제안
# ---------------------------
st.subheader("📊 운영 전략")

if category == "수익형":
    st.write("👉 저가 회전율 극대화 / 인건비 최소화")
elif category == "브랜드형":
    st.write("👉 대형 간판 / 노출 극대화 / 구독모델")
elif category == "매출형":
    st.write("👉 야간 운영 / 디저트 크로스셀")
elif category == "안정형":
    st.write("👉 배달 최적화 / 단골 확보")
else:
    st.write("👉 팝업 / 테스트 전략")
