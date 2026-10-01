# Linux permissions and least privilege

**Type:** Reconstructed training exercise. Commands below describe the approach; no original terminal transcript is supplied.

## Objective

Review a research team's project files and remove permissions that exceed the intended access policy.

## Approach

Inspect the working directory before changing permissions:

```bash
cd /home/researcher2/projects
pwd
ls -la
ls -ld drafts
```

Read each permission string as owner, group, and other. Hidden files require `ls -a` to appear in the listing. Check ownership as well as mode bits; permission changes do not correct an incorrect owner or group.

| Lab requirement | Example command | Intended effect |
|---|---|---|
| Remove write access for others from project_k.txt | `chmod o-w project_k.txt` | Preserves other existing permissions |
| Give only the owner read/write access to project_m.txt | `chmod u=rw,g=,o= project_m.txt` | Sets mode 600 |
| Make .project_x.txt read-only for owner/group with no other access | `chmod u=r,g=r,o= .project_x.txt` | Sets mode 440 |
| Remove group traversal of drafts | `chmod g-x drafts` | Removes group execute permission |

The project_m.txt row uses an explicit owner-only policy as a reconstruction; verify the actual exercise requirement before applying it.

## Verification and interpretation

Run `ls -la` and `ls -ld drafts` again and compare the relevant bits. Record before/after output when repeating the lab. Directory execute permission controls traversal; read permission controls listing names. Mode bits alone may not capture effective access when ACLs or privileged users are involved.

## Security value

Reducing unnecessary write permissions limits accidental modification and unauthorized changes. Least privilege should follow a documented business requirement and be checked from the affected account, not only from an administrator session.

## Evidence status

Original output is not attached. A repeat run should include sanitized before/after listings and an explanation of each permission change; do not present expected modes as observed output.
