# Command Center

Daily operations dashboard. Generated from YAML task data + live git metadata.
Single-file HTML. No server required — open in any browser.

---

## Generate

```bash
./regen.sh
```

Backs up current HTML, generates new HTML to a temp file, validates size delta,
promotes if safe, prunes old backups to keep last 10.

Output: `~/Downloads/{SLUG}-COMMAND-CENTER.html`
where `{SLUG}` comes from `data/tasks.yaml` → `meta.slug`.

---

## Edit tasks

Edit `data/tasks.yaml` only.
Never edit `generate.py` for task content — the generator is pure logic.

```yaml
modules:
  - id: auth
    name: Authentication
    status: shipped        # shipped | in_progress | planned
    tasks:
      - id: AUTH-1
        title: "JWT middleware"
        status: done       # done | in_progress | queued | blocked
        notes: "Shipped in migration 003."
```

---

## Adopt for a new project

```bash
# 1. Copy this folder into your project repo
cp -r path/to/command-center-template your-project/command-center

# 2. Edit the meta block in data/tasks.yaml
#    Set: slug, product, repo_path

# 3. Replace example modules with your own

# 4. Test
cd your-project/command-center
python3 generate.py --output /tmp/test.html
open /tmp/test.html   # verify it renders

# 5. Wire the regenerator
chmod +x regen.sh
./regen.sh
```

---

## Recover from a bad regen

```bash
# List backups
ls -lt backups/

# Restore the most recent backup
cp backups/{SLUG}-COMMAND-CENTER.TIMESTAMP.html ~/Downloads/{SLUG}-COMMAND-CENTER.html
```

`regen.sh` keeps the last 10 backups. If the new HTML is >20% smaller than the old,
it aborts automatically and leaves the old HTML in place.

---

## Structure

```
command-center/
├── data/
│   ├── tasks.yaml           # EDIT THIS for task content
│   └── tasks.yaml.example   # reference copy — do not delete
├── generate.py              # pure function: data + git → HTML
├── regen.sh                 # safe wrapper: backup → validate → generate
├── backups/                 # auto — last 10 HTML snapshots (.gitignored)
├── .gitignore
└── README.md                # this file
```

---

## Why the 20% shrink guard?

The HTML grows as tasks accumulate — typically 3-8% per sprint.
A 20% drop almost always means a module was accidentally removed from YAML.
The guard prevents silent data loss. If it triggers, inspect `data/tasks.yaml`
and compare with the backup before proceeding.
