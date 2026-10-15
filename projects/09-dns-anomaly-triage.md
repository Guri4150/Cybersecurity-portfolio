# DNS anomaly triage: evidence, hypotheses and detection tuning

**Type:** Fictional SOC tabletop exercise based on cybersecurity practice on 15 October 2026.  
**Status:** Written analysis only. No real incident, packet capture, Wireshark execution or deployed SIEM rule is claimed.

## Investigation question

Does a burst of TXT queries from a workstation justify escalation, and what evidence would distinguish DNS tunneling from legitimate software activity?

## Scenario and supplied evidence

In this simulated scenario, workstation `ws-07` (`10.20.5.7`) generates 480 DNS queries during the five-minute window `[08:30, 08:35)`, compared with a supplied baseline of 20–40 queries per five minutes. Many queries use changing subdomains of `sync.example`. An approved software update started at 08:29, but the process generating the DNS queries is unknown.

All times are fictional UTC times on 15 October 2026. The domain uses the reserved `.example` namespace. The totals and baseline are scenario inputs, not measurements derived from the small samples below.

### Illustrative DNS log excerpt

```text
08:30:01 client=10.20.5.7 query=a81f.sync.example type=TXT
08:30:02 client=10.20.5.7 query=b92e.sync.example type=TXT
08:30:03 client=10.20.5.7 query=c03d.sync.example type=TXT
```

### Independent packet-filter exercise

This five-row synthetic packet summary is for filter practice; it is not a complete representation of the 480-query window.

| Frame | Source | Destination | DNS message | Question type | Question name |
|---|---|---|---|---|---|
| 1 | 10.20.5.7 | 10.20.0.53 | Query | TXT (16) | a81f.sync.example |
| 2 | 10.20.0.53 | 10.20.5.7 | Response | TXT (16) | a81f.sync.example |
| 3 | 10.20.5.7 | 10.20.0.53 | Query | A (1) | portal.example |
| 4 | 10.20.5.8 | 10.20.0.53 | Query | TXT (16) | b92e.sync.example |
| 5 | 10.20.5.7 | 10.20.0.53 | Query | TXT (16) | c03d.sync.example |

## Evidence assessment

| Supported by the scenario | Not established |
|---|---|
| Query volume exceeds the supplied baseline. | An attacker controls the workstation or domain. |
| Several illustrated queries request TXT records with changing names. | Those names encode sensitive data or exhibit high entropy. |
| An approved update began shortly before the burst. | The updater generated or explains the queries. |
| The client queries an internal resolver. | The resolver forwarded each query to an external authoritative server. |

**Working assessment:** Suspicious DNS activity requiring investigation; exfiltration is not confirmed.

Two competing explanations remain open:

- **Possible DNS tunneling:** A process could encode outbound data in queried names. TXT answers could carry data back. A TXT query does not itself contain the TXT answer payload.
- **Possible legitimate activity:** An updater could make TXT lookups for metadata, or repeated lookups could reflect retries. This must be verified against the actual software's behavior.

Three short changing labels are insufficient to establish high entropy. Assess a larger sample before making that claim.

## Wireshark filter and expected result

**Language:** Wireshark display-filter syntax.

```text
ip.src == 10.20.5.7 && dns.flags.response == 0 && dns.qry.type == 16
```

Expected matches by inspection: **frames 1 and 5**.

- Frame 2 is a response.
- Frame 3 asks for an A record.
- Frame 4 comes from another client.

This result is reasoned from the table, not obtained by running Wireshark. The filter selects decoded DNS queries; it does not identify malicious traffic by itself.

## Detection reasoning

**Language:** Vendor-neutral pseudocode; not executable SIEM syntax.

```text
Select DNS query events with event_time >= window_start
                        and event_time < window_end
Group by client_ip
Alert when query_count > 100
```

The supplied count of 480 triggers this illustrative rule in the specified window. A count of exactly 100 would not. The threshold is a teaching example, not a production recommendation.

A raw count can also flag updates, retry storms or other legitimate bursts. Improve investigation context by:

1. Grouping by client and destination domain, with a defined domain-normalization method; for this fixture, use sync.example.
2. Considering distinct queried names, query-type distribution, label lengths and measured entropy across an adequate sample.
3. Comparing activity with the host's historical behavior and relevant peer systems.
4. Enriching the alert with process identity and verified change records.

Do not automatically suppress the alert because an update was approved. Also distinguish genuine repeated queries from duplicate telemetry before counting events. Account for delayed ingestion and retain alert deduplication state if searches overlap.

## Next investigation steps

1. Identify the generating process using endpoint telemetry: process identifier, executable path, parent process, signature where applicable, user and timestamps.
2. Check whether the updater normally produces these query names and types; compare other endpoints running the same update.
3. Examine a larger query sample and DNS responses, including response codes and answer content. Correlate resolver logs to determine whether queries were forwarded externally.
4. Preserve relevant endpoint and DNS evidence, document the window and visibility limits, and escalate under the incident-response playbook if corroborating evidence supports compromise.

Missing process or resolver telemetry should be recorded as an evidence gap, not treated as evidence that the activity is benign.

## Example analyst handoff

> ws-07 exceeded the supplied DNS baseline with 480 queries in the 08:30–08:35 UTC window. The sample includes changing TXT query names under sync.example. An approved update began at 08:29, but the generating process is unknown. DNS tunneling and legitimate software activity remain hypotheses; no sensitive-data transfer is established. Next checks are process attribution, updater behavior and resolver/query-response evidence.

## Skills demonstrated and next milestone

This exercise demonstrates evidence-based triage, DNS query/response interpretation, Wireshark filter reasoning, detection tuning and concise incident documentation.

**Future hands-on milestone:** Reproduce a small benign DNS fixture in an owned isolated lab, save a sanitized capture, apply the filter and record actual frame matches with tool version, date and limitations. Any capture or SIEM execution evidence must be added only after that work is performed.

[Back to portfolio](../README.md)
