# SQL for security investigations

**Type:** Reconstructed training queries. The examples assume the training schema below; they have not been executed against an attached dataset.

## Objective

Narrow an authentication investigation to relevant events and connect employee records to device inventory.

## Assumed schema

- `log_in_attempts(event_id, username, country, login_date, login_time, success)`
- `employees(username, department, office, device_id)`
- `machines(device_id, operating_system, os_patch_date)`

Inspect the actual schema first. Boolean representation and date functions can vary by database.

## Investigation queries

Find unsuccessful login attempts outside an example 07:00–18:00 shift:

```sql
SELECT event_id, username, login_date, login_time, country
FROM log_in_attempts
WHERE success = 0
  AND (login_time < '07:00:00' OR login_time >= '18:00:00')
ORDER BY login_date, login_time;
```

This is a lead for review, not proof of compromise. Validate the time zone, staff schedules, remote access, and whether failed attempts are followed by a successful login.

Review activity during an inclusive training date range:

```sql
SELECT event_id, username, login_date, login_time, success
FROM log_in_attempts
WHERE login_date BETWEEN '2022-05-09' AND '2022-05-11'
ORDER BY login_date, login_time;
```

This assumes `login_date` is a DATE. For timestamp columns, prefer a half-open range ending at the next day's midnight.

Find Finance and Sales employees and any linked device inventory:

```sql
SELECT e.username, e.department, e.device_id,
       m.operating_system, m.os_patch_date
FROM employees AS e
LEFT JOIN machines AS m ON e.device_id = m.device_id
WHERE e.department IN ('Finance', 'Sales')
ORDER BY e.department, e.username;
```

A LEFT JOIN preserves employee rows with missing inventory matches. A null result needs investigation; it does not by itself establish that a device is unpatched. Confirm join-key uniqueness to avoid duplicate rows being mistaken for additional devices.

## Verification plan

Use synthetic records at 06:59:59, 07:00:00, 17:59:59, and 18:00:00; include successful and unsuccessful events. Check employees with and without device matches. Save sanitized query output and explain why each returned record meets the filter.

## Takeaway

SQL helps scope an investigation efficiently. Conclusions require context, reliable timestamps, and corroborating evidence. No event counts or compromise findings are claimed in this write-up.
