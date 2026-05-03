from collections import defaultdict
from datetime import datetime, timedelta
from user_agents import parse

request_history = defaultdict(list)

SUSPICIOUS_KEYWORDS = [
    "python",
    "requests",
    "scrapy",
    "curl",
    "wget",
    "bot",
    "crawler",
    "spider",
    "selenium",
    "headless"
]


def detect_scraper(request):
    score = 0
    reasons = []

    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent", "")
    accept = request.headers.get("Accept", "")
    accept_language = request.headers.get("Accept-Language", "")
    referer = request.headers.get("Referer", "")

    now = datetime.now()

    request_history[ip].append(now)

    one_minute_ago = now - timedelta(minutes=1)
    request_history[ip] = [
        time for time in request_history[ip]
        if time > one_minute_ago
    ]

    requests_per_minute = len(request_history[ip])

    if requests_per_minute > 20:
        score += 40
        reasons.append("Too many requests in one minute")

    if requests_per_minute > 10:
        score += 20
        reasons.append("High request frequency")

    ua_lower = user_agent.lower()

    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in ua_lower:
            score += 40
            reasons.append(f"Suspicious User-Agent contains '{keyword}'")
            break

    if not user_agent:
        score += 30
        reasons.append("Missing User-Agent header")

    if not accept:
        score += 15
        reasons.append("Missing Accept header")

    if not accept_language:
        score += 15
        reasons.append("Missing Accept-Language header")

    if not referer and request.path not in ["/", "/dashboard"]:
        score += 10
        reasons.append("Missing Referer header")

    try:
        parsed_ua = parse(user_agent)

        if parsed_ua.is_bot:
            score += 35
            reasons.append("User-Agent recognized as bot")

        if not parsed_ua.browser.family:
            score += 20
            reasons.append("Unknown browser family")

    except Exception:
        score += 15
        reasons.append("Could not parse User-Agent")

    if score >= 70:
        status = "Blocked"
    elif score >= 40:
        status = "Suspicious"
    else:
        status = "Human"

    if not reasons:
        reasons.append("Normal browsing behavior")

    return score, status, ", ".join(reasons)
