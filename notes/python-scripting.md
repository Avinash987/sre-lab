# Python scripting for ops

## Key ideas

- Ops scripts are small and boring on purpose: functions, `with open`, a `__main__` guard.
- When generating test data, the **shape** of the data must match what you'll test. Random isn't the same as realistic.

## Building blocks

```python
import random
random.choice(["GET", "POST"])                         # one item, all equally likely
random.choices([200, 404], weights=[9, 1])[0]          # weighted; returns a LIST, so take [0]
random.choices(pool, weights=w, k=1000)                # k picks at once
random.randint(100, 5000)                              # int, both ends included

from datetime import datetime, timedelta
t = datetime(2026, 11, 17, 21, 30, 1)
t.strftime("%d/%b/%Y:%H:%M:%S +0000")                  # 17/Nov/2026:21:30:01 +0000
t + timedelta(seconds=2)                               # move time forward

with open("access.log", "w") as f:                     # closes the file even on error
    f.write(line + "\n")                               # write() adds no newline for you

if __name__ == "__main__":                             # runs only when executed, not on import
    main()
```

### strftime codes I used

| Code | Means | Example |
|---|---|---|
| `%d` | day, 2 digits | `17` |
| `%b` | short month name | `Nov` |
| `%Y` | 4-digit year | `2026` |
| `%H:%M:%S` | 24h time | `21:30:01` |

## Q&A

### Why must IPs come from a small pool?
4 random octets give ~4.3 billion possible IPs, so 50,000 lines are nearly all unique. A "top 10 IPs" query would then show ten IPs with a count of 1 each and prove nothing. Real traffic is skewed: a few clients send most requests.

### How big should the pool be?
Bigger than the "top N" you'll query, and skewed. With exactly 10 IPs picked uniformly, "top 10" just lists every IP with about the same count, which proves nothing. Use more IPs than N (for example 20), or weight them so a few dominate.

### `random.choice` vs `random.choices`?
`choice(seq)` returns one item, all equally likely. `choices(seq, weights=..., k=n)` returns a **list** of n items, picked using the weights. Use it when some outcomes should be more common, like 200s in a log.

### Why should log timestamps go forward?
Logs are written as events happen, so they're in time order. Tools and tasks that slice by time, like "errors in the last 5 minutes", assume that order.

## Common mistakes

- Uniform random data when the task needs skew (IPs, status codes).
- Recomputing a constant inside a loop, for example `datetime.now()` on every line.
- Forgetting `\n` in `f.write()` gives one giant line.
- Forgetting `[0]` after `random.choices(...)` puts `[200]` in the log instead of `200`.

## Self-test

1. What does `random.choices` return, and why do you often need `[0]`?
2. Why is fully random IP data useless for a "top talkers" query?
3. What does `if __name__ == "__main__":` protect against?
4. Write the strftime string for `17/Nov/2026:21:30:01 +0000` from memory.

## References

- [random: choices](https://docs.python.org/3/library/random.html#random.choices)
- [datetime: strftime format codes](https://docs.python.org/3/library/datetime.html#format-codes)
