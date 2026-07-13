# FAQ

The questions worth answering are the hostile ones. Some of these do not have good answers, and where that is the case we say so.

---

**Is this just OpenStreetMap?**

No, and we depend on OSM rather than competing with it. OSM answers *what and where*. Cities On Palm answers *who owns it, what it cost, who is accountable, and what happened to it*. Geometry is an input to us. Accountability data is the product.

---

**Why no accounts for reading? Wouldn't accounts help with abuse?**

Accounts would help with abuse on a system where reading and writing share a surface. Ours do not. Reading is anonymous because a platform that records who investigated which public official is a surveillance tool aimed at exactly the people it claims to protect. There is no account because there is no reader to identify, and therefore nothing to subpoena, leak, or sell.

---

**The physical write path excludes disabled people, people without documents, and people far from a civic office. How do you justify that?**

We do not fully justify it. It is a real cost, borne unevenly, and we are not going to pretend otherwise.

What we will say: the cost applies to the *write* path only, which is a small fraction of the platform's public value. Reading — the map, the passports, the archive, the API, the bulk dumps — is free, anonymous, and unbarred, and always will be. And the alternative is worse: a remote write path means a system where the loudest actor is whoever can afford the most bots, and where defending against that requires collecting more and more data about writers until the platform becomes the thing it was built to oppose.

Partial mitigations exist and are in scope: mobile issuance units, terminals in libraries and post offices rather than only government buildings, assisted filing where a clerk operates the terminal at the citizen's direction. None of these close the gap entirely. We would rather have an honest, narrow, trustworthy write channel than a broad, cheap, poisoned one.

---

**Isn't rating officials just a harassment vector?**

It would be, if we let people rate *people*. We do not — but we very much hold individuals accountable, and the distinction is worth being precise about, because it is the difference between a platform that survives and one that gets sued into the ground.

Complaints and ratings attach to a **project, decision, or object**. Something with a date, a budget, and a documented chain of responsibility. Those propagate upward into the record of every office that authority passed through. An official's record is therefore the computed sum of what happened under them: projects completed, projects late, cost variance, complaints answered within the statutory period, what they inherited, what they left unfinished. Reproducible from a published formula. Nobody types it; it is derived.

So a governor who presided over four failed projects has a record that says exactly that, with names of everyone else in each chain. What they do not have is a comment section.

The reason is not squeamishness. A complaint attached to a person invites "I don't like him," which is worthless as evidence and dangerous as a target. A complaint attached to a project says "this cost 3× estimate and finished two years late," which is checkable, contestable, and survives a defamation suit. The second is far more damaging to a bad official than the first — because it is specific, and because they have to answer it.

If someone has genuinely never had anything go wrong under their authority, that is what the record will show, and they can point at it. If their record is bad and they cannot explain it, that is informative too. Full picture, crowd decides. See [DATA_MODEL.md § 3](DATA_MODEL.md#3-institution--office-passports).

---

**What stops a bribed clerk from minting a thousand fake keys?**

Nothing stops them minting a few. The design stops them minting a thousand, and makes the few visible.

Every key ever issued is published: serial number, office, clerk pseudonym, timestamp. Nothing about the citizen — the platform never learns who holds which key. Serials are monotonic per office and never reused, which means a gap is an unaccounted-for key and an office is publicly on the hook to explain it, and a clerk issuing 430 keys in a week against an office median of 40 is visible to any journalist with a spreadsheet.

Beyond that: the identity commitment derives from the document's chip signature, not from anything the clerk types, so inventing a citizen requires forging a passport. Reissues after loss need two clerks on different shifts. And if a range is later found fraudulent, we flag exactly that range — we do not delete it, because a platform that deletes inconvenient history under investigation is not one anyone should trust.

The honest ceiling: a determined clerk can still issue a handful. See [SECURITY.md § The corrupt clerk](SECURITY.md#the-corrupt-clerk).

---

**What stops a government from just ordering you to delete something?**

Nothing stops the order. What we control is the consequence:

- Removal is logged as a public event. The fact of the takedown, the ordering authority, and the legal basis are published.
- It does not propagate. Other Stewards are notified and are not obliged to comply.
- The data is ODbL and mirrored. A deletion in one jurisdiction is a deletion from one server, not from the record.

We cannot make a government powerless. We can make its use of power visible and largely futile.

---

**What stops the project itself from being captured?**

Nothing, permanently. So we designed for capture instead of against it: federated Stewards, no central store, content-addressed data, continuous signed bulk dumps, open licences, and an Assembly that can suspend a captured Steward. If we are corrupted, the correct outcome is that someone forks the data and continues without us. See [GOVERNANCE.md § 6](GOVERNANCE.md#6-capture-and-forking).

---

**Why not just use a blockchain?**

Because we need an append-only log with strong provenance, and we already have that: content-addressed revisions plus independent mirrors held by legally separate organisations in different jurisdictions. That gives us tamper-evidence without the throughput ceiling, the energy cost, the governance-by-token, or the very serious problem that a blockchain makes legally-mandated deletion technically impossible — which sounds like a feature until you meet an actual court order about actually sensitive data.

---

**Won't the data just be wrong and stale?**

Some of it, yes. Which is why every record carries a **verification tier** and a **provenance chain**, and why the primary ingestion path is automated adapters against institutional systems of record rather than volunteer enthusiasm. Enthusiasm is real and does not last thirty years. A cron job does.

Where we do not know something, the record says we do not know it, and says why. Declared absence is more useful than a clean-looking blank.

---

**Why is 3D not in Phase 1?**

Because 3D is a rendering problem and the data model is the hard problem. A beautiful globe over a wrong schema is a liability. See [ROADMAP.md](ROADMAP.md).

---

**What if AI could just fill in all the missing data?**

It could produce something that looks like the missing data. That is not the same thing, and on an accountability platform the difference is the entire point. AI may propose, at the `machine_extracted` tier, always linked to a source, never promoted without human review, never presented as record. It may not assert, rank, score, or summarise institutions. See [ARCHITECTURE.md § 6](ARCHITECTURE.md#6-future-ai-integration).

---

**Who is paying for this?**

Stewards publish their funding in full, annually, per source. No Steward may take more than 25% of its budget from a single government body, or more than 10% from any entity holding public contracts in its jurisdiction. A Steward in breach loses its Assembly vote — though not its obligation to keep publishing. See [GOVERNANCE.md § 5](GOVERNANCE.md#5-conflict-of-interest).

---

**Is this project realistic?**

At the scale described, over the timeline described, by the people currently working on it: no. It is a hundred-year proposition attempted by people who will not finish it. What is realistic is one city, one working query, one journalist who finds something they could not find before. That is Phase 1, and it is the only thing we are actually asking to be judged on right now.
