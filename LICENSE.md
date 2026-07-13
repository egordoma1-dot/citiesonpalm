# Licensing

Three artefacts, three licences. Each chosen for a specific failure it prevents.

| Artefact | Licence |
|---|---|
| Code (reference implementation, adapters, clients) | **AGPL-3.0** |
| Data (passports, revisions, bulk dumps) | **ODbL 1.0** |
| Documentation and schema specifications | **CC BY-SA 4.0** |

---

## Code — AGPL-3.0

The relevant failure mode is a government or vendor deploying a modified, closed fork of this platform: same interface, same public trust, quietly different behaviour in the ingestion or takedown path. A permissive licence permits exactly that. GPL does not prevent it either, because the platform is delivered over a network and never distributed as a binary.

AGPL closes the network loophole. If you run a modified Cities On Palm as a service, you publish your modifications. For a transparency platform, running unauditable code is the one thing that cannot be allowed, and the licence is the only enforcement mechanism available.

**Consequence we accept:** some commercial actors will not touch AGPL. Good. The ones deterred by an obligation to publish their changes to a public-accountability platform are not the ones we want operating one.

---

## Data — ODbL 1.0

Chosen for **share-alike**, and for compatibility with OpenStreetMap, which we ingest from and must not create a licence conflict with.

Share-alike is the fork guarantee described in [GOVERNANCE.md § 6](GOVERNANCE.md#6-capture-and-forking). If a Steward is captured, the data cannot be enclosed: derivatives of the public database must themselves be published under ODbL. This makes the fork threat credible, and the fork threat is what makes capture unattractive.

**Attribution:** derived works cite Cities On Palm and, where applicable, the upstream source of the record. Provenance survives redistribution — that is the whole point of the provenance chain.

---

## Documentation and schema — CC BY-SA 4.0

The schema is intended to be adopted by institutions that are not us, including ones that never federate with us and never run our code. CC BY-SA lets a procurement system emit passport-shaped records natively without touching AGPL code. That is the fifteen-year outcome described in [VISION.md](VISION.md), and the licensing has to permit it.

---

## Contributor terms

- Code contributions: DCO sign-off. **No CLA.** A CLA concentrates relicensing power in one organisation, which is precisely the concentration this project's governance exists to prevent. We will not hold a key that could be used to relicense the commons.
- Data contributions: contributors grant rights compatible with ODbL and warrant that the source is lawfully public.
- Documentation: CC BY-SA 4.0 on submission.

---

## Trademark

The name and marks are held separately from the licences and are not granted by them. A fork may use the code and the data freely. It may not call itself Cities On Palm. This is the one lever we retain against a captured deployment trading on the name of an uncaptured one, and it is deliberately the only lever.
