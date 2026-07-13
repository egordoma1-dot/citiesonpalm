# Cities On Palm

**Cities On Palm** is a long-term civic infrastructure platform. Its purpose is to make every physical object in the world legible through public data.

It is not a website. A website is one of its rendering surfaces. The platform is a public data commons: a versioned, geospatially indexed record of the built environment and the public institutions responsible for it.

---

## The core idea

Every physical object built or maintained with public consequence — a pavement slab, a bridge, a substation, a park bench, a housing block — has a **passport**: a structured, permanent, publicly readable record of what it is, who owns it, when it was built, what it cost, who is accountable for it, and what is planned for it next.

Every passport is versioned. Nothing is deleted. A change to an object produces a new revision; the old revision remains readable forever. The history of a city becomes queryable.

Institutions and public officials also have passports — not personal profiles, but **accountability records**: jurisdiction, mandate, budget lines, projects under their authority. Scoped strictly to information that is legally public.

Objects nest into a single hierarchical world model:

```
Object → Street → District → City → Region → Country → World
```

Zoom in and you see a manhole cover. Zoom out and you see the ministry that owns the water network.

---

## Design constraints

These are not features. They are constraints the system is built around, and they are load-bearing.

| Constraint | Consequence |
|---|---|
| **No accounts for reading** | The public data surface has no sign-in, no session, no cookie, no analytics. Reading is anonymous by construction, not by policy. |
| **No behavioural tracking** | The platform does not record who looked at what. There is nothing to subpoena and nothing to sell. |
| **Write access is physically gated** | Feedback, complaints, and ratings are submitted only from **physical civic terminals**, on isolated wired networks. See [ARCHITECTURE.md](ARCHITECTURE.md). |
| **Read/write separation is architectural** | The public web surface is a read-only replica. It has no code path that can write to the canonical store. |
| **Append-only history** | Revisions are immutable. Corrections are new revisions with provenance, not overwrites. |
| **Neutrality** | The platform publishes facts and provenance. It does not rank, editorialise, or algorithmically amplify. |

The write path is deliberately expensive and slow. This is the point. A civic record that is cheap to write is cheap to poison.

---

## Repository contents

| Document | What it covers |
|---|---|
| [VISION.md](VISION.md) | What this is for, over decades. Success and failure conditions. |
| [PRINCIPLES.md](PRINCIPLES.md) | The six binding principles. Non-negotiable. |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System topology, the air-gapped write path, ingestion, serving, 3D rendering. |
| [DATA_MODEL.md](DATA_MODEL.md) | Object passports, institution passports, revisions, the spatial hierarchy, schemas. |
| [GOVERNANCE.md](GOVERNANCE.md) | Who decides what. Schema changes, jurisdiction onboarding, capture resistance. |
| [ROADMAP.md](ROADMAP.md) | Phased plan, from single-city pilot to federation. |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Code, schema, and data contribution workflows. Verification tiers. |
| [SECURITY.md](SECURITY.md) | Threat model, disclosure policy, physical security. |
| [FAQ.md](FAQ.md) | The hard questions, answered honestly, including the ones without good answers. |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Behavioural standards and enforcement. |
| [LICENSE.md](LICENSE.md) | Licensing recommendations for code, data, and documentation. |
| [CHANGELOG.md](CHANGELOG.md) | Release history. |

Read [PRINCIPLES.md](PRINCIPLES.md) before proposing anything. Most rejected proposals are rejected on principle, not on merit.

---

## Status

**Pre-alpha. Specification stage.** This release is documentation only. No production code is included.

We are specifying before building because the mistakes that matter in this project — a leaky privacy model, a capturable governance structure, a schema that cannot represent a Japanese address or an informal settlement — are mistakes that cannot be patched later. They are foundational.

The first implementation milestone is a single-city pilot. See [ROADMAP.md](ROADMAP.md).

---

## What this project is not

- **Not a mapping product.** OpenStreetMap already maps the world, and does it well. We depend on it. We are not a competitor; we are a layer of accountability data that references it.
- **Not a social network.** There are no follows, feeds, likes, or profiles. Ratings are aggregate signals attached to institutional records, not content in a timeline.
- **Not a surveillance system.** The object of scrutiny is public infrastructure and public office. Private individuals are out of scope, permanently. See [PRINCIPLES.md § Privacy](PRINCIPLES.md#3-privacy-is-a-boundary-not-a-setting).
- **Not neutral about transparency.** It is neutral between political actors. It is not neutral on the question of whether public spending should be publicly visible.

---

## Contributing

We currently need: geospatial engineers, database engineers with append-only/temporal experience, WebGL/3D rendering engineers, hardware-security specialists (for the terminal path), civic-data librarians, and translators.

Start with [CONTRIBUTING.md](CONTRIBUTING.md). Open a discussion before opening a large PR.

## Licence

Code: **AGPL-3.0**. Data: **ODbL 1.0**. Documentation: **CC BY-SA 4.0**. Rationale in [LICENSE.md](LICENSE.md).
