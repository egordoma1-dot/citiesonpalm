# Security

## Reporting

Report vulnerabilities to **security@citiesonpalm.org** (PGP key in `SECURITY_KEY.asc`). Do not open a public issue.

- Acknowledgement within 72 hours.
- Assessment within 14 days.
- Coordinated disclosure: 90 days, or on fix, whichever is sooner. We will not ask you to extend an embargo indefinitely.
- We do not litigate good-faith research. We will name you in the advisory unless you ask us not to.

---

## Threat model

We assume the adversary is well-resourced, patient, and may be a state. We design for that rather than for opportunistic abuse.

| Adversary | Goal | Primary defence |
|---|---|---|
| **State actor** | Alter or remove records; identify readers | Federation (no centre to seize); no reader identity to obtain; append-only log; mirrored content-addressed dumps |
| **Political operation** | Astroturf ratings and complaints at scale | Physical write path: one key, one person, in person, per jurisdiction. Scale attack requires physical presence at scale. |
| **Commercial actor** | Suppress a procurement record; obtain reader data | Immutability; publication of takedown attempts; no reader data exists |
| **Opportunistic attacker** | Deface the public surface | Serving plane is read-only replica with no write path; compromise yields nothing writable |
| **Insider (Steward)** | Quietly rewrite history | Content addressing + independent mirrors make divergence detectable; Assembly suspension; fork |
| **Aggregator** | Build a surveillance product from public records | Query layer refuses natural-person result sets; bulk dumps carry the same restriction |

---

## The read surface

There is no reader identity. No accounts, no sessions, no cookies, no analytics, no third-party scripts, no CDN-hosted fonts, no persistent request logs.

This is a security property, not a policy: **we cannot disclose what we do not hold.** A subpoena for "who viewed this bridge's passport" has no answer. A breach of the serving plane exposes a read-only copy of data that is already published in bulk.

---

## The write surface

Detail in [ARCHITECTURE.md § 4](ARCHITECTURE.md#4-the-write-path).

- Terminals have **no wireless hardware**. Not disabled — absent. A Wi-Fi radio that can be re-enabled by firmware is not an air gap.
- Isolated wired segment, port-authenticated (802.1X + MACsec or equivalent). Plugging an unenrolled device into a socket yields nothing.
- No route to the internet in either direction. Receipts move to the canonical store by controlled transfer or unidirectional gateway.
- One hardware key per person per jurisdiction. Identity verified in person; **identity data never enters the platform** — only a one-way commitment held by the issuing authority, sufficient to answer "does this person already have a key?" and nothing else.
- Key loss: fee plus a reissue delay of weeks. The delay is a control. Instant reissue is a Sybil factory.
- Write receipts use a rotating per-epoch pseudonym: Sybil detection within an epoch, no permanent per-person dossier across epochs.

---

## The corrupt clerk

The sharpest edge in the model. A human must stand between a physical person and a write credential — someone has to look at the document and the face. That human can be bought.

We do not claim to prevent this. We claim to make it **cheap to detect and expensive to scale**. Five controls, in order of importance:

### 1. The public issuance ledger

Every key ever minted is published: serial, office, clerk pseudonym, timestamp, event type. Nothing about the citizen — no name, no document number, no hash of either. Schema in [DATA_MODEL.md § 8](DATA_MODEL.md#8-the-issuance-ledger).

Serials are **monotonic per office and never reused**. This single property does most of the work:

- **A gap is a question.** A missing serial is a key minted and unaccounted for. The office answers publicly, or its silence is public.
- **Rate anomalies are visible without any personal data.** One clerk pseudonym, 430 issuances in a week, against an office median of 40. You do not need to know who any of those citizens were to see that.
- **Reissue farming surfaces.** Loss-and-reissue rates per clerk are published. A Sybil operation looks like an implausible run of clumsy citizens.

The clerk is not caught by an auditor. The office's numbers simply look wrong, in daylight, to anyone who cares to look.

### 2. Split the trust

Today one clerk performs three acts: verify the document, derive the identity commitment, enrol the key. Separate them.

- The clerk verifies **the person against the document**. That is a human judgement and stays human.
- A **tamper-evident reader** — not the clerk — reads the document and derives the commitment. The clerk cannot hand-key the input.
- The key is enrolled by a device the clerk cannot address directly.

A clerk who wants a ghost key must now defeat hardware, not merely lie.

### 3. Bind uniqueness to something the clerk does not control

The identity commitment derives from the document's **issuer-attested value** — chip signature or equivalent — not from data a clerk types. If a clerk can type the input, a clerk can invent citizens. If the input must come from a genuine state-issued credential, minting a fraudulent key requires forging a passport: a different, far harder crime, against which the state already spends enormous sums.

### 4. Two-person issuance for the risky cases

Normal issuance: one clerk. **Reissuance after loss**, or **any issuance in an office already flagged for anomalous rates**: two clerks, different shifts, both signing the ledger entry. This roughly squares the cost of collusion, and it applies precisely where the fraud incentive concentrates.

### 5. Cap the blast radius, do not delete

If an office or a serial range is later found compromised, we do **not** delete its writes. Append-only means append-only, and a platform that deletes inconvenient history on the say-so of an investigation is not one anybody should trust.

Instead, affected feedback receives `issuance_flag: contested_issuance` from the finding forward. The records survive and remain readable. Their weight in aggregates does not. The finding is itself a public revision, with an author and a date.

### What this does not do

It does not stop a determined clerk from issuing a **handful** of bad keys. It stops them issuing ten thousand, and it makes the handful visible after the fact.

That is the honest ceiling. We state it here rather than claiming the problem is closed, because a security document that oversells is worse than none.

---

## Other residual risks

- **Compromised terminal.** Can forge writes from its own physical location. Bounded by throughput — one terminal, one queue, one office, opening hours — and by the issuance ledger, which makes the office's volume anomalous.
- **Coercion of a key holder.** Not defensible by technical means. We do not claim otherwise.
- **Collusion between a clerk and the oversight body auditing them.** The ledger is public, so the *data* to detect this is available to journalists and to other Stewards even when the local overseer is compromised. That is the point of publishing it rather than merely auditing it internally.

---

## Data integrity

- Append-only, content-addressed revision log.
- Independent mirrors held by other Stewards; divergence is detectable by hash comparison.
- Bulk dumps published on a fixed schedule and signed.
- Hard deletion occurs only under legal order, is logged as a public event, and does not propagate across Stewards.

---

## Out of scope

- Vulnerabilities in third-party data sources we ingest from. Report those to the source; tell us so we can flag affected records.
- Social engineering of civic office staff. Report to the Steward and the office.
- Denial of service against the public read surface. It is a cacheable read-only replica; we will fix it, but it is not a confidentiality or integrity event, and we will not treat it as one.
