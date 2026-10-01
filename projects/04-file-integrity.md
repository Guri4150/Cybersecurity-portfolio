# File integrity verification with SHA-256

**Type:** Reproducible illustrative exercise based on hashing training. Results below are expected behavior, not a saved execution transcript.

## Objective

Detect a change in file content and explain the limits of hash-based verification.

Run in a new disposable lab directory so existing files are not overwritten:

```bash
mkdir integrity-demo
cd integrity-demo
printf 'Authorized configuration\n' > baseline.txt
cp baseline.txt candidate.txt
sha256sum baseline.txt candidate.txt
sha256sum baseline.txt > baseline.sha256
sha256sum -c baseline.sha256
printf 'Unexpected setting\n' >> candidate.txt
sha256sum baseline.txt candidate.txt
```

## Expected behavior

Initially both files should have the same digest because their bytes match. After appending a line to candidate.txt, its digest should differ. The manifest check verifies baseline.txt against its recorded digest; it does not verify candidate.txt.

SHA-256 comparisons provide strong practical evidence of byte equality or difference, but do not explain whether a change was authorized or malicious. Hashing alone does not authenticate a publisher or provide non-repudiation. Obtain reference hashes through a trusted channel and protect the manifest from modification.

## Evidence to capture

Save the two comparisons and the manifest check from a repeat run. Explain exactly which file was changed, where the reference digest came from, and why an integrity mismatch warrants investigation.
