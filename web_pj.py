import streamlit as st
import re

# ====== 세션 상태 초기화 ======
if "started" not in st.session_state:
    st.session_state.started = False

# ====== 페이지 설정 ======
st.set_page_config(page_title="Digit Validator & RNG Tool", layout="centered")

# ====== 스타일 설정 ======
st.markdown("""
    <style>
    .example-text {
        font-size: 0.8em;
        color: #555;
        margin-top: -10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ====== 시작 안내 페이지 ======
st.title("숫자 처리 도구")

if not st.session_state.started:
    st.markdown("### 숫자 관련 도구들을 테스트해볼 수 있어요!")
    if st.button("테스트 시작"):
        st.session_state.started = True
    st.stop()

# ====== 입력 파싱 함수 ======
def parse_input(s):
    s = s.strip().replace('^', '**')
    try:
        value = eval(s, {"__builtins__": None}, {})
        if not isinstance(value, int):
            raise ValueError("Input is not an integer")
        return value
    except:
        raise ValueError("Invalid input format")

# ====== 선형 합동 생성기 ======
def linear_congruential_generator(seed, a, c, m, count):
    x = seed
    numbers = []
    for _ in range(count):
        x = (a * x + c) % m
        numbers.append(x)
    return numbers

# ====== ISBN-10 검사 ======
def validate_isbn10(isbn):
    isbn = isbn.replace("-", "").upper()
    if len(isbn) != 10:
        return False
    total = 0
    for i in range(9):
        if not isbn[i].isdigit():
            return False
        total += (i + 1) * int(isbn[i])
    last_char = isbn[9]
    if last_char == 'X':
        total += 10 * 10
    elif last_char.isdigit():
        total += 10 * int(last_char)
    else:
        return False
    return total % 11 == 0

# ====== ISBN-13 검사 ======
def validate_isbn13(isbn):
    isbn = isbn.replace("-", "")
    if len(isbn) != 13 or not isbn.isdigit():
        return False
    total = 0
    for i in range(12):
        digit = int(isbn[i])
        total += digit if i % 2 == 0 else digit * 3
    check_digit = (10 - (total % 10)) % 10
    return check_digit == int(isbn[-1])

# ====== 신용카드 검사 ======
def validate_credit_card(number):
    number = number.replace(" ", "")
    if len(number) < 12 or len(number) > 19:
        return False
    if not number.isdigit():
        return False
    digits = list(map(int, number[::-1]))
    total = 0
    for i, digit in enumerate(digits):
        if i % 2 == 1:
            doubled = digit * 2
            total += doubled - 9 if doubled > 9 else doubled
        else:
            total += digit
    return total % 10 == 0

# ====== 메인 콘텐츠 ======
st.title("📁Check Digit Validator & RNG Tool")
st.markdown("""
**Topic:** Check Digit Validator + Random Number Generator Tool  
**Description:**  
- Validate ISBN-10, ISBN-13, and credit card numbers using correct checksum algorithms.  
- Generate pseudorandom numbers using a Linear Congruential Generator.  
- User-friendly web GUI with instant feedback.  

**Team 3 - 이나경, 최현서, 김수아랑, 김혜진, 이현진**
""")

# ====== 탭 구성 ======
tabs = st.tabs(["LCG Generator", "ISBN-10", "ISBN-13", "Credit Card"])

# ====== LCG 탭 ======
with tabs[0]:
    st.subheader("Linear Congruential Generator")
    col1, col2 = st.columns(2)
    with col1:
        seed = st.text_input("Seed (x₀)")
        st.markdown('<div class="example-text">e.g. <b>7</b> (valid), <b>two</b> (invalid)</div>', unsafe_allow_html=True)
        a = st.text_input("Multiplier (a)")
        st.markdown('<div class="example-text">e.g. <b>5</b> (valid), <b>5.5</b> (invalid)</div>', unsafe_allow_html=True)
        c = st.text_input("Increment (c)")
        st.markdown('<div class="example-text">e.g. <b>3</b> (valid), <b>three</b> (invalid)</div>', unsafe_allow_html=True)
    with col2:
        m = st.text_input("Modulus (m)")
        st.markdown('<div class="example-text">e.g. <b>16</b> (valid), <b>-1</b> (invalid)</div>', unsafe_allow_html=True)
        count = st.text_input("How many numbers?")
        st.markdown('<div class="example-text">e.g. <b>10</b> (valid), <b>ten</b> (invalid)</div>', unsafe_allow_html=True)

    if st.button("Generate"):
        try:
            seed_val = parse_input(seed)
            a_val = parse_input(a)
            c_val = parse_input(c)
            m_val = parse_input(m)
            count_val = parse_input(count)
            result = linear_congruential_generator(seed_val, a_val, c_val, m_val, count_val)
            st.success("Generated Numbers:")
            st.code("\n".join(map(str, result)))
        except Exception as e:
            st.error(f"Invalid input: {e}")

# ====== ISBN-10 탭 ======
with tabs[1]:
    st.subheader("ISBN-10 Validator")
    isbn10 = st.text_input("Enter ISBN-10")
    st.markdown('<div class="example-text">e.g. <b>0306406152</b> (valid), <b>1234567890</b> (invalid)</div>', unsafe_allow_html=True)
    if st.button("Validate ISBN-10"):
        if validate_isbn10(isbn10):
            st.success("✅ Valid ISBN-10")
        else:
            st.error("❌ Invalid ISBN-10")

# ====== ISBN-13 탭 ======
with tabs[2]:
    st.subheader("ISBN-13 Validator")
    isbn13 = st.text_input("Enter ISBN-13")
    st.markdown('<div class="example-text">e.g. <b>9780306406157</b> (valid), <b>9781234567890</b> (invalid)</div>', unsafe_allow_html=True)
    if st.button("Validate ISBN-13"):
        if validate_isbn13(isbn13):
            st.success("✅ Valid ISBN-13")
        else:
            st.error("❌ Invalid ISBN-13")

# ====== 신용카드 탭 ======
with tabs[3]:
    st.subheader("Credit Card Validator")
    card = st.text_input("Enter credit card number")
    st.markdown('<div class="example-text">e.g. <b>4539 1488 0343 6467</b> (valid), <b>1234 5678 9012 3456</b> (invalid)</div>', unsafe_allow_html=True)
    if st.button("Validate Credit Card"):
        if validate_credit_card(card):
            st.success("✅ Valid credit card number")
        else:
            st.error("❌ Invalid credit card number")
