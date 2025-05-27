
import tkinter as tk
from tkinter import ttk, messagebox

# ====== 입력 파싱 함수 ======
def parse_input(s):
    s = s.strip().replace('^', '**')
    try:
        value = eval(s, {"__builtins__":None}, {})
        if not isinstance(value, int):
            raise ValueError("Input is not an integer")
        return value
    except:
        raise ValueError("Invalid input format")

# ====== 선형 합동 생성기 함수 ======
def linear_congruential_generator(seed, a, c, m, count):
    x = seed
    numbers = []
    for _ in range(count):
        x = (a * x + c) % m
        numbers.append(x)
    return numbers

# ====== ISBN-10 검증 ======
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

# ====== ISBN-13 검증 ======
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

# ====== 신용카드 검증 (Luhn) ======
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

# ====== GUI 함수들 ======

def run_lcg():
    try:
        seed = parse_input(seed_entry.get())
        a = parse_input(a_entry.get())
        c = parse_input(c_entry.get())
        m = parse_input(m_entry.get())
        count = parse_input(count_entry.get())
        numbers = linear_congruential_generator(seed, a, c, m, count)
        lcg_result.delete(1.0, tk.END)
        for i, num in enumerate(numbers, 1):
            lcg_result.insert(tk.END, f"{i}: {num}\n")
    except Exception as e:
        messagebox.showerror("Input Error", f"입력 오류! {e}")

def run_isbn10():
    isbn = isbn10_entry.get()
    if validate_isbn10(isbn):
        isbn10_result.config(text="✅ 유효한 ISBN-10입니다!")
    else:
        isbn10_result.config(text="❌ 유효하지 않은 ISBN-10입니다!")

def run_isbn13():
    isbn = isbn13_entry.get()
    if validate_isbn13(isbn):
        isbn13_result.config(text="✅ 유효한 ISBN-13입니다!")
    else:
        isbn13_result.config(text="❌ 유효하지 않은 ISBN-13입니다!")

def run_credit_card():
    card = credit_entry.get()
    if validate_credit_card(card):
        credit_result.config(text="✅ 유효한 신용카드 번호입니다!")
    else:
        credit_result.config(text="❌ 유효하지 않은 신용카드 번호입니다!")

# ====== 메인 윈도우 ======

root = tk.Tk()
root.title("Check Digit Validator + Linear Congruential Generator Tool")
root.geometry("450x400")

tab_control = ttk.Notebook(root)

# 1) LCG 탭
tab_lcg = ttk.Frame(tab_control)
tab_control.add(tab_lcg, text="선형 합동 생성기")

labels_lcg = ["Seed (x₀):", "Multiplier (a):", "Increment (c):", "Modulus (m):", "Count:"]
seed_entry = a_entry = c_entry = m_entry = count_entry = None
entries = []

for i, text in enumerate(labels_lcg):
    ttk.Label(tab_lcg, text=text).grid(row=i, column=0, sticky="e", padx=5, pady=3)
    entry = ttk.Entry(tab_lcg, width=20)
    entry.grid(row=i, column=1, padx=5, pady=3)
    entries.append(entry)

seed_entry, a_entry, c_entry, m_entry, count_entry = entries

generate_btn = ttk.Button(tab_lcg, text="Generate", command=run_lcg)
generate_btn.grid(row=5, column=0, columnspan=2, pady=10)

lcg_result = tk.Text(tab_lcg, height=10, width=40)
lcg_result.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

# 2) ISBN-10 탭
tab_isbn10 = ttk.Frame(tab_control)
tab_control.add(tab_isbn10, text="ISBN-10 검증")

ttk.Label(tab_isbn10, text="ISBN-10 입력:").grid(row=0, column=0, sticky="e", padx=5, pady=10)
isbn10_entry = ttk.Entry(tab_isbn10, width=30)
isbn10_entry.grid(row=0, column=1, padx=5, pady=10)
isbn10_btn = ttk.Button(tab_isbn10, text="검증", command=run_isbn10)
isbn10_btn.grid(row=1, column=0, columnspan=2, pady=5)
isbn10_result = ttk.Label(tab_isbn10, text="")
isbn10_result.grid(row=2, column=0, columnspan=2, pady=5)

# 3) ISBN-13 탭
tab_isbn13 = ttk.Frame(tab_control)
tab_control.add(tab_isbn13, text="ISBN-13 검증")

ttk.Label(tab_isbn13, text="ISBN-13 입력:").grid(row=0, column=0, sticky="e", padx=5, pady=10)
isbn13_entry = ttk.Entry(tab_isbn13, width=30)
isbn13_entry.grid(row=0, column=1, padx=5, pady=10)
isbn13_btn = ttk.Button(tab_isbn13, text="검증", command=run_isbn13)
isbn13_btn.grid(row=1, column=0, columnspan=2, pady=5)
isbn13_result = ttk.Label(tab_isbn13, text="")
isbn13_result.grid(row=2, column=0, columnspan=2, pady=5)

# 4) 신용카드 검증 탭
tab_credit = ttk.Frame(tab_control)
tab_control.add(tab_credit, text="신용카드 검증")

ttk.Label(tab_credit, text="신용카드 번호 입력:").grid(row=0, column=0, sticky="e", padx=5, pady=10)
credit_entry = ttk.Entry(tab_credit, width=30)
credit_entry.grid(row=0, column=1, padx=5, pady=10)
credit_btn = ttk.Button(tab_credit, text="검증", command=run_credit_card)
credit_btn.grid(row=1, column=0, columnspan=2, pady=5)
credit_result = ttk.Label(tab_credit, text="")
credit_result.grid(row=2, column=0, columnspan=2, pady=5)

tab_control.pack(expand=1, fill="both")

root.mainloop()
