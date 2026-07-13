# Vision

## The problem

The built environment is opaque by default.

A citizen standing on a street cannot answer basic questions about what they are looking at. Who owns this building? When was this road last resurfaced, and at what cost? Which office authorised the demolition of the block behind it? Which contractor won the tender, and were they the cheapest bid or the third-cheapest? What is scheduled to happen here in eighteen months?

This information usually exists. It is held in cadastral registries, procurement portals, municipal minutes, planning archives, and utility asset databases. It is nominally public. It is practically unreachable — scattered across hundreds of incompatible systems, retrievable only by those who already know where to look and have the time to look.

Opacity of this kind is not accidental, but it is also not always malicious. It is mostly *entropic*: the accumulated result of institutions that each digitised their own records, in their own formats, on their own schedule, with no obligation to be legible to anyone outside the building.

The consequence is the same regardless of cause. Public accountability collapses to the vanishing point where a determined journalist with a FOI request can still, occasionally, reconstruct a fragment of what happened.

## The proposition

Give every physical object a passport. Give every institution an accountability record. Version everything. Publish it all, anonymously readable, permanently.

The unit of the system is the **object** — not the document, not the department, not the fiscal year. Documents get lost. Departments get reorganised. Fiscal years end. The bridge stays where it is.

By anchoring the record to the physical object, we get a spine that survives institutional churn. A road does not care that the highways agency was merged into the transport ministry in 2031; the road's passport simply records that responsibility transferred on that date, and both the old and new responsible parties remain in the history.

## What success looks like, in stages

**In five years.** A citizen in one pilot city can point their phone at a building and read its passport. A journalist can query "all municipal contracts over €500,000 awarded to companies incorporated in the last 24 months" and get an answer in seconds, with citations to primary sources. A city council can no longer quietly re-scope a project between approval and construction, because the re-scope produces a revision, and the revision is public the day it is filed.

**In fifteen years.** The passport is a normal thing to expect. Procurement systems in participating jurisdictions emit passport revisions natively, as a side effect of their internal workflow, because the export adapter is part of the software they already bought. Coverage is uneven — some countries are complete, some are absent — but the *shape* of the record is standard enough that cross-border comparison is meaningful.

**In forty years.** The archive is the point. Someone in 2066 can reconstruct exactly how a district was built, decade by decade, decision by decision, and see whose name was on each decision. Historians use it. Engineers use it to understand why the foundations were laid the way they were. Cities use it to avoid repeating mistakes they no longer have living memory of.

The long-term value of this system is not the map. It is the archive that the map is a view onto.

## What failure looks like

We name these because a project of this shape fails in predictable ways, and naming them is the cheapest available defence.

**Capture.** A government, a party, or a corporation gains enough influence over the platform to shape what it records or how it presents it. Mitigated by [GOVERNANCE.md](GOVERNANCE.md): federated stewardship, no single controlling entity, forkable data under an open licence.

**Drift into surveillance.** The system starts with public infrastructure and public office, and someone proposes — always for good reasons — extending it to landlords, then to property owners, then to residents. This is the failure mode we consider most likely and most dangerous. The scope boundary in [PRINCIPLES.md](PRINCIPLES.md) is written to be brittle: hard to bend without visibly breaking.

**Weaponisation.** Officials' passports become a targeting list for harassment or violence. Mitigated by scoping strictly to the *office*, not the person: mandate, budget, jurisdiction, decisions. Never home address, never family, never movements. Ratings attach to institutional performance, not to individuals as individuals.

**Rot.** The data is entered once, celebrated, and never updated. Coverage decays into a museum of 2029. Mitigated by making the primary ingestion path *automated* — adapters that pull from institutional systems continuously — rather than relying on volunteer enthusiasm, which is real but not durable at this scale.

**Irrelevance.** We build a beautiful, rigorous, unused thing. Mitigated by starting with one city and one genuinely useful query, and refusing to expand until that works.

## Why the write path is physical

The write path — how a citizen files a complaint, rates an institution, or contests a record — runs through physical civic terminals on isolated wired networks. No remote access, no internet-facing write API, one hardware key per person, issued in person against identity documents.

This is an unusual choice and it deserves an unusual defence.

A civic record is only as valuable as it is trustworthy. The moment a public accountability system can be written to remotely and at scale, it becomes a target for exactly the actors with the strongest motive and the deepest resources to corrupt it: astroturfing operations, state information units, and anyone with an interest in the record saying something other than what happened.

Every purely-digital defence against this — rate limiting, CAPTCHA, reputation scoring, ML-based abuse detection — is an arms race the defender eventually loses, and each round of the race requires collecting more data about the writer. The endpoint of that path is an accountability platform that surveils its own users in order to protect itself. That is a contradiction we refuse.

So we take the cost up front. Writing is slow. Writing requires physical presence. Writing is bound to a hardware key bound to a verified identity — an identity the system never stores, and cannot reconstruct.

The result: an attacker who compromises the entire public web surface gains nothing but a read-only replica. To forge a single complaint, they must physically enter a government office, present a genuine identity document, and use a specific terminal on a specific cable. Fabricating one is expensive. Fabricating ten thousand is not an operation any adversary can run quietly.

Full mechanism in [ARCHITECTURE.md § The Write Path](ARCHITECTURE.md#4-the-write-path). Its costs — including its exclusion of people who cannot easily reach an office — are discussed honestly in [FAQ.md](FAQ.md).

## The horizon

Cities On Palm is a hundred-year project attempted by people who will not see it finished. Everything in this repository is written on that assumption: schemas designed to be migrated by people we will never meet, governance designed to survive its founders, licences designed so that if this specific organisation fails, the data outlives it and someone else can carry it.

If the institution running this project is captured, corrupted, or simply dies, the correct outcome is that the data forks and continues. The design goal is not the permanence of the organisation. It is the permanence of the record.
