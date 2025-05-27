import streamlit as st

# 세션 상태 초기화
if "started" not in st.session_state:
    st.session_state.started = False

st.title("숫자 처리 도구")

# 아직 시작 안 했으면 시작 안내와 버튼만 보여줌
if not st.session_state.started:
    st.markdown("### 숫자 관련 도구들을 테스트해볼 수 있어요!")
    if st.button("테스트 시작"):
        st.session_state.started = True
    st.stop()  # 아래 코드 실행 안 되게 멈춤

# 메뉴 선택 (시작한 이후에만 보임)
menu = st.sidebar.selectbox("기능 선택", ["선형 합동 생성기", "ISBN-10 검증", "ISBN-13 검증", "신용카드 검증"])

# 함수들 정의
def linear_congruential_generator(seed, a, c, m, count):
    x = seed
    numbers = []
    for _ in range(count):
        x = (a * x + c) % m
        numbers.append(x)
    return numbers

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

# 메뉴별 동작
if menu == "선형 합동 생성기":
    seed = st.number_input("Seed (x₀)", value=1)
    a = st.number_input("Multiplier (a)", value=1103515245)
    c = st.number_input("Increment (c)", value=12345)
    m = st.number_input("Modulus (m)", value=2**31)
    count = st.number_input("Count", value=10, min_value=1, max_value=1000)

    if st.button("Generate"):
        try:
            numbers = linear_congruential_generator(seed, a, c, m, count)
            st.write(numbers)
        except Exception as e:
            st.error(f"입력 오류! {e}")

elif menu == "ISBN-10 검증":
    isbn10 = st.text_input("ISBN-10 입력")
    if st.button("검증"):
        if validate_isbn10(isbn10):
            st.success("✅ 유효한 ISBN-10입니다!")
        else:
            st.error("❌ 유효하지 않은 ISBN-10입니다!")

elif menu == "ISBN-13 검증":
    isbn13 = st.text_input("ISBN-13 입력")
    if st.button("검증"):
        if validate_isbn13(isbn13):
            st.success("✅ 유효한 ISBN-13입니다!")
        else:
            st.error("❌ 유효하지 않은 ISBN-13입니다!")

elif menu == "신용카드 검증":
    card = st.text_input("신용카드 번호 입력")
    if st.button("검증"):
        if validate_credit_card(card):
            st.success("✅ 유효한 신용카드 번호입니다!")
        else:
            st.error("❌ 유효하지 않은 신용카드 번호입니다!")
