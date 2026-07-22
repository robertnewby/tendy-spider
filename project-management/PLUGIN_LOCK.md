# Obsidian plugin lock

Verified **2026-07-19** against the installed Obsidian desktop app, version
**1.12.7**.

| Plugin | Version | Minimum Obsidian | Release |
| --- | --- | ---: | --- |
| Tasks | 8.2.2 | 1.8.7 | https://github.com/obsidian-tasks-group/obsidian-tasks/releases/tag/8.2.2 |
| QuickAdd | 2.12.3 | 1.11.4 | https://github.com/chhoumann/quickadd/releases/tag/2.12.3 |
| Kanban | 2.0.51 | 1.0.0 | https://github.com/obsidian-community/obsidian-kanban/releases/tag/2.0.51 |

QuickAdd 2.12.3 is intentionally pinned because QuickAdd 2.13.0 and later
require Obsidian 1.13.0. Upgrade the Obsidian app before advancing that pin.

## SHA-256

```text
Tasks main.js       5c68dd0f4e1838f3bd263df39aa508d66ed94e85cc4a48bb338170be2955e077
Tasks manifest.json db6fe0eb4f033955cdae3e545a39f69748c87262ea8b352805662c4ccbcb714b
Tasks styles.css    32b3d394b697a058f2dcaef0d38476b3c3e585aea63549a816bcc237cf3e3872

QuickAdd main.js       a0c59ebed18ab870e7b9dc5f70b84e5730bb15116dba673c8fd6ce90f0aeaf90
QuickAdd manifest.json 60625157623a60e143aa26ab1823fd10e2361d12b2eb946792a555839231e7d5
QuickAdd styles.css    7198c40b23c4b1ba825156f376855e6122ed8a7f8792e6bd813ebb86534e133e

Kanban main.js       a7e3bd4cf25f9b7f53a841c44ce990db0ef5f7954ebcab17ae6dca80310c39ac
Kanban manifest.json 24976787097ead467969e014a35654e7a80e4db49a977689a48afadfa15e1854
Kanban styles.css    ecf6dd31f1727c441cce6f54794b0d3916dcfffc87fa17b855c79ba04a85d9a7
```

The GitHub release API publishes digests for Tasks and QuickAdd. Kanban's older
release does not publish digests; its values above are checksums of the named
official 2.0.51 release assets retrieved on the verification date.

Install or repair the local bundles with:

```bash
./scripts/install_obsidian_plugins.sh
```
