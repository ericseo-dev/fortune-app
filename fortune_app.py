import os
from dotenv import load_dotenv
from anthropic import Anthropic
import streamlit as st
from datetime import datetime, date

load_dotenv()

client = Anthropic(
    base_url=os.getenv("ANTHROPIC_BASE_URL"),
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def ask_ai(prompt):
    res = client.messages.create(
        model="claude-haiku", max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return res.content[0].text

# 별자리 목록
ZODIAC_SIGNS = [
    "양자리 (3/21-4/19)",
    "황소자리 (4/20-5/20)",
    "쌍둥이자리 (5/21-6/20)",
    "게자리 (6/21-7/22)",
    "사자자리 (7/23-8/22)",
    "처녀자리 (8/23-9/22)",
    "천칭자리 (9/23-10/22)",
    "전갈자리 (10/23-11/21)",
    "궁수자리 (11/22-12/21)",
    "염소자리 (12/22-1/19)",
    "물병자리 (1/20-2/18)",
    "물고기자리 (2/19-3/20)"
]

st.set_page_config(page_title="운세 & 별자리 앱", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #ff6b6b;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .result-box {
        background-color: #fff8f8;
        border: 2px solid #ff6b6b;
        border-radius: 10px;
        padding: 1.5rem;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🔮 나의 운세 & 별자리 앱 🔮</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">당신의 오늘을 예측해보세요!</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("👤 이름", placeholder="예: 김철수")

with col2:
    birth_date = st.date_input("📅 생년월일", min_value=date(1950, 1, 1), max_value=date.today())

zodiac = st.selectbox(
    "♈ 별자리 선택",
    ["별자리를 선택해주세요"] + ZODIAC_SIGNS,
    index=0
)

col1, col2, col3 = st.columns(3)
with col2:
    get_fortune_button = st.button("✨ 운세 보기 ✨", use_container_width=True)

if get_fortune_button:
    if not name or not birth_date or zodiac == "별자리를 선택해주세요":
        st.warning("⚠️ 모든 정보를 입력해주세요!")
    else:
        birth_str = birth_date.strftime("%Y-%m-%d")

        with st.spinner("🔮 운세를 보는 중입니다..."):
            try:
                prompt = f"""당신은 재미있고 따뜻한 운세 전문가입니다.

사용자 정보:
- 이름: {name}
- 생년월일: {birth_str}
- 별자리: {zodiac}

오늘의 날짜: {datetime.now().strftime('%Y년 %m월 %d일')}

위 정보를 바탕으로 {name}님을 위한 오늘의 운세를 4-5줄로 작성해주세요.
운세는 밝고 친근한 말투로, 사용자가 재미있게 읽을 수 있도록 작성해주세요.
이모지도 적절히 섞어서 사용하세요!"""

                fortune = ask_ai(prompt)

                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown(f"### 📖 {name}님의 오늘 운세")
                st.markdown(fortune)
                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ 오류 발생: {str(e)}")

st.divider()
st.markdown("""
    <div style="text-align: center; color: #999; font-size: 0.9rem; margin-top: 2rem;">
    💫 매일 새로운 운세로 하루를 시작하세요! 💫
    </div>
""", unsafe_allow_html=True)