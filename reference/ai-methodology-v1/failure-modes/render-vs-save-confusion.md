# Render vs Save Confusion

## What happens

A generator system produces output — an HTML dashboard, a PDF report, a compiled configuration file. Someone edits the output directly, because it is right there and the edit is small. The next time the generator runs, it regenerates the output from the source data. The manual edit is gone.

Alternatively: someone edits the generator logic without realising that the output is currently serving as the source of truth for some data. The generator runs. The data disappears.

Both variants produce the same result: invisible data loss. The output looks correct. The data is gone.

## Why it happens

The output looks like a document. Documents are edited. The mental model of "this is generated output" breaks down when the output is a file you can open and change.

The confusion is especially acute when:
- The generator is rarely run (so the output feels stable)
- The output file contains both rendered content and embedded data (mixed concerns)
- There is no visible marker in the output that says "this file is generated — do not edit"

## How it escalates

1. Output file is generated and looks correct.
2. Someone adds a task directly to the output HTML ("I'll just add it here, I'll update the generator later").
3. Later never comes.
4. The generator runs again (triggered by an unrelated update).
5. The output is regenerated from source data that does not contain the manually-added task.
6. The task is gone. The file looks correct. Nobody notices until the task is due.

Born from: a dashboard generator used `open("w")` to write to the output file. The file also contained tasks that had been added manually between generator runs. The generator ran with stale in-memory state. All manually-added content was overwritten. 1.5 hours of task history was lost before the pattern was identified and the architecture was separated.

## Defence

**1. Separate data from logic from output.**

Three files, three concerns:

```
data.yaml       ← source of truth (human-editable, version-controlled)
generate.py     ← pure function: reads data.yaml, writes output.html
output.html     ← disposable (generated, never edited directly)
```

The data file is version-controlled. Edits to data go in the data file. The output is regenerated from the data file. If the output is deleted, running the generator restores it exactly.

**2. Output files are marked as generated.**

The first line of every generated file:
```html
<!-- GENERATED FILE — DO NOT EDIT. Edit data.yaml and run generate.py -->
```

```python
# GENERATED FILE — DO NOT EDIT. Edit data.yaml and run generate.py
```

This is not documentation. It is a warning sign that catches the "I'll just edit it here" impulse.

**3. Generator is idempotent.**

Running the generator twice on the same data produces the same output. A generator that produces different output on subsequent runs with the same input is a generator that cannot be trusted.

**4. Version-control the data file, not the output file.**

The data file is committed to git. The output file is `.gitignore`-d or treated as build artefact. This makes the data file the obvious source of truth and the output file obviously disposable.

**5. Pre-write size check.**

Before the generator writes output, compare the expected output size to the previous output size. A drop of more than 20% aborts the write with an error. This catches the case where the generator is running with incomplete data.
