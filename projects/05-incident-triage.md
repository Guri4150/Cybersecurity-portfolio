# SOC triage: suspicious authentication activity

**Type:** Fictional case study created for this portfolio. All events below are hypothetical and do not describe a real employer or investigation.

## Scenario

An identity alert reports repeated failed sign-ins followed by a successful login for one account from an unfamiliar source. The user's expected work schedule and travel status have not yet been confirmed.

## Initial assessment

Treat the alert as requiring prompt review. Failed attempts followed by success could indicate guessing or stolen credentials, but could also reflect a legitimate user correcting a password. Set an initial priority according to the account's privilege, affected resources, and the organization's severity matrix; do not infer severity from event volume alone.

## Investigation workflow

1. Preserve alert identifiers, raw authentication events, timestamps and time zones.
2. Confirm the account, source address, device, application, authentication method, and MFA outcome.
3. Compare the source and device with the account's baseline. Consider VPNs, shared gateways, and IP geolocation limitations.
4. Contact the user through an established trusted channel and verify whether the activity was expected.
5. Correlate identity, endpoint, VPN, and application logs for session activity, privilege changes, and access to sensitive data.
6. Escalate according to the playbook, documenting confirmed facts separately from hypotheses.

## Decision examples

| Evidence | Proposed action |
|---|---|
| User confirms expected activity and corroborating logs agree | Document rationale and close under the approved process |
| User denies the login or evidence shows session misuse | Escalate; seek authorized account/session containment |
| Privileged account or sensitive resource is involved | Increase urgency according to the severity matrix |
| Logs are missing or contradictory | Keep the case open and document the evidence gap |

## Containment and recovery considerations

With the appropriate authority, actions could include revoking sessions, resetting credentials, reviewing MFA enrollment, and isolating an endpoint when endpoint compromise is supported. Account for business impact and preserve evidence before changes where feasible. Validate recovery and monitor for recurrence before closure.

## Case record

A complete report should include the timeline, affected entities, evidence references, confidence level, actions and approvals, business impact, disposition, and follow-up owner. For this fictional scenario, the outcome remains undetermined because no logs or user confirmation were supplied.

## Learning outcome

Good triage connects multiple evidence sources and states uncertainty clearly. A suspicious alert is the beginning of an investigation, not a confirmed breach.
