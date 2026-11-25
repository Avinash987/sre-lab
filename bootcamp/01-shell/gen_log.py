"""Generate a realistic HTTP access log for testing."""

import random
from datetime import datetime, timedelta, timezone

IP_ADDRESSES = (
    "192.168.1.1",
    "192.168.1.2",
    "192.168.1.3",
    "192.168.1.4",
    "192.168.1.5",
    "192.168.1.6",
    "192.168.1.7",
    "192.168.1.8",
    "192.168.1.9",
    "192.168.1.10",
    "10.0.0.1",
    "10.0.0.2",
    "10.0.0.3",
    "10.0.0.4",
    "10.0.0.5",
    "10.0.0.6",
    "10.0.0.7",
    "10.0.0.8",
    "10.0.0.9",
    "10.0.0.10"
)
HTTP_METHODS = ("GET", "POST", "PUT", "DELETE")
ENDPOINTS = ("/api/items", "/api/users", "/api/orders", "/api/products")
RESPONSE_CODES = (200, 301, 404, 500)
RESPONSE_CODE_WEIGHTS = (80, 5, 10, 5)


def generate_log_entry(timestamp=None):
    if timestamp is None:
        timestamp = datetime.now(timezone.utc)

    ip_address = random.choice(IP_ADDRESSES)
    formatted_timestamp = timestamp.strftime("%d/%b/%Y:%H:%M:%S +0000")

    method = random.choice(HTTP_METHODS)
    endpoint = random.choice(ENDPOINTS)

    http_version = "HTTP/1.1"
    response_code = random.choices(
        RESPONSE_CODES, weights=RESPONSE_CODE_WEIGHTS, k=1
    )[0]

    response_size = random.randint(100, 5000)

    return (
        f'{ip_address} - - [{formatted_timestamp}] '
        f'"{method} {endpoint} {http_version}" {response_code} {response_size}'
    )


def generate_log_file(filename, num_entries=50000):
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=365)

    with open(filename, 'w') as log_file:
        for index in range(num_entries):
            if num_entries > 1:
                timestamp = start_time + (end_time - start_time) * (
                    index / (num_entries - 1)
                )
            else:
                timestamp = end_time

            log_entry = generate_log_entry(timestamp)
            log_file.write(log_entry + '\n')


if __name__ == "__main__":
    generate_log_file("access.log")