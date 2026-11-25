# Shell pipelines: awk, sort, uniq, head

## Key ideas

- Every command reads **stdin** and writes **stdout**. `|` connects one command's stdout to the next command's stdin.
- Each command is a small filter doing one job. Pipelines are built **one stage at a time**: add a stage, run it, look at the output, then add the next.
- The classic counting pattern is **extract → sort → count → sort by count → top N**.

## The tools

### awk: pick fields
- Splits each line on whitespace: `$1`, `$2`, …; `$0` is the whole line; `NF` is the number of fields.
- `awk '{print $1}' file`: first column.
- `awk '{print $2, $1}' file`: reorder columns.
- **Gotcha:** quotes and brackets don't group anything, only spaces split fields. In an access log, `"GET` and `+0000]` are separate fields.

### sort: order lines
| Flag | Meaning |
|---|---|
| (none) | Alphabetical, so `10` comes before `2` |
| `-n` | Numeric |
| `-r` | Reverse |
| `-nr` | Numeric, highest first |

### uniq: collapse adjacent repeats
- Only merges lines that are **next to each other**, so input must be sorted first.
- `-c` puts a count in front of each line.

### head: keep the first N
- `head -3` keeps the first 3 lines (default is 10).

## Practice data

```
printf "apple red 3\nbanana yellow 5\napple green 2\ncherry red 7\napple red 1\nbanana green 4\n" > fruit.txt
```

## Q&A

### Why does `uniq` need `sort` first?
`uniq` compares each line only with the one before it. Unsorted, the same value shows up in separate runs, and each run is counted separately. `sort` puts equal lines next to each other.

### Why does plain `sort` put `10` before `2`?
It compares text character by character: `1` < `2`. `-n` compares the values as numbers.

### How do I find which field number holds a value?
`head -1 file | awk '{print $N}'` and change N. Or `awk '{print NF}'` to see how many fields there are, then count the spaces.

## Debugging a pipeline

- Remove the last stage and look at what goes into it.
- Add `| head` while building, so a big file doesn't flood the screen.
- Check totals: `| wc -l`, or add up the counts. They should match the input line count.

## My pipelines (bootcamp 1)

Log line: `192.168.1.23 - - [17/Nov/2026:21:30:01 +0000] "GET /api/items HTTP/1.1" 200 512`

### Top 10 IPs

```
awk '{print $1}' access.log | sort | uniq -c | sort -nr | head -10
```

| Stage | What it does |
|---|---|
| `awk '{print $1}' access.log` | Print only field 1, the client IP, one per line |
| `sort` | Put identical IPs next to each other, so `uniq` can see them |
| `uniq -c` | Collapse each run of the same IP into one line with its count in front |
| `sort -nr` | Sort by that count as a number, highest first |
| `head -10` | Keep the top 10 |

Output (20 IPs in the pool, picked uniformly, so the counts are close):
```
   2621 10.0.0.6
   2548 192.168.1.6
   2545 192.168.1.7
   2543 10.0.0.8
   2522 192.168.1.2
   2512 192.168.1.1
   2502 10.0.0.7
   2501 192.168.1.10
   2501 10.0.0.3
   2496 10.0.0.5
```
Reading it: 50,000 lines ÷ 20 IPs ≈ 2,500 each, so this is noise, not a heavy hitter. In a real log, one IP far above the rest is the signal to look into: a scraper, a retry storm or a misbehaving client.

### Count per status code

```
awk '{print $9}' access.log | sort | uniq -c | sort -nr
```

**Why field 9?** awk splits on spaces only, so the quoted request is 3 fields:

| Field | `$1` | `$2` | `$3` | `$4` | `$5` | `$6` | `$7` | `$8` | `$9` | `$10` |
|---|---|---|---|---|---|---|---|---|---|---|
| Value | `192.168.1.23` | `-` | `-` | `[17/Nov/2026:21:30:01` | `+0000]` | `"GET` | `/api/items` | `HTTP/1.1"` | **`200`** | `512` |

Same stages as above, with no `head` because there are only 4 codes.

Output (adds up to 50,000; shares match the 80/10/5/5 weights in `gen_log.py`):
```
  39990 200
   4990 404
   2535 500
   2485 301
```
Reading it: the 5xx rate is 2,535 / 50,000 ≈ **5%**. In production that's an incident; most SLOs allow well under 1%.

### Bonus: the same count in one awk

```
awk '{count[$9]++} END {for (s in count) print count[s], s}' access.log | sort -nr
```
`count` is an associative array (a dict) keyed by status. `END` runs after the last line. This uses one process instead of four and doesn't need the first sort, which is handy on huge logs. Interviewers like seeing both.

## Common mistakes

- `uniq -c` without `sort` first → the same value is counted in several pieces.
- `sort -r` instead of `sort -nr` on counts → text order, so `9` beats `10`.
- Off-by-one field numbers because of spaces inside quotes.

## Self-test

1. What do stdin, stdout and `|` mean?
2. Why must `sort` come before `uniq -c`?
3. What's the difference between `sort -r` and `sort -nr` on counts?
4. In `1.2.3.4 - - [17/Nov/2026:21:30:01 +0000] "GET /x HTTP/1.1" 200 512`, which field is the status? Why?
5. What's the 5-stage pattern for "top N of a column"?

## References

- `man awk`, `man sort`, `man uniq`, `man head`
- [The GNU Awk User's Guide: Getting Started](https://www.gnu.org/software/gawk/manual/html_node/Getting-Started.html)
- [Julia Evans: Bite Size Command Line](https://wizardzines.com/zines/bite-size-command-line/)
