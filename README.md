<p align="center">
  <img src="assets/overview.svg" alt="Visual overview of OCR and Documents" width="100%">
</p>

# OCR and Documents

> Extract text and structure from PDFs and scans using OCR and document parsers.

This repository packages a single, reusable Hermes skill as a documentation-first public reference. It explains the problem, operating contract, safety boundaries, expected evidence, and example usage without claiming a bundled runtime that is not present.

## Why this exists

Tool integrations can create accidental side effects when authentication, scope, preview, execution, and verification are not separated. **OCR and Documents** turns that work into an explicit sequence with visible inputs, outputs, review points, and completion evidence.

## Why the repository has this name

The shared `hermes-skill-` prefix identifies this as a portable Hermes workflow package. `ocr-and-documents` names the capability directly—ocr and documents—so the repository remains searchable and understandable outside the original AI-OS workspace. The public title is **OCR and Documents**.

## At a glance

| Question | Answer |
| --- | --- |
| What is it? | Tool and service workflow packaged as a reusable Hermes `SKILL.md`. |
| What does it do? | Extract text and structure from PDFs and scans using OCR and document parsers. |
| Who is it for? | Builders, operators, and reviewers who want a repeatable, inspectable workflow. |
| What is delivered? | A skill contract, examples, safety guidance, release checks, and rendered SVG diagrams. |
| Runtime status | Documentation-first reference package; connect it to the tools available in your own environment. |

## How it works

<p align="center">
  <img src="assets/workflow.svg" alt="Step-by-step workflow for OCR and Documents" width="760">
</p>

1. Confirm the target service and requested operation
2. Check access without exposing credentials
3. Inspect current state and narrow the target
4. Preview any consequential change
5. Execute only the approved bounded action
6. Re-read the target and report the verified result

See [How it works](docs/HOW-IT-WORKS.md) for the detailed walkthrough, decision points, and verification checklist.

## Inputs

- The target tool, workspace, or local runtime
- A precisely scoped read or write request
- Existing authorized credentials supplied by the environment

## Outputs

- A preview or completed bounded operation
- A verification record of what changed
- Explicit blockers when authorization or state is ambiguous

## Example request

> In a disposable test workspace, extract text and structure from PDFs and scans using OCR and document parsers. Return the result, the evidence used to verify it, and any limitations or actions that still require approval.

More scenarios and expected results are in [Examples](docs/EXAMPLES.md).

## Safety and trust model

<p align="center">
  <img src="assets/safety-boundary.svg" alt="Safety and approval boundaries for OCR and Documents" width="900">
</p>

This workflow is designed around inspection and evidence; uncertainty must remain visible. It must stop when ownership, authorization, target state, or publication safety is ambiguous. Never place credentials, private endpoints, personal data, or environment-specific secrets in the skill package or its evidence.

Read [SAFETY.md](SAFETY.md) and [SECURITY.md](SECURITY.md) before connecting the workflow to real accounts, devices, repositories, or production data.

## What this repository does not claim

- It does not bypass authentication, silently broaden permissions, or perform unrelated account changes.
- It is not a hosted service, executable application, or vendor endorsement.
- It does not include credentials, private infrastructure, or the original personal AI-OS configuration.
- A successful example does not prove production readiness for every environment.

## Repository map

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Concise trigger conditions and operating workflow used by an agent. |
| `docs/PRODUCT.md` | Problem framing, audience, boundaries, and readiness model. |
| `docs/HOW-IT-WORKS.md` | Expanded walkthrough with diagrams and verification points. |
| `docs/EXAMPLES.md` | Realistic safe, review-only, and stop-condition scenarios. |
| `docs/RELEASE.md` | Checks to complete before publishing a revision. |
| `assets/*.svg` | Accessible, GitHub-rendered visual explanations. |
| `tests/README.md` | Manual contract and package validation guidance. |
| `SAFETY.md` / `SECURITY.md` | Operational and disclosure boundaries. |

## Use this package

1. Read `SKILL.md` and confirm its trigger matches your task.
2. Copy the package into the skill location supported by your agent environment, or use it as a reference when authoring an equivalent workflow.
3. Replace tool assumptions with the tools actually available to you; do not add secrets to the repository.
4. Run the smallest safe example from `docs/EXAMPLES.md`.
5. Record verification evidence and review any consequential action before widening scope.

## Contributing

Improvements are welcome when they preserve narrow scope, honest capability claims, safe defaults, and reproducible verification. See [CONTRIBUTING.md](CONTRIBUTING.md).
