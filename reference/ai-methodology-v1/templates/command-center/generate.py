"""Command Center generator.

Reads data/tasks.yaml + pulls live git metadata, renders a single-file
HTML dashboard to ~/Downloads/{SLUG}-COMMAND-CENTER.html.

Usage:
    python3 generate.py
    python3 generate.py --output /tmp/test.html

Palette: metallic gray background, orange accent (#F39237), Arial font.
No external dependencies beyond PyYAML (pip install pyyaml).
"""

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

HERE = Path(__file__).parent
DATA_PATH = HERE / "data" / "tasks.yaml"


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def _git(repo: Path, *args: str) -> str:
    try:
        r = subprocess.run(
            ["git", "-C", str(repo)] + list(args),
            capture_output=True, text=True, timeout=5,
        )
        return r.stdout.strip()
    except Exception:
        return ""


def git_meta(repo: Path, product: str) -> dict:
    branch = _git(repo, "branch", "--show-current") or "unknown"
    head_sha = _git(repo, "rev-parse", "--short", "HEAD") or "?"
    head_subject = _git(repo, "log", "-1", "--format=%s") or "no commits"
    commits_total_raw = _git(repo, "rev-list", "--count", "HEAD") or "0"
    commits_total = int(commits_total_raw) if commits_total_raw.isdigit() else 0

    tags_raw = _git(repo, "tag", "-l", "stable-v*", "--sort=-v:refname")
    tags = [t for t in tags_raw.splitlines() if t]
    latest_stable = tags[0] if tags else "none"

    today_raw = _git(repo, "log", "--since=midnight", "--format=%h|%s")
    today_commits = [l for l in today_raw.splitlines() if l]

    return {
        "product": product,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "branch": branch,
        "head_sha": head_sha,
        "head_subject": head_subject,
        "commits_total": commits_total,
        "stable_tags": len(tags),
        "latest_stable": latest_stable,
        "today_count": len(today_commits),
        "today_commits": today_commits,
    }


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

STATUS_ORDER = ["in_progress", "queued", "blocked", "done", "shipped", "planned"]


def task_counts(tasks: list) -> dict:
    counts = {"total": len(tasks), "done": 0, "in_progress": 0, "queued": 0, "blocked": 0}
    for t in tasks:
        s = t.get("status", "queued")
        if s in counts:
            counts[s] += 1
    return counts


def pct_done(tasks: list) -> int:
    if not tasks:
        return 0
    done = sum(1 for t in tasks if t.get("status") in ("done", "shipped"))
    return round(done * 100 / len(tasks))


# ---------------------------------------------------------------------------
# HTML escaping
# ---------------------------------------------------------------------------

def esc(s: object) -> str:
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ---------------------------------------------------------------------------
# HTML fragment builders
# ---------------------------------------------------------------------------

CSS = """
:root {
  --accent:      #F39237;
  --accent-deep: #d4751d;
  --accent-soft: #FFF3E8;
  --g-900: #1A1A2E;
  --g-700: #2d2d4a;
  --g-500: #64748b;
  --g-400: #94a3b8;
  --g-300: #cbd5e1;
  --g-200: #e2e8f0;
  --g-150: #eef2f7;
  --g-100: #f1f5f9;
  --g-75:  #f8fafc;
  --white: #ffffff;
  --surface: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
  --border: 1px solid #e2e8f0;
  --border-soft: 0.5px solid #eef2f7;
  --radius: 12px;
  --radius-sm: 8px;
  --radius-xs: 6px;
  --radius-pill: 999px;
  --shadow-1: 0 1px 3px rgba(0,0,0,0.04);
  --shadow-2: 0 2px 8px rgba(0,0,0,0.06);
  --shadow-3: 0 4px 16px rgba(0,0,0,0.08);
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: Arial, -apple-system, sans-serif;
  font-size: 13px;
  background: #eef2f7;
  color: var(--g-900);
  min-height: 100vh;
}

.page-wrap { max-width: 1280px; margin: 0 auto; padding: 24px 20px; }

/* Header */
.topbar {
  background: var(--g-900);
  color: #e2e8f0;
  padding: 14px 24px;
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 20px;
  border-radius: var(--radius);
  box-shadow: var(--shadow-3);
}
.topbar h1 { font-size: 20px; font-weight: 700; color: #fff; }
.topbar h1 span { color: var(--accent); }
.topbar .meta { font-size: 11px; color: var(--g-400); display: flex; gap: 16px; align-items: center; }
.topbar .meta code {
  font-family: "SF Mono", Menlo, monospace; font-size: 10px;
  background: rgba(255,255,255,0.08); padding: 2px 6px;
  border-radius: var(--radius-xs); color: #cbd5e1;
}
.branch-pill {
  background: var(--accent); color: #fff;
  padding: 2px 10px; border-radius: var(--radius-pill);
  font-size: 10px; font-weight: 700; text-transform: uppercase;
}
.tag-pill {
  background: rgba(16,185,129,0.18); color: #6ee7b7;
  border: 1px solid rgba(16,185,129,0.3);
  padding: 2px 9px; border-radius: var(--radius-pill);
  font-size: 10px; font-weight: 600;
}

/* Git strip */
.gitstrip {
  display: grid; grid-template-columns: repeat(6, 1fr);
  background: #fff;
  border: var(--border);
  border-radius: var(--radius);
  padding: 16px 24px; margin-bottom: 20px;
  box-shadow: var(--shadow-2);
  gap: 0;
}
.git-cell { display: flex; flex-direction: column; gap: 4px; padding: 0 12px; }
.git-cell:first-child { padding-left: 0; }
.git-cell:last-child { padding-right: 0; }
.git-cell:not(:last-child) { border-right: 1px solid var(--g-150); }
.git-label { font-size: 9px; color: var(--g-400); font-weight: 600; letter-spacing: 0.8px; text-transform: uppercase; }
.git-value { font-size: 18px; font-weight: 700; color: var(--g-900); font-variant-numeric: tabular-nums; }
.git-value.sm { font-size: 12px; font-family: "SF Mono", Menlo, monospace; font-weight: 600; }
.git-value.accent { color: var(--accent); }

/* Module tabs */
.tabs { display: flex; gap: 4px; margin-bottom: 20px; overflow-x: auto; }
.tab-btn {
  padding: 8px 16px; border: var(--border); background: #fff;
  font-family: Arial, sans-serif; font-size: 12px; font-weight: 500;
  color: var(--g-500); cursor: pointer; white-space: nowrap;
  border-radius: var(--radius-sm); transition: all 0.15s ease;
}
.tab-btn:hover { color: var(--g-900); border-color: var(--g-300); }
.tab-btn.active {
  background: var(--accent); color: #fff; border-color: var(--accent);
  font-weight: 700; box-shadow: var(--shadow-2);
}
.badge { font-size: 10px; margin-left: 5px; opacity: 0.75; }

/* Module panel */
.module-panel { display: none; }
.module-panel.active { display: block; }

/* Module header card */
.mod-header {
  background: #fff; border: var(--border); border-radius: var(--radius);
  padding: 20px 24px; margin-bottom: 16px; box-shadow: var(--shadow-1);
}
.mod-title { font-size: 18px; font-weight: 700; color: var(--g-900); margin-bottom: 4px; display: flex; align-items: center; gap: 10px; }
.mod-desc { font-size: 12px; color: var(--g-500); margin-top: 6px; line-height: 1.5; }
.mod-progress { margin-top: 12px; display: flex; align-items: center; gap: 12px; }
.pbar-track { flex: 1; max-width: 400px; height: 6px; background: var(--g-150); border-radius: var(--radius-pill); overflow: hidden; }
.pbar-fill { height: 100%; background: var(--accent); border-radius: var(--radius-pill); }
.pbar-pct { font-size: 12px; font-weight: 600; color: var(--g-500); }
.pbar-counts { font-size: 11px; color: var(--g-400); }

/* Status badges */
.status-badge {
  display: inline-block; padding: 2px 9px;
  border-radius: var(--radius-pill); font-size: 10px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.5px;
}
.s-done         { background: #d1fae5; color: #065f46; }
.s-shipped      { background: #e0e7ff; color: #3730a3; }
.s-in_progress  { background: #fed7aa; color: #9a3412; }
.s-queued       { background: var(--g-100); color: var(--g-500); border: 1px dashed var(--g-300); }
.s-blocked      { background: #fecaca; color: #991b1b; }
.s-planned      { background: var(--g-100); color: var(--g-400); }

/* Task table */
.task-table { width: 100%; border-collapse: collapse; background: #fff; border-radius: var(--radius-sm); overflow: hidden; box-shadow: var(--shadow-1); margin-bottom: 20px; }
.task-table th { background: var(--g-75); color: var(--g-500); font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; padding: 10px 14px; text-align: left; border-bottom: 1px solid var(--g-150); }
.task-table td { padding: 10px 14px; border-bottom: 1px solid var(--g-75); font-size: 12px; vertical-align: top; }
.task-table tr:last-child td { border-bottom: 0; }
.task-table tr:hover td { background: var(--g-75); }
.task-id { font-family: "SF Mono", Menlo, monospace; font-size: 10px; font-weight: 600; background: #fef3c7; color: #78350f; padding: 2px 6px; border-radius: 4px; white-space: nowrap; }
.task-title { font-weight: 500; color: var(--g-900); line-height: 1.4; }
.task-notes { font-size: 11px; color: var(--g-500); margin-top: 3px; line-height: 1.45; }
.owner-pill { font-size: 10px; color: var(--g-500); background: var(--g-100); padding: 2px 7px; border-radius: var(--radius-pill); white-space: nowrap; }
.priority-p0 { color: #991b1b; font-weight: 700; font-size: 10px; }
.priority-p1 { color: #9a3412; font-size: 10px; }
.priority-p2 { color: var(--g-400); font-size: 10px; }

/* Sessions */
.session-card {
  background: #fff; border: var(--border); border-radius: var(--radius-sm);
  padding: 14px 18px; margin-bottom: 10px; box-shadow: var(--shadow-1);
  display: flex; gap: 16px; align-items: baseline;
}
.session-date { font-size: 11px; color: var(--g-400); min-width: 90px; }
.session-sha { font-family: "SF Mono", Menlo, monospace; font-size: 10px; color: var(--accent); }
.session-commits { font-size: 11px; color: var(--g-500); }
.session-summary { font-size: 12px; color: var(--g-700); flex: 1; line-height: 1.4; }

/* Archive */
.archive-note { font-size: 12px; color: var(--g-500); padding: 8px 0; border-bottom: 1px solid var(--g-75); line-height: 1.45; }
.archive-note:last-child { border-bottom: 0; }

/* Footer */
footer { text-align: center; color: var(--g-400); font-size: 10px; margin-top: 40px; padding-top: 16px; border-top: 1px solid var(--g-150); }
"""


def render_status_badge(status: str) -> str:
    cls = f"s-{status}"
    label = status.replace("_", " ")
    return f'<span class="status-badge {cls}">{esc(label)}</span>'


def render_task_table(tasks: list) -> str:
    if not tasks:
        return '<p style="color:#94a3b8;font-size:12px;padding:12px 0;">No tasks in this module.</p>'

    rows = []
    for t in tasks:
        tid = esc(t.get("id", ""))
        title = esc(t.get("title", ""))
        notes = esc(t.get("notes", ""))
        status = t.get("status", "queued")
        priority = t.get("priority", "")
        owner = esc(t.get("owner", ""))

        pri_cls = f"priority-{priority}" if priority else ""
        pri_html = f'<span class="{pri_cls}">{esc(priority)}</span>' if priority else ""

        notes_html = f'<div class="task-notes">{notes}</div>' if notes else ""

        rows.append(f"""
        <tr>
          <td><span class="task-id">{tid}</span></td>
          <td><div class="task-title">{title}</div>{notes_html}</td>
          <td>{render_status_badge(status)}</td>
          <td>{pri_html}</td>
          <td><span class="owner-pill">{owner}</span></td>
        </tr>""")

    rows_html = "".join(rows)
    return f"""
    <table class="task-table">
      <thead>
        <tr>
          <th style="width:90px">ID</th>
          <th>Task</th>
          <th style="width:110px">Status</th>
          <th style="width:50px">Pri</th>
          <th style="width:120px">Owner</th>
        </tr>
      </thead>
      <tbody>{rows_html}</tbody>
    </table>"""


def render_module_panel(mod: dict, active: bool) -> str:
    mid = esc(mod.get("id", ""))
    name = esc(mod.get("name", ""))
    status = mod.get("status", "planned")
    version = esc(mod.get("version", ""))
    desc = esc(mod.get("description", ""))
    tasks = mod.get("tasks", [])

    counts = task_counts(tasks)
    pct = pct_done(tasks)
    version_html = f' <span class="status-badge s-shipped" style="font-size:9px">{version}</span>' if version else ""
    active_cls = " active" if active else ""

    return f"""
<div id="panel-{mid}" class="module-panel{active_cls}">
  <div class="mod-header">
    <div class="mod-title">{name}{version_html} {render_status_badge(status)}</div>
    <div class="mod-desc">{desc}</div>
    <div class="mod-progress">
      <div class="pbar-track"><div class="pbar-fill" style="width:{pct}%"></div></div>
      <span class="pbar-pct">{pct}%</span>
      <span class="pbar-counts">{counts['done']}/{counts['total']} done
        &nbsp;·&nbsp; {counts['in_progress']} active
        &nbsp;·&nbsp; {counts['queued']} queued
        {f"&nbsp;·&nbsp; <span style='color:#991b1b;font-weight:600'>{counts['blocked']} blocked</span>" if counts['blocked'] else ""}
      </span>
    </div>
  </div>
  {render_task_table(tasks)}
</div>"""


def render_tabs(modules: list) -> str:
    tabs = []
    for i, mod in enumerate(modules):
        mid = esc(mod.get("id", ""))
        name = esc(mod.get("name", ""))
        tasks = mod.get("tasks", [])
        counts = task_counts(tasks)
        active_cls = " active" if i == 0 else ""
        tabs.append(
            f'<button class="tab-btn{active_cls}" onclick="showTab(\'{mid}\')">'
            f'{name}<span class="badge">{counts["total"]}</span>'
            f'</button>'
        )
    return '<div class="tabs">' + "".join(tabs) + "</div>"


def render_gitstrip(meta: dict) -> str:
    cells = [
        ("Branch", f'<span class="branch-pill">{esc(meta["branch"])}</span>', False),
        ("HEAD", f'<span class="git-value sm">{esc(meta["head_sha"])}</span>', False),
        ("Commits", str(meta["commits_total"]), True),
        ("Stable tags", str(meta["stable_tags"]), False),
        ("Latest stable", f'<span class="tag-pill">{esc(meta["latest_stable"])}</span>', False),
        ("Today", str(meta["today_count"]), True),
    ]
    parts = []
    for label, value, is_big in cells:
        val_cls = "git-value accent" if is_big else "git-value sm"
        if is_big:
            val_html = f'<span class="git-value accent">{value}</span>'
        else:
            val_html = value
        parts.append(f'<div class="git-cell"><span class="git-label">{label}</span>{val_html}</div>')
    return '<div class="gitstrip">' + "".join(parts) + "</div>"


def render_sessions(sessions: list) -> str:
    if not sessions:
        return "<p style='color:#94a3b8;font-size:12px'>No sessions logged yet.</p>"
    cards = []
    for s in sessions:
        date = esc(s.get("date", ""))
        agent = esc(s.get("agent", ""))
        commits = s.get("commits", 0)
        sha = esc(s.get("tip_sha", ""))
        summary = esc(s.get("summary", ""))
        cards.append(f"""
        <div class="session-card">
          <span class="session-date">{date}</span>
          <span class="session-sha">{sha}</span>
          <span class="session-commits">{commits} commits</span>
          <span class="session-summary">{summary}</span>
        </div>""")
    return "".join(cards)


def render_archive(notes: list) -> str:
    if not notes:
        return "<p style='color:#94a3b8;font-size:12px'>No archive notes yet.</p>"
    return "".join(f'<div class="archive-note">{esc(n)}</div>' for n in notes)


JS = """
function showTab(id) {
  document.querySelectorAll('.module-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  const panel = document.getElementById('panel-' + id);
  if (panel) panel.classList.add('active');
  document.querySelectorAll('.tab-btn').forEach(b => {
    if (b.textContent.trim().startsWith(
      panel ? panel.querySelector('.mod-title') ? '' : '' : ''
    )) {}
  });
  // match tab by onclick attribute content
  document.querySelectorAll('.tab-btn').forEach(b => {
    if (b.getAttribute('onclick') === "showTab('" + id + "')") {
      b.classList.add('active');
    }
  });
}
"""


# ---------------------------------------------------------------------------
# Main renderer
# ---------------------------------------------------------------------------

def render_html(data: dict, meta: dict) -> str:
    modules = data.get("modules", [])
    sessions = data.get("sessions", [])
    archive_notes = data.get("archive_notes", [])
    product = esc(meta["product"])

    # summary stats across all modules
    all_tasks = [t for m in modules for t in m.get("tasks", [])]
    all_counts = task_counts(all_tasks)
    overall_pct = pct_done(all_tasks)

    tabs_html = render_tabs(modules)
    panels_html = "".join(render_module_panel(m, i == 0) for i, m in enumerate(modules))
    gitstrip_html = render_gitstrip(meta)
    sessions_html = render_sessions(sessions)
    archive_html = render_archive(archive_notes)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{product} — Command Center</title>
<style>{CSS}</style>
</head>
<body>
<div class="page-wrap">

  <div class="topbar">
    <h1>{product} <span>Command Center</span></h1>
    <div class="meta">
      <span>{esc(meta['updated'])}</span>
      <code>{esc(meta['head_subject'][:60])}</code>
      <span>{overall_pct}% complete &nbsp;|&nbsp; {all_counts['done']}/{all_counts['total']} tasks done</span>
    </div>
  </div>

  {gitstrip_html}

  {tabs_html}

  {panels_html}

  <!-- Sessions timeline -->
  <div style="margin-top:32px">
    <h3 style="font-size:14px;font-weight:700;color:#1A1A2E;margin-bottom:14px;padding-bottom:8px;border-bottom:1px solid #e2e8f0;">
      Session Log
    </h3>
    {sessions_html}
  </div>

  <!-- Archive notes -->
  <div style="margin-top:28px">
    <h3 style="font-size:14px;font-weight:700;color:#1A1A2E;margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid #e2e8f0;">
      Archive Notes
    </h3>
    {archive_html}
  </div>

  <footer>
    Generated {esc(meta['updated'])} &nbsp;|&nbsp;
    {esc(meta['branch'])} @ {esc(meta['head_sha'])} &nbsp;|&nbsp;
    {all_counts['total']} tasks across {len(modules)} modules
  </footer>
</div>
<script>{JS}</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Command Center generator")
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output HTML path. Defaults to ~/Downloads/{SLUG}-COMMAND-CENTER.html",
    )
    args = parser.parse_args()

    if not DATA_PATH.exists():
        print(f"ERROR: {DATA_PATH} not found.", file=sys.stderr)
        print("Copy data/tasks.yaml.example to data/tasks.yaml and fill it in.", file=sys.stderr)
        sys.exit(1)

    data = yaml.safe_load(DATA_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        print("ERROR: tasks.yaml must be a YAML mapping at the top level.", file=sys.stderr)
        sys.exit(1)

    meta_block = data.get("meta", {})
    slug = meta_block.get("slug", "PROJECT")
    product = meta_block.get("product", slug)
    repo_path_str = meta_block.get("repo_path", "")
    repo = Path(repo_path_str) if repo_path_str else HERE.parent

    output_path = Path(args.output) if args.output else (
        Path.home() / "Downloads" / f"{slug}-COMMAND-CENTER.html"
    )

    meta = git_meta(repo, product)
    html = render_html(data, meta)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")

    lines = html.count("\n")
    size_kb = len(html.encode("utf-8")) / 1024
    print(f"Generated: {output_path}")
    print(f"  {lines} lines / {size_kb:.1f} KB")
    print(f"  {meta['commits_total']} commits · branch {meta['branch']} · {meta['head_sha']}")


if __name__ == "__main__":
    main()
