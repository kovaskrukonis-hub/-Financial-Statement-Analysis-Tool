def score_metric(value, thresholds):

    if value is None or value != value:
        return None
    for condition, points in thresholds:
        if condition(value):
            return points
    return 0


def calculate_scores(
    # Valuation
    price_to_earnings,
    eps,
    margin_of_safety,
    # Profitability
    return_on_assets,
    return_on_equity,
    gross_profit_margin,
    operating_profit_margin,
    # Solvency & Efficiency
    current_ratio,
    debt_to_assets,
    interest_coverage,
    inventory_turnover_year,
    avg_collection_period,
    average_payment_period,
):

    valuation_scores = []

    # P/E: negative means net loss, <15 is cheap, <30 is fair, >=30 is expensive
    valuation_scores.append(score_metric(price_to_earnings, [
        (lambda v: v < 0,  0),
        (lambda v: v < 15, 2),
        (lambda v: v < 30, 1),
    ]))

    # EPS: positive = profitable, negative = loss
    valuation_scores.append(score_metric(eps, [
        (lambda v: v > 0, 2),
    ]))

    # DCF Margin of Safety: >=30% deeply undervalued, >=0% fair, <0% overvalued
    valuation_scores.append(score_metric(margin_of_safety, [
        (lambda v: v >= 30, 2),
        (lambda v: v >= 0,  1),
    ]))


    profitability_scores = []

    # ROA: >10% excellent, >5% acceptable
    profitability_scores.append(score_metric(return_on_assets, [
        (lambda v: v > 10, 2),
        (lambda v: v > 5,  1),
    ]))

    # ROE: >20% excellent, >10% acceptable
    profitability_scores.append(score_metric(return_on_equity, [
        (lambda v: v > 20, 2),
        (lambda v: v > 10, 1),
    ]))

    # Gross Profit Margin: >40% strong, >20% acceptable
    profitability_scores.append(score_metric(gross_profit_margin, [
        (lambda v: v > 40, 2),
        (lambda v: v > 20, 1),
    ]))

    # Operating Margin: >15% strong, >8% acceptable
    profitability_scores.append(score_metric(operating_profit_margin, [
        (lambda v: v > 15, 2),
        (lambda v: v > 8,  1),
    ]))

    solvency_scores = []

    # Current Ratio: >2 strong, >1 acceptable, <1 risky
    solvency_scores.append(score_metric(current_ratio, [
        (lambda v: v > 2, 2),
        (lambda v: v > 1, 1),
    ]))

    # Debt to Assets: <20% strong, <50% acceptable, >=50% risky
    solvency_scores.append(score_metric(debt_to_assets, [
        (lambda v: v < 20, 2),
        (lambda v: v < 50, 1),
    ]))

    # Interest Coverage: >5x strong, >2x acceptable
    solvency_scores.append(score_metric(interest_coverage, [
        (lambda v: v > 5, 2),
        (lambda v: v > 2, 1),
    ]))

    # Inventory Turnover: >10 strong, >5 acceptable
    # None is valid for service companies — excluded gracefully
    solvency_scores.append(score_metric(inventory_turnover_year, [
        (lambda v: v > 10, 2),
        (lambda v: v > 5,  1),
    ]))

    # Average Collection Period: <30 days strong, <60 days acceptable
    solvency_scores.append(score_metric(avg_collection_period, [
        (lambda v: v < 30, 2),
        (lambda v: v < 60, 1),
    ]))

    # Average Payment Period: >45 days strong (holding cash longer = good),
    # >30 days acceptable, <30 days means paying suppliers too fast
    solvency_scores.append(score_metric(average_payment_period, [
        (lambda v: v > 45, 2),
        (lambda v: v > 30, 1),
    ]))

    # AGGREGATE: scale each category to 0–10
    # Only count metrics with actual data (skip None)
    
    def category_score(scores):
        valid = [s for s in scores if s is not None]
        if not valid:
            return None
        return round((sum(valid) / (len(valid) * 2)) * 10, 1)

    valuation_cat     = category_score(valuation_scores)
    profitability_cat = category_score(profitability_scores)
    solvency_cat      = category_score(solvency_scores)

    # FINAL WEIGHTED SCORE (0–100)
    # Valuation 35%, Profitability 30%, Solvency & Efficiency 35%
    # Weight redistributes automatically if a whole category has no data
    
    weights = {
        'valuation':     0.35,
        'profitability': 0.30,
        'solvency':      0.35,
    }
    category_map = {
        'valuation':     valuation_cat,
        'profitability': profitability_cat,
        'solvency':      solvency_cat,
    }

    total_weight = sum(w for k, w in weights.items() if category_map[k] is not None)

    if total_weight == 0:
        final_score = None
    else:
        weighted_sum = sum(
            (category_map[k] / 10) * w
            for k, w in weights.items()
            if category_map[k] is not None
        )
        final_score = round((weighted_sum / total_weight) * 100, 1)

    return {
        'valuation':     valuation_cat,
        'profitability': profitability_cat,
        'solvency':      solvency_cat,
        'final_score':   final_score,
    }


def get_verdict(score):

    if score is None:
        return None, None, None
    if score >= 80:
        return "STRONG BUY",   "\033[92m", "Fundamentals are excellent across the board"
    elif score >= 65:
        return "BUY",          "\033[92m", "Solid fundamentals with good value"
    elif score >= 50:
        return "HOLD",         "\033[93m", "Mixed signals — proceed with caution"
    elif score >= 35:
        return "WEAK",         "\033[91m", "Several weak areas, elevated risk"
    else:
        return "AVOID",        "\033[91m", "Fundamentals are poor across most categories"

