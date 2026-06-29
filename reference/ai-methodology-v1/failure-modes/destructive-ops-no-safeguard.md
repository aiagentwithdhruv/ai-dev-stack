# Destructive Operations Without Safeguard

## What happens

A generator, script, or migration runs. It overwrites a file or drops a database object. There was no backup. There was no size check. There was no confirmation step. The data is gone.

The most common form: a Python script uses `open("w")` to write to a file. The "w" mode truncates the file before writing. If the in-memory data is incomplete, stale, or wrong, the file is overwritten with garbage. The previous content is unrecoverable without git history.

The database variant: a migration drops a column or table. Another backend consumer, still running old code, begins returning 500 errors on every request.

## Why it happens

Destructive operations feel routine. `open("w")` is how you write a file. `DROP COLUMN` is how you remove a column you no longer need. The operation is correct in intent. The problem is the lack of a safety net when the intent fails to match reality.

In generator systems, the failure often happens when:
- The data source and the output target are the same file (mixed concerns)
- The generator runs with partial or stale data
- The output file is larger than expected, indicating it contained data the generator doesn't know about

In database systems, the failure happens when:
- Destructive migrations run before all consumers are updated
- The migration sequence is run in isolation rather than as part of a coordinated deployment

## How it escalates

Generator variant:
1. Generator runs. In-memory data is partially loaded.
2. `open("w")` truncates the output file.
3. The partial data is written.
4. The rest of the file's content is gone.
5. Nobody notices until a task that was in the file is due and missing.
6. Recovery requires reconstructing from memory, chat history, or external systems — none of which are reliable.

Database variant:
1. Migration drops 2 columns.
2. Second backend consumer is still running old code that references those columns.
3. Every API request through that consumer returns 500.
4. The error is traced to the missing columns.
5. Emergency recovery: restore the columns with defaults, stop the migration, coordinate a proper deployment.

Born from: a task dashboard generator wrote to a file with `open("w")`. The file contained both generated content and manually-added task data. The generator ran with stale in-memory data. All 1.5 hours of manually-added task history was overwritten. No backup existed. The incident was the specific driver for the destructive-ops rules in this methodology.

## Defence

**1. Backup before overwriting any file over 100 lines.**

```bash
cp target.file target.file.bak.$(date +%Y%m%d_%H%M%S)
```

This takes under a second. Run it before every write that could overwrite meaningful content.

**2. 20% size drop = abort.**

```python
before = os.path.getsize(filepath)
# ... prepare content ...
after_estimate = len(content.encode())
if after_estimate < before * 0.8:
    raise RuntimeError(f"Output is {after_estimate} bytes vs {before} bytes before. Aborting — likely stale data.")
```

A file that shrinks 20% or more likely lost content. Abort before writing. Alert the human.

**3. Separate data from output. Always.**

The data file is the source of truth. The output file is disposable.

```
data.yaml    ← edited by humans, committed to git
generate.py  ← reads data.yaml, writes output
output.html  ← regenerated on every run, never edited
```

If a human wants to add data: they edit `data.yaml`. The generator is run. The output reflects the new data.

**4. Destructive DB migrations: code first, migrate second.**

Before running any migration that drops a column or table:
1. Confirm ALL backend consumers are running code that does not reference the dropped object
2. Deploy the new code to all consumers
3. Verify all consumers healthy
4. Then run the migration
5. Verify all consumers still healthy

If any consumer cannot be updated first: defer the migration. Use a `DEFAULT` value on the column to keep old code working while new code ignores it. Drop the column in the next coordinated release.

**5. State the before-vs-after before every destructive operation.**

Before running: print or log:
- Current state (file size, row count, column list)
- Expected state after the operation
- What will be irreversibly changed

Get confirmation (human or automated size check) before proceeding.
