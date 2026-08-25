# Product Brief: OCR and Documents

## One-sentence definition

Extract text and structure from PDFs and scans using OCR and document parsers.

## User problem

Tool integrations can create accidental side effects when authentication, scope, preview, execution, and verification are not separated. The result is often difficult to reproduce, audit, or hand to another person.

## Intended users

- Builders adding a focused capability to a Hermes-compatible agent.
- Operators who need a repeatable workflow with explicit stop conditions.
- Reviewers evaluating what happened, why it happened, and whether the result is trustworthy.
- Portfolio readers who want to understand the design without access to private infrastructure.

## Product promise

The package provides a narrow operating contract: when to invoke the skill, which evidence to inspect, how to move through the work, where to pause, and what proof is required before completion.

## Core capabilities

1. **Scope:** convert an open-ended request into a bounded target and success criteria.
2. **Operate:** follow a reviewable sequence suited to the capability.
3. **Guard:** keep authorization, privacy, and side effects explicit.
4. **Verify:** distinguish an attempted action from a confirmed result.
5. **Handoff:** return enough evidence for another person to understand or continue the work.

## Trust boundary

The default posture is evidence-first and read-oriented; any later write path requires a separate authorization decision. Credentials, personal records, private endpoints, and original AI-OS infrastructure are outside the public package.

## Non-goals

- It does not bypass authentication, silently broaden permissions, or perform unrelated account changes.
- Providing a hosted runtime, account, secret, or production environment.
- Claiming that documentation alone guarantees correct execution.
- Generalizing beyond the tools and evidence available in the adopter's environment.

## Definition of a successful run

A run is complete only when the requested output exists, the relevant checks pass, the result can be traced to the inputs, and unresolved limitations are reported. If any of those conditions cannot be met, the correct output is a clear blocker—not a success claim.

## Maturity

This is a public, documentation-first reference workflow extracted from a larger private workbench. The skill contract and publication materials are reviewable; runtime behavior depends on the adopter's tools, permissions, and test environment.
