# Simulator deployment and evidence plan (NOT YET EXECUTED)

Use only owned/authorized Cisco-compatible virtual devices in GNS3 or EVE-NG. IOS feature support varies.

1. Create three nodes: `EDGE-R1`, `CORE-SW1` (L3 switch), `ACCESS-SW1` (L2 switch). Add one host to VLAN 10, one guest in VLAN 30, one management host in VLAN 99.
2. Connect edge to core with a routed link (not included in current template; choose free /30 subnet and add matching interfaces). Connect core to access using an 802.1Q trunk, matching port names to image.
3. Apply baseline configs after reviewing and adapting interface names, passwords, privilege access, OSPF advertising, and licensing.
4. Validate `show vlan brief`, `show interfaces trunk`, `show ip route`, `show ip ospf neighbor`, `show access-lists`, `show running-config`.
5. Validate allowed flows, and **deny guest VLAN 30 -> management VLAN 99**. Also verify authorized DHCP and DNS by creating controlled test services; these are not configured in these templates.
6. Create one controlled drift event by removing the guest ACL inbound binding in the simulator; re-export the running config as `configs/observed/CORE-SW1.cfg` and execute `netguard scan`.
7. Create a change ticket, generate a plan, request approval, and restore baseline **manually using the simulator console**; re-export and verify `netguard scan` returns no critical findings.
8. Capture sanitized screenshots and CLI output in `evidence/simulator/`, documenting lab image versions and test environment.

**Do not claim:** routed OSPF neighbor establishment, real device rollback, DHCP relay, physical hardware validation, or successful network segmentation until simulator evidence exists.
