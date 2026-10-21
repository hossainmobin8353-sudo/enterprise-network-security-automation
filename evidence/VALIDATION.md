# Offline Validation Evidence

Validated in a Linux-based Python runtime on 2026-10-21.

- **20/20 automated tests passed:** 16 unit tests and 4 end-to-end CLI integration tests.
- **Synthetic drift findings:** one medium baseline divergence, two critical policy findings on CORE-SW1.
- **Approval workflow:** valid simulated approvals work; invalid, expired, wrong-device, wrong-hash tokens rejected.
- **All remediation is simulation-only**; there are no network device connections or configuration-writing operations.
- **Not tested:** Windows PowerShell setup script, GitHub Actions runner, GNS3/EVE-NG, actual Cisco IOS syntax, OSPF adjacency, packet forwarding/segmentation, physical network gear.

Files:
- `test-results.txt` — executed test log
- `synthetic-drift-report.json` — generated offline scan
- `remediation-plan.json` — generated text diff/change plan
