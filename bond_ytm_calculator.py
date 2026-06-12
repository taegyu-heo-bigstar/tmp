# bond_ytm_calculator.py
# 채권 가격 및 만기수익률(YTM) 계산기

DEFAULT_FACE_VALUE = 10000.0
DEFAULT_COUPON_RATE = 0.05
DEFAULT_MATURITY = 3
DEFAULT_MARKET_RATE = 0.04
DEFAULT_PAYMENTS_PER_YEAR = 1
DEFAULT_MARKET_PRICE = 10277.50


def bond_price(face_value, coupon_rate, maturity, market_rate, payments_per_year):
    """
    채권의 이론적 가격을 계산합니다.

    face_value: 액면가
    coupon_rate: 표면이율
    maturity: 만기, 년 단위
    market_rate: 시장이자율
    payments_per_year: 연간 이자 지급 횟수
    """
    total_periods = maturity * payments_per_year
    coupon = face_value * coupon_rate / payments_per_year
    period_rate = market_rate / payments_per_year
    price = 0.0

    for period in range(1, total_periods + 1):
        price += coupon / ((1 + period_rate) ** period)

    price += face_value / ((1 + period_rate) ** total_periods)

    return price


def ytm_from_price(
    face_value,
    coupon_rate,
    maturity,
    market_price,
    payments_per_year,
    tolerance=0.000001,
    max_iteration=1000,
):
    """
    시장가격을 기준으로 만기수익률(YTM)을 역산합니다.

    scipy.optimize를 사용하지 않고,
    이분법을 이용해 YTM을 계산합니다.
    """
    low = -0.99
    high = 1.0

    for _ in range(max_iteration):
        mid = (low + high) / 2
        calculated_price = bond_price(
            face_value,
            coupon_rate,
            maturity,
            mid,
            payments_per_year,
        )

        if abs(calculated_price - market_price) < tolerance:
            return mid

        if calculated_price > market_price:
            low = mid
        else:
            high = mid

    return mid


def input_yes_or_no(message):
    """
    y 또는 n을 입력받습니다.
    y이면 True, n이면 False를 반환합니다.
    """
    while True:
        answer = input(message).strip().lower()

        if answer == "y":
            return True
        if answer == "n":
            return False

        print("y 또는 n만 입력하세요.")


def input_float(message):
    """
    실수 값을 입력받습니다.
    잘못된 값이 들어오면 다시 입력받습니다.
    """
    while True:
        try:
            return float(input(message))
        except ValueError:
            print("숫자를 입력하세요.")


def input_positive_int(message):
    """
    양의 정수를 입력받습니다.
    잘못된 값이 들어오면 다시 입력받습니다.
    """
    while True:
        try:
            value = int(input(message))

            if value > 0:
                return value

            print("1 이상의 정수를 입력하세요.")
        except ValueError:
            print("정수를 입력하세요.")


def get_user_inputs():
    """
    사용자 입력을 처리합니다.

    처음에 기본값 사용 여부를 y/n으로 입력받습니다.
    y를 입력하면 기존 기본값을 사용합니다.
    n을 입력하면 사용자가 직접 값을 입력합니다.
    """
    print("[기본값]")
    print(f"액면가: {DEFAULT_FACE_VALUE:,.0f}원")
    print(f"표면이율: {DEFAULT_COUPON_RATE * 100:.2f}%")
    print(f"만기: {DEFAULT_MATURITY}년")
    print(f"시장 이자율: {DEFAULT_MARKET_RATE * 100:.2f}%")
    print(f"연간 이자 지급 횟수: {DEFAULT_PAYMENTS_PER_YEAR}회")
    print(f"YTM 역산용 시장가격: {DEFAULT_MARKET_PRICE:,.2f}원")
    print()

    use_default = input_yes_or_no("기본값을 사용하시겠습니까? (y/n): ")

    if use_default:
        return (
            DEFAULT_FACE_VALUE,
            DEFAULT_COUPON_RATE,
            DEFAULT_MATURITY,
            DEFAULT_MARKET_RATE,
            DEFAULT_PAYMENTS_PER_YEAR,
            DEFAULT_MARKET_PRICE,
        )

    print()
    print("직접 값을 입력하세요.")
    print("주의: 이율은 5%가 아니라 0.05 형식으로 입력합니다.")
    print()

    face_value = input_float("액면가: ")
    coupon_rate = input_float("표면이율: ")
    maturity = input_positive_int("만기(년): ")
    market_rate = input_float("시장 이자율: ")
    payments_per_year = input_positive_int("연간 이자 지급 횟수: ")
    market_price = input_float("YTM 역산용 시장가격: ")

    return (
        face_value,
        coupon_rate,
        maturity,
        market_rate,
        payments_per_year,
        market_price,
    )


def make_result_text(
    face_value,
    coupon_rate,
    maturity,
    market_rate,
    payments_per_year,
    market_price,
):
    """
    계산 결과를 문자열로 생성합니다.

    결과를 복사하기 쉽도록 하나의 문자열로 만들어 반환합니다.
    """
    calculated_price = bond_price(
        face_value,
        coupon_rate,
        maturity,
        market_rate,
        payments_per_year,
    )

    ytm = ytm_from_price(
        face_value,
        coupon_rate,
        maturity,
        market_price,
        payments_per_year,
    )

    result = ""
    result += "===== 계산 결과 시작 =====\n"
    result += "[채권 가격 계산 결과]\n"
    result += f"액면가: {face_value:,.0f}원\n"
    result += f"표면이율: {coupon_rate * 100:.2f}%\n"
    result += f"만기: {maturity}년\n"
    result += f"시장 이자율: {market_rate * 100:.2f}%\n"
    result += f"연간 이자 지급 횟수: {payments_per_year}회\n"
    result += f"이론적 채권 가격: {calculated_price:,.2f}원\n"
    result += "\n"
    result += "[만기수익률(YTM) 역산 결과]\n"
    result += f"시장가격: {market_price:,.2f}원\n"
    result += f"역산된 YTM: {ytm * 100:.4f}%\n"
    result += "===== 계산 결과 끝 ====="

    return result


def main():
    """
    사용자 입력을 받은 뒤,
    채권 가격과 만기수익률을 계산합니다.
    """
    (
        face_value,
        coupon_rate,
        maturity,
        market_rate,
        payments_per_year,
        market_price,
    ) = get_user_inputs()

    result_text = make_result_text(
        face_value,
        coupon_rate,
        maturity,
        market_rate,
        payments_per_year,
        market_price,
    )

    print()
    print(result_text)


if __name__ == "__main__":
    main()
