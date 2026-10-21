# Validation matrix

| Check | Evidence | Status |
|---|---|---|
| Synthetic inventory three devices | Python unit tests | Automated |
| Guest-to-management ACL removal found | Unit and CLI tests | Automated |
| Config diff and remediation plan | Unit and CLI tests | Automated |
| Wrong device / hash / expired HMAC rejected | Unit tests | Automated |
| No config writes performed | Source inspection; simulate command | Offline behavior |
| VLAN isolation ICMP/TCP validation | GNS3 or EVE-NG | NOT TESTED |
| OSPF neighbor adjacency/routing | GNS3 or EVE-NG | NOT TESTED |
| Real IOS syntax and feature support | GNS3 or EVE-NG | NOT TESTED |
| Config recovery after human approval | Simulator console + evidence | NOT TESTED |

Static policy parsing is intentionally a limited subset, **not** a complete Cisco IOS parser: this demo uses text matching and requires lab verification and human review.
