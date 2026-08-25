# How OCR and Documents Works

This page expands the concise contract in `SKILL.md`. The diagrams are static SVG files so they render directly on GitHub on both phones and desktop browsers.

## End-to-end workflow

![Step-by-step workflow for OCR and Documents](../assets/workflow.svg)

### 1. Confirm the target service and requested operation

At this stage, record the relevant input, the decision made, and the evidence that allows the workflow to continue. If the evidence is missing or contradictory, stop and report the blocker before moving to step 2.
### 2. Check access without exposing credentials

At this stage, record the relevant input, the decision made, and the evidence that allows the workflow to continue. If the evidence is missing or contradictory, stop and report the blocker before moving to step 3.
### 3. Inspect current state and narrow the target

At this stage, record the relevant input, the decision made, and the evidence that allows the workflow to continue. If the evidence is missing or contradictory, stop and report the blocker before moving to step 4.
### 4. Preview any consequential change

At this stage, record the relevant input, the decision made, and the evidence that allows the workflow to continue. If the evidence is missing or contradictory, stop and report the blocker before moving to step 5.
### 5. Execute only the approved bounded action

At this stage, record the relevant input, the decision made, and the evidence that allows the workflow to continue. If the evidence is missing or contradictory, stop and report the blocker before moving to step 6.
### 6. Re-read the target and report the verified result

At this stage, record the relevant input, the decision made, and the evidence that allows the workflow to continue. If the evidence is missing or contradictory, stop and report the blocker before moving to step 6.

## Safety boundary

![Safety and approval boundaries for OCR and Documents](../assets/safety-boundary.svg)

The documented path is read-oriented. If the task expands into a write or external action, treat that as a new approval boundary.

The workflow must also stop when:

- The user does not own or control the target.
- Authentication exists but the requested authority is unclear.
- Inputs contain private material that is not necessary for the task.
- A result cannot be verified independently.
- The requested action conflicts with repository, platform, or organizational policy.

## Evidence model

| Stage | Evidence to retain |
| --- | --- |
| Scope | The exact request, target, constraints, and success criteria. |
| Inspection | Source files, tool output, or current-state observations actually used. |
| Decision | The reason for the selected path and any rejected alternatives that affect safety. |
| Execution | The artifact or bounded operation result—not merely an attempt message. |
| Verification | A direct check against the target and acceptance criteria. |
| Handoff | Remaining risks, withheld actions, and the smallest useful next step. |

## Reliability principles

- Prefer the smallest reversible action that can answer the request.
- Separate observed facts from interpretations.
- Never infer permission from a logged-in session alone.
- Treat failed or missing verification as an incomplete run.
- Preserve user work and avoid unrelated changes.

## Capability boundary

It does not bypass authentication, silently broaden permissions, or perform unrelated account changes. This package defines how to reason and verify; the adopter is responsible for connecting compatible tools and testing them in their own environment.
