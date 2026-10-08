# Case SYN-CASE-001 — failures followed by success

**Exercise:** fictional, offline, educational.  
**Disposition:** alert condition met; suspicious authentication, compromise unconfirmed.  
**Priority:** Medium, review promptly under an organization's own response targets.  
**Response status:** recommendations only; no actions executed.

## Scenario assumptions, separate from log evidence

The fictional organization is Owl Learning Lab. For this scenario only,
`demo_owl` is a standard, non-administrative training account in one
fictional authentication service. There is no asset inventory or privilege
record in the dataset to verify that assumption. Source ownership, approved
access patterns, device identity, and user intent are unknown.

All seven records were authored for this exercise. They are not captured
telemetry. Authentication success is the status recorded by the fictional
service; no session creation or subsequent access is independently verified.

## Evidence inventory and timeline

Evidence E1 is `synthetic_auth.jsonl`; E2 is generated `example_alerts.json`.
E2 is derived from E1 and is not independent corroboration. The detector and
tests make this transformation reproducible. Times below are UTC,
October 7, 2026.

| Time | E1 line | Recorded event | Interpretation |
|---|---:|---|---|
| 09:00 | 1 | demo_owl, 192.0.2.10, failure | One unsuccessful authentication |
| 09:01 | 2 | Same user/IP, failure | Repeated failure |
| 09:02 | 3 | Same user/IP, failure | Third failure |
| 09:03 | 4 | Same user/IP, success | Meets correlation rule with lines 1–3 |
| 09:04 | 5 | demo_fox, 203.0.113.30, failure | Separate user/IP |
| 09:05 | 6 | demo_fox, 203.0.113.30, success | Only one prior failure; no alert |
| 09:06 | 7 | demo_badger, 198.51.100.20, success | No prior matching failures; no alert |

The full observed interval is 09:00–09:06. These seven lines are the entire
fixture, not proof that all relevant activity has been collected.

## Triage performed on the fixture

1. **Validate the evidence:** the run reports seven unique valid events,
   no invalid or blank lines, and no duplicate tuples.
2. **Reproduce the alert:** identify the success at line 4; match failures
   at lines 1–3 by username and source IP.
3. **Check the time window:** failures occurred 180, 120, and 60 seconds
   before the success, all inside the inclusive 300-second lower boundary.
4. **Check surrounding fixture activity:** the other user/IP pairs do not
   meet the threshold. There is no further `demo_owl` event in this file.
5. **Assess evidence gaps:** no device, destination, MFA, session, application
   audit, endpoint, or owner-confirmation evidence is supplied.
6. **Assign Medium and retain uncertainty:** repeated failures plus success
   justify review, but the dataset cannot distinguish mistakes from misuse.

## Questions for an authorized follow-up investigation

These are proposed steps, not completed interviews or findings:

| Question | Evidence to request | Effect on assessment |
|---|---|---|
| Did the account owner expect this login? | Independent verified contact and approved activity records | Unexpected use increases concern; a claim alone does not close the alert |
| Was the device/session expected? | Identity-provider device, session, MFA and authentication-method logs | New device, unusual MFA activity, or unknown session increases concern |
| What privileges and assets were accessible? | Account roles and asset inventory | Administrative or sensitive access raises potential impact |
| What happened after success? | Application audit and endpoint process/file/network events | Unauthorized changes or access can substantiate an incident |
| Is this part of a wider pattern? | Broader authorized searches by account, source, service and time | Reveals additional affected accounts or distributed attempts |
| Are the records reliable and complete? | Collector health, time synchronization, retention and event IDs | Gaps reduce confidence; no events is not proof of no activity |

Start with the surrounding 30 minutes, then expand based on findings and
available retention. Correlate by session/device identifiers when available;
timing alone does not prove that one event caused another.

## Severity decision

This exercise uses its own simple rubric, not an industry-wide scoring scale:

| Level | Example decision basis |
|---|---|
| Low | Isolated failures with no success or corroborating concern |
| Medium | Repeated failures then success, impact and legitimacy unresolved |
| High | Corroborated unauthorized use or a suspicious privileged/sensitive session |
| Critical | Verified ongoing destructive activity or broad severe business impact |

**Selected: Medium.** The rule condition is reproducible and the successful
status merits investigation. The scenario assumes a standard training account;
there is no evidence of privileged access, malicious post-login behavior,
data loss, or service impact. Confidence is high that the fixture matches the
rule, but evidence is insufficient to conclude malicious activity.

Escalate if owner verification and session evidence support unauthorized use,
or if sensitive access or malicious endpoint activity is found. Lower or close
as benign only after corroborated expected activity and adequate log coverage.
Do not automatically close merely because later activity is absent from this
tiny fixture.

## Findings and competing explanations

**Supported:** three recorded failures precede one recorded success for the
same account and IP within three minutes; one rule alert results.

**Plausible benign explanation:** a legitimate user corrected a password after
three mistakes, or a stale client credential caused failures.

**Plausible malicious explanation:** someone guessed or otherwise obtained a
credential and authenticated. The logs contain neither passwords nor the
method used, so successful password guessing cannot be concluded.

**Not established:** attacker identity, IP reputation, brute force, successful
MFA, actual session use, privilege escalation, malware, lateral movement,
exfiltration, or root cause. The documentation IP has no attributed actor.

## Containment recommendations

No blocking is warranted solely by this fixture. In a real authorized workflow:

1. Preserve relevant raw logs, export metadata, timestamps and session details
   in approved evidence storage. Record collection scope and chain of custody.
2. Notify the designated incident lead and account/service owner through
   approved channels; coordinate potential account disruption.
3. If unauthorized activity is corroborated, revoke affected sessions and
   tokens, temporarily restrict the affected account as appropriate, and reset
   compromised credentials through trusted recovery.
4. Consider source restrictions only after checking shared-IP impact and
   confirming the control is useful. Blocking an IP alone does not invalidate
   active sessions or address other sources.
5. Isolate an endpoint only if endpoint evidence supports compromise and an
   authorized response owner approves the operational impact.

Record the actor, reason, scope, timestamp, approval and rollback path for each
action. Do not execute these actions against any real account for this exercise.

## Eradication, recovery and closure recommendations

Identify the actual cause before claiming eradication. If credentials were
compromised, rotate affected secrets, remove unauthorized access methods and
review MFA enrollment. If a stale client or user error is corroborated, correct
that cause and avoid blanket rule suppression.

Restore access after identity verification and control checks. Verify expected
login behavior, session revocation, legitimate service operation, and continued
log collection. Define a monitoring period with the incident owner based on
risk; review recurrence and related alerts before closure.

Closure requires a documented disposition, adequate evidence supporting the
cause or an explicit unresolved limitation, completed authorized actions where
needed, successful recovery checks, and review by the designated owner.
This case ends at a simulated recommendation stage; no recovery or remediation
is claimed complete.

## Lessons

Time windows and account grouping make the original aggregate parser more
useful for triage. A detected sequence still needs independent evidence.
Future improvements are stable event IDs, service/host identifiers, session
correlation, ingestion-quality monitoring and a real isolated SIEM deployment.
