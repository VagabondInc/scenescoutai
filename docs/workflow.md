# Workflow

## Step 1: Prepare script

Use a simple Markdown script format with section headings.

## Step 2: Prepare archive metadata

Use JSON metadata describing the footage library.

## Step 3: Generate package plan

Run:

```bash
python examples/workflows/demo_script_to_package.py
```

## Step 4: Review output

Open:

```text
examples/output/sample_package_plan.json
```

## Step 5: Human review

Every matched clip and generated prompt should be reviewed by a human editor.
