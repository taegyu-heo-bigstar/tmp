"""
금융데이터와 프로그래밍 - 숙제 4 / 3번
채권 가격 및 만기수익률(YTM) 계산기

내용:
1. 채권의 액면가, 표면이율, 만기, 시장이자율을 입력받아 이론적 채권 가격을 계산합니다.
2. 현재 시장가격을 입력하면 이분법(bisection method)으로 만기수익률(YTM)을 역산합니다.

실행 방법:
    python bond_ytm_calculator.py

주의:
- 이율은 5%를 0.05처럼 소수로 입력합니다.
- 기본 설정은 연 1회 이자 지급입니다.
"""


def validate_inputs(face_value, coupon_rate, maturity, rate, payments_per_year=1):
    """입력값이 계산 가능한 범위인지 확인합니다."""
    if face_value <= 0:
        raise ValueError("액면가는 0보다 커야 합니다.")
    if coupon_rate < 0:
        raise ValueError("표면이율은 0 이상이어야 합니다.")
    if maturity <= 0:
        raise ValueError("만기는 0보다 커야 합니다.")
    if payments_per_year <= 0 or not isinstance(payments_per_year, int):
        raise ValueError("연간 이자 지급 횟수는 양의 정수여야 합니다.")
    if 1 + rate / payments_per_year <= 0:
        raise ValueError("할인율이 너무 낮아 계산할 수 없습니다.")


def bond_price(face_value, coupon_rate, maturity, market_rate, payments_per_year=1):
    """
    채권의 이론 가격을 계산합니다.

    Parameters
    ----------
    face_value : float
        채권 액면가
    coupon_rate : float
        연 표면이율. 예: 5% -> 0.05
    maturity : float
        만기까지 남은 기간. 단위: 년
    market_rate : float
        연 시장이자율 또는 요구수익률. 예: 4% -> 0.04
    payments_per_year : int
        연간 이자 지급 횟수. 연 1회=1, 반기=2, 분기=4

    Returns
    -------
    float
        이론적 채권 가격
    """
    validate_inputs(face_value, coupon_rate, maturity, market_rate, payments_per_year)

    periods = int(round(maturity * payments_per_year))
    coupon_payment = face_value * coupon_rate / payments_per_year
    period_rate = market_rate / payments_per_year

    price = 0.0

    # 매 기간 지급되는 이자 현금흐름의 현재가치 합계
    for t in range(1, periods + 1):
        price += coupon_payment / ((1 + period_rate) ** t)

    # 만기 시점에 상환되는 액면가의 현재가치
    price += face_value / ((1 + period_rate) ** periods)

    return price


def ytm_from_price(
    face_value,
    coupon_rate,
    maturity,
    market_price,
    payments_per_year=1,
    tolerance=1e-7,
    max_iterations=200,
):
    """
    현재 시장가격을 기준으로 만기수익률(YTM)을 역산합니다.

    scipy 없이도 실행 가능하도록 이분법을 사용했습니다.
    채권 가격은 일반적으로 수익률이 올라가면 하락하므로,
    목표 가격과 계산 가격의 차이가 0이 되는 수익률을 찾습니다.

    Returns
    -------
    float
        연율 기준 YTM
    """
    if market_price <= 0:
        raise ValueError("시장가격은 0보다 커야 합니다.")

    validate_inputs(face_value, coupon_rate, maturity, 0.0, payments_per_year)

    def price_difference(rate):
        return bond_price(
            face_value,
            coupon_rate,
            maturity,
            rate,
            payments_per_year,
        ) - market_price

    # 할인율의 하한은 기간 할인율이 -100%가 되지 않도록 설정합니다.
    low = -0.9999 * payments_per_year
    high = 1.0

    # high에서 계산 가격이 시장가격보다 여전히 높으면 high를 키워 탐색 범위를 확장합니다.
    while price_difference(high) > 0:
        high *= 2
        if high > 100:
            raise ValueError("YTM 탐색 범위를 찾지 못했습니다. 입력값을 확인하세요.")

    for _ in range(max_iterations):
        mid = (low + high) / 2
        diff = price_difference(mid)

        if abs(diff) < tolerance:
            return mid

        if diff > 0:
            low = mid
        else:
            high = mid

    return (low + high) / 2


def print_bond_result(face_value, coupon_rate, maturity, market_rate, payments_per_year=1):
    """예제 결과를 보기 좋게 출력합니다."""
    price = bond_price(face_value, coupon_rate, maturity, market_rate, payments_per_year)

    print("[채권 가격 계산 결과]")
    print(f"액면가: {face_value:,.0f}원")
    print(f"표면이율: {coupon_rate * 100:.2f}%")
    print(f"만기: {maturity}년")
    print(f"시장 이자율: {market_rate * 100:.2f}%")
    print(f"연간 이자 지급 횟수: {payments_per_year}회")
    print(f"이론적 채권 가격: {price:,.2f}원")
    print()


def main():
    """과제 제출용 실행 예시입니다."""
    # 예시 1: 채권 가격 계산
    face_value = 10000        # 액면가 10,000원
    coupon_rate = 0.05        # 표면이율 5%
    maturity = 3              # 만기 3년
    market_rate = 0.04        # 시장이자율 4%
    payments_per_year = 1     # 연 1회 이자 지급

    print_bond_result(
        face_value,
        coupon_rate,
        maturity,
        market_rate,
        payments_per_year,
    )

    # 예시 2: 시장가격을 이용한 YTM 역산
    market_price = 10277.50
    ytm = ytm_from_price(
        face_value,
        coupon_rate,
        maturity,
        market_price,
        payments_per_year,
    )

    print("[만기수익률(YTM) 역산 결과]")
    print(f"시장가격: {market_price:,.2f}원")
    print(f"역산된 YTM: {ytm * 100:.4f}%")


if __name__ == "__main__":
    main()
