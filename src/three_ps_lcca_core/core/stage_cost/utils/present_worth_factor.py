def sum_of_present_worth_factor(
    inflation_rate,
    discount_rate,
    analysis_period,
    interval,
    service_life,
    construction_period=0,
    debug=False
):
    i = inflation_rate / 100
    d = discount_rate / 100
    r = (1 + i) / (1 + d)

    years = []
    factors = []

    cycle_length = construction_period + service_life
    cycle_start = 0

    while cycle_start < analysis_period:
        op_start = cycle_start + construction_period

        for age in range(interval, service_life, interval):
            year = op_start + age

            if year >= analysis_period:
                break

            # Round year to 2 decimal places BEFORE calculating PWI
            year = round(year, 2)

            years.append(year)
            factors.append(r ** year)

        cycle_start += cycle_length

    total = sum(factors)

    if debug:
        return {
            "total": round(total, 3),
            "breakdown": {
                "year_to_pwf": {y: round(p, 3) for y, p in zip(years, factors)},
                "construction_period": construction_period,
                "service_life": service_life,
                "interval": interval
            }
        }

    return {"total": round(total, 3)}


def demolition_spwi(
    inflation_rate,
    discount_rate,
    analysis_period,
    service_life,
    construction_period=0,
    demolition_duration_years=0,
    debug=False
):
    i = inflation_rate / 100
    d = discount_rate / 100
    r = (1 + i) / (1 + d)

    cycle_length = construction_period + service_life
    cycle_start = 0

    reconstruction_years = []

    while cycle_start < analysis_period:
        demolition_year = (
            cycle_start
            + construction_period
            + service_life
            + demolition_duration_years
        )

        if demolition_year < analysis_period:
            # Round year to 2 decimal places BEFORE calculating PWI
            demolition_year = round(demolition_year, 2)
            reconstruction_years.append(demolition_year)

        cycle_start += cycle_length

    final_year = round(analysis_period, 2)

    reconstruction_pwi = {year: r ** year for year in reconstruction_years}
    final_pwi = {final_year: r ** final_year}

    if debug:
        return {
            "reconstruction_demolition": round(sum(reconstruction_pwi.values()), 3),
            "final_demolition": round(final_pwi[final_year], 3),
            "reconstruction_demolition_breakdown": {
                y: round(p, 3) for y, p in reconstruction_pwi.items()
            },
            "final_demolition_breakdown": {final_year: round(final_pwi[final_year], 3)}
        }

    return {
        "reconstruction_demolition": round(sum(reconstruction_pwi.values()), 3),
        "final_demolition": round(final_pwi[final_year], 3)
    }
