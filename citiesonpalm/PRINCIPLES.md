# Principles

Six binding principles. They constrain every design decision in this repository. A proposal that improves usability, performance, or coverage at the cost of one of these is rejected regardless of merit.

Where two principles conflict — and they do — the resolution order is: **Privacy > Data Integrity > Neutrality > Transparency > Accountability > Accessibility.** Privacy wins ties because a privacy failure is irreversible; an accessibility failure is a backlog item.

---

## 1. Transparency

**Everything the system knows, it publishes.**

- Every record is readable without an account, a session, or a payment.
- Every record carries its provenance: which source, which document, which date, which ingestion run.
- The code that produces the record is open. The schema is open. The ingestion adapters are open.
- Absence is published too. "We have no cost data for this bridge" is a fact, and the record says so, rather than silently omitting the field.

Transparency includes transparency about ourselves. Funding, governance minutes, and takedown requests are published on the same terms as everything else.

**What this does not mean:** transparency is not a mandate to collect. We publish what we hold; we are extremely conservative about what we hold. See Principle 3.

---

## 2. Public Accountability

**The subject of scrutiny is public power, not private life.**

Institutions and offices are in scope because they spend public money and exercise public authority. That authority is the *reason* they are legible here, and it is also the *limit* of what is legible.

An official's passport contains: their office, its mandate, its jurisdiction, its budget, the decisions taken under it, and the objects it is responsible for. It does not contain: home address, family, movements, private finances, personal communications, or anything else that would be private for a citizen holding no office.

**Individuals in public office are accountable as individuals** — but through their decisions, not through opinion. Complaints and ratings attach to a **project, decision, or object**: something with a date, a budget, and a documented chain of responsibility. They propagate upward into the record of every office that authority passed through.

An officeholder's record is therefore the computed sum of what happened under their authority — including what they inherited and what they left unfinished, because the dates say so. Responsibility is usually shared, and every party in the chain is named.

What does not exist is a place to type an opinion about a human being. A complaint that a project ran 3× over budget is checkable, contestable, and damaging in a way that survives scrutiny. A star rating on a person is noise that discredits the platform and endangers the person. We publish the first and refuse to build the second.

---

## 3. Privacy is a boundary, not a setting

**Private individuals are permanently out of scope. This is not configurable.**

There is no toggle, no jurisdictional exception, no "opt-in for landlords," no phased expansion. The scope boundary is:

| In scope | Out of scope |
|---|---|
| Public infrastructure | Private residences as dwellings |
| Publicly-owned or publicly-funded objects | Occupants, tenants, residents |
| Public offices and their occupants **qua officeholders** | Private individuals, including private property owners |
| Legally-public ownership registries (as-published) | Any derived profile of a natural person |
| Aggregate, non-attributable civic feedback | Any record of who read what |

Two mechanisms enforce this on the read side:

- **No reader identity exists.** The public surface has no login, no cookie, no session, no analytics, no request logging beyond ephemeral operational counters. We cannot disclose who read what because we do not know.
- **No cross-object joins on natural persons.** The query layer refuses to satisfy queries whose result set is a set of natural persons filtered by attribute. "All objects owned by entity X" is answerable if X is a public body or a company. It is not answerable for a natural person, even where each individual ownership record is separately public.

That last rule is the one people argue with. It is the one we will not move on. Individually-public facts aggregate into a surveillance product, and the aggregation is the harm.

---

## 4. Neutrality

**The platform publishes facts and provenance. It does not editorialise.**

- No ranking of institutions by anything other than a stated, published, reproducible metric the user selected.
- No algorithmic feed, no recommendation, no amplification.
- No editorial layer over the data. If a contributor believes a record implies wrongdoing, the correct output is a journalism piece elsewhere that cites the record — not a badge on the record.
- Contested records are marked as contested, with both positions and their evidence shown. They are not adjudicated by the platform where the underlying fact is genuinely disputed.

Neutrality is between actors, not between values. We are not neutral on whether public expenditure should be visible. We are neutral on which party spent it.

---

## 5. Data Integrity

**The record is append-only. Corrections are new facts, not erasures.**

- Revisions are immutable and content-addressed. Editing history is not a supported operation; it is an incident.
- Every revision names its source, its ingestion method, and its verification tier ([DATA_MODEL.md § Verification](DATA_MODEL.md#7-verification-tiers)).
- Deletion exists only as **tombstoning**: the record is marked withdrawn, with a reason and an authority, and remains in the history. Hard deletion occurs only under a legal order, is itself logged as a public event, and the fact of removal is never hidden.
- Uncertainty is represented, not smoothed. A cost figure with a `low_confidence` flag is more honest than a clean number we cannot defend.

---

## 6. Accessibility

**A record nobody can read is not public.**

- Data is available as bulk download, not only through an interface. The 3D map is one client; the API and the dumps are the substrate.
- The read surface degrades gracefully: WebGL globe → 2D map → plain HTML tables → text. The plain-text layer is not a fallback afterthought; it is a first-class target, and it must work on a decade-old phone over a poor connection.
- Machine-readable is a form of accessible. Stable identifiers, stable schemas, documented migrations.
- Multilingual by construction. Names, addresses, and administrative divisions are not assumed to be Latin-script, Western-ordered, or singular.

**The known tension:** the write path is physically gated (see [ARCHITECTURE.md](ARCHITECTURE.md#4-the-write-path)), which is a real accessibility cost, borne unevenly by people with mobility limits, no documents, or no nearby office. We accept this cost for the *write* path only, and we are explicit that it is a cost rather than pretending it away. The *read* path — which is the overwhelming majority of the platform's public value — carries no such barrier and never will.
