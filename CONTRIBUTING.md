# Contributing

## Before anything else

Read [PRINCIPLES.md](PRINCIPLES.md). Most rejected proposals are rejected on principle, not on quality. A brilliant PR that adds a login to the read surface, a recommendation algorithm, or a field on a natural person will be closed without a code review, and this is not a comment on the code.

Open a Discussion before a large PR. We would rather argue about the design for two weeks than reject 3,000 lines.

---

## What we need now

Phase 0 is a specification phase. The highest-value contributions today are **not code**:

- **Adversarial review of the privacy model.** Find the aggregation attack we missed. This is the most valuable thing you can do for this project.
- **Schema stress-testing against your jurisdiction.** Does the address model survive Japan? Does the containment DAG survive an informal settlement with no cadastre? Does the office model survive a system where the mayor is appointed, not elected? Break it now.
- **Hardware-security review of the write path.** We are asserting properties about terminals and keys. Test the assertions.
- **Translation and script coverage.** The schema assumes multilingual. Prove it.

---

## Contribution types

### Code

- Reference implementation, adapters, validators, tile pipeline, clients.
- Conventional commits. One logical change per PR.
- Tests are not optional for anything touching the revision log, the validator, or the write path.
- Adapters must be independently runnable and must not require credentials we cannot publish. If a source needs a key, the adapter documents how to obtain one; it does not embed one.

### Schema

- Additive and optional by default. A required field is a breaking change.
- Any new field on an entity representing a natural person is a **Constitutional** change ([GOVERNANCE.md § 3](GOVERNANCE.md#3-change-classes)). Expect a 90-day comment period and near-unanimity. Expect to lose.
- Every schema PR includes: migration path, effect on existing revisions, and at least two real-world examples from different jurisdictions.

### Data

Data does not arrive by pull request. It arrives through **adapters** (automated, preferred) or the **contribution queue** (human, corroborated).

Human-contributed records enter at `contributed` tier and cannot be promoted by the contributor. Promotion requires corroboration from an independent source and is itself a revision with an author. There is no path from "I know this is true" to `authoritative`, and there will not be one.

You may not contribute:
- Anything about a natural person who is not an officeholder, acting in that office.
- Anything sourced from a leak, a hack, or a breach. Even if it is true. Even if it is important. We are a public-record platform; if it is not lawfully public, it is not ours. Take it to a journalist.
- Anything you cannot cite.

### Documentation

Prose contributions are welcome and are held to the same standard as code: precise, sourced, no marketing language. If a sentence could appear on a startup landing page, delete it.

---

## Review

- Routine: one TSG-delegated maintainer, lazy consensus, 72h.
- Substantial: TSG vote, 14-day public comment.
- Breaking / Constitutional: see [GOVERNANCE.md](GOVERNANCE.md).

Reviewers are asked to state which principle, if any, a rejection rests on. "I don't like it" is not a review.

---

## Conduct

[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) applies to every space this project occupies, including the Discussions where we argue about the schema, which is where most of the arguing happens.
