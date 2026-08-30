# Contributing

Thanks for helping make Gaussian Robotics Atlas more accurate. A useful contribution can
be one corrected field, one replacement link, or one well-supported new resource.

## Before you submit

Search the [catalog](CATALOG.md), source records in [`catalog/`](catalog/), and existing
issues. Projects often change names between arXiv and code release, so compare DOI,
arXiv ID, and repository owner before adding a new entry.

We accept resources that meet all of these conditions:

- Gaussian Splatting or a closely related Gaussian representation is central to the
  method or tool.
- The work has a direct robotics use, evaluation, interface, or integration path.
- At least one primary source identifies the resource.
- The proposed metadata can be checked without private access.

We usually decline generic rendering papers, duplicate project pages, unsourced product
claims, link farms, and repositories whose only robotics connection is a topic tag.

## Fastest contribution: open an issue

Use the form that matches the problem:

- [Add a resource](https://github.com/Laityperfect7/awesome-gaussian-robotics/issues/new?template=add-resource.yml)
- [Correct a record](https://github.com/Laityperfect7/awesome-gaussian-robotics/issues/new?template=correction.yml)
- [Report a broken link](https://github.com/Laityperfect7/awesome-gaussian-robotics/issues/new?template=broken-link.yml)

Issue submissions do not require Python or a fork. Include primary-source links and
disclose whether you are an author, maintainer, employee, or otherwise affiliated with
the resource.

## Add or edit a record

1. Fork the repository and create a focused branch.
2. Install the local tool and development checks:

   ```bash
   python -m pip install -e ".[dev]"
   ```

3. Edit the appropriate JSON file under `catalog/`. Keep unrelated formatting and
   records unchanged.
4. Validate the source data and regenerate derived files:

   ```bash
   gr-atlas validate
   gr-atlas build
   gr-atlas build --check
   ```

5. Run the Python checks when your change touches tooling:

   ```bash
   python -m pytest
   python -m ruff check .
   python -m mypy src
   ```

6. Open a pull request with the evidence links and a short account of what changed.

`CATALOG.md` and files under `docs/` are generated. Edit the records first, run the
builder, and commit the resulting changes. Do not hand-edit a generated table to work
around a validation error.

## Record-writing rules

Write for someone deciding whether to inspect a method, not for a project homepage.

- Keep the summary factual and between 8 and 45 words.
- State the robot task and the method's usable output.
- Use the title and identifiers from the primary publication.
- Record input sensors only when a paper, project page, or repository documents them.
- Treat framework, hardware, and real-time claims the same way.
- Use `unknown` when the source does not state a license or compatibility detail.
- Omit star counts, citation counts, download counts, and other fast-changing popularity
  numbers.
- Do not copy an abstract, README paragraph, or marketing text.

Avoid judgments such as “best,” “fastest,” “production-ready,” or “state of the art.” A
benchmark result belongs only when the schema explicitly supports it and the record links
to the exact table or artifact. The current catalog does not rank performance.

## Evidence and links

Primary evidence includes the publisher or arXiv record, an author-maintained project
page, and the official code repository. A survey, blog post, or list can help discover a
resource but should not be its only source.

For every changed fact:

- add the most direct source URL available;
- prefer HTTPS and a canonical page over search results or URL shorteners;
- verify that the link resolves and names the same resource;
- update `verified_date` to the day you checked the sources;
- keep DOI and arXiv identifiers in their normalized fields;
- record a public code license exactly, or use `unknown` when none is declared.

`code_status` has a narrow meaning:

| Value | Use it when |
|---|---|
| `released` | The linked repository contains the implementation described by the resource. |
| `partial` | Public code covers only part of the described method or omits key training or evaluation pieces. |
| `archived` | Code is public, but the repository is archived or explicitly unmaintained. |
| `paper-only` | A primary publication exists and no official code release was found. |
| `unavailable` | A code release was announced or referenced but cannot currently be accessed. |

A public repository does not prove reproducibility. Do not convert “code released” into
“results reproduced.”

## Pull request scope

Keep a data pull request easy to audit. One resource or a small related batch is ideal.
Separate Python refactors from catalog additions unless one depends on the other.

Reviewers will check duplicate identities, canonical URLs, controlled vocabulary,
evidence quality, generated-file drift, and affiliation disclosure. They may edit a
summary for neutral wording or ask for a more direct source.

## Tooling changes

The CLI and generator support Python 3.10 and later and should keep zero runtime
dependencies unless a proposal shows a clear maintenance benefit. New behavior needs
tests, deterministic output, and an explanation in the pull request. Network access must
remain optional; validation of catalog structure should work offline.

Discuss broad schema changes in an issue before implementing them. A new field affects
the source records, validator, CLI, exports, site, documentation, and downstream users.

## Licensing

By contributing catalog records or generated catalog content, you agree to release that
contribution under [CC0 1.0](LICENSE). By contributing software or software
documentation, you agree to license it under the [MIT License](LICENSE-CODE).

You remain responsible for submitting work you have the right to share. Link to
third-party material instead of copying it into the repository.

Participation is subject to the [Code of Conduct](CODE_OF_CONDUCT.md).
