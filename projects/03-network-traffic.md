# Network traffic investigation with Wireshark and tcpdump

**Type:** Training workflow reconstructed from introductory packet-analysis practice. No packet capture or observed incident is attached.

## Objective

Identify DNS queries and unencrypted HTTP requests in an authorized lab capture, then document what the traffic supports and what remains unknown.

## Collect a bounded lab capture

```bash
sudo tcpdump -D
# Replace <lab-interface> with the correct interface from the list.
sudo tcpdump -i <lab-interface> -nn -c 50 -w lab-traffic.pcap
```

The placeholder must be replaced before running the command. Capture only traffic you are authorized to inspect. A packet-count limit can still wait indefinitely on a quiet interface; stop with Ctrl+C when sufficient traffic is collected.

## Inspect the capture

```bash
tcpdump -nn -r lab-traffic.pcap -c 10
```

Open the file in Wireshark and apply display filters:

| Question | Display filter | Fields to inspect |
|---|---|---|
| Which DNS requests are visible? | `dns.flags.response == 0` | Query name, type, source, destination |
| Which DNS responses failed? | `dns.flags.response == 1 && dns.flags.rcode != 0` | Response code and matching query |
| Which HTTP requests are visible? | `http.request` | Host, method, URI |
| What traffic involves a chosen lab host? | `ip.addr == 192.0.2.10` | Timing, peers, protocols |

192.0.2.10 is a documentation example, not an observed host. These are Wireshark display filters, not tcpdump capture-filter syntax.

## Analysis boundaries

Match queries and responses using transaction and endpoint context. Inspect repeated failures, unexpected destinations, and unusual timing, then compare against expected lab activity. A DNS query does not prove a connection succeeded. Port 80 alone does not prove HTTP, and HTTPS payloads ordinarily cannot be read from an undecrypted capture. Encrypted DNS and incomplete captures also limit visibility.

## Report format

Record the capture scope, time zone, relevant frame numbers, endpoints, protocol details, hypothesis, supporting evidence, and unanswered questions. Avoid declaring traffic malicious based only on a port, unfamiliar domain, or isolated packet.

## Evidence status

Add a sanitized capture summary and redacted screenshots after repeating this lab. No packet counts, malicious domains, or incident findings are asserted here.
