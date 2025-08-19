import time

RATE_LIMIT = 20
WINDOW = 300
ip_buckets = {}


def cleanup_old_buckets():
    now = time.time()
    expired_ips = []

    for ip, timestamps in ip_buckets.items():
        recent_timestamps = [t for t in timestamps if now - t < WINDOW]

        if recent_timestamps:
            ip_buckets[ip] = recent_timestamps
        else:
            expired_ips.append(ip)

    for ip in expired_ips:
        del ip_buckets[ip]


def is_rate_limited(ip):
    cleanup_old_buckets()
    now = time.time()
    if ip not in ip_buckets:
        ip_buckets[ip] = []
    ip_buckets[ip] = [t for t in ip_buckets[ip] if now - t < WINDOW]
    if len(ip_buckets[ip]) >= RATE_LIMIT:
        return True
    ip_buckets[ip].append(now)
    return False
