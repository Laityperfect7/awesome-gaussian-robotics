# Security Policy

## Supported versions

Security fixes target the default branch and the latest tagged release. Older snapshots
of the generated site and catalog may not receive patches.

## Report a vulnerability privately

Use [GitHub's private security advisory form](https://github.com/Laityperfect7/awesome-gaussian-robotics/security/advisories/new).
Please do not open a public issue before maintainers have assessed the report.

Include the affected file or command, a minimal reproduction, the impact you expect, and
any safe mitigation you already tested. Remove tokens, personal data, private repository
URLs, and unrelated machine details from logs or screenshots.

Maintainers aim to acknowledge a report within seven days and provide a triage decision
within 30 days. These are response targets, not a disclosure deadline. We will coordinate
credit and publication timing with the reporter when a fix is needed.

## What counts as a security issue

Examples include:

- code execution or unsafe file writes caused by catalog content;
- HTML or script injection in generated pages;
- a dependency or workflow configuration that exposes credentials;
- a repository-controlled link that intentionally distributes malicious content;
- a committed secret, private key, access token, or sensitive personal data.

An ordinary dead link, incorrect paper field, or third-party repository vulnerability is
usually a catalog correction. Use the broken-link or correction issue form unless the
link now serves malware, captures credentials, or creates another immediate risk.

## Security design

The CLI, validator, and static site are designed to run without API keys. Contributions
must not add credentials to catalog records, examples, test fixtures, issue text, or
workflow files. CI permissions should stay read-only unless a documented publishing job
needs a narrower write permission.

Generated HTML must treat catalog strings as untrusted input. The builder should escape
text and URLs, reject unsafe URL schemes, and avoid third-party scripts. Network-based
link checks should remain separate from structural validation so contributors can audit
the catalog offline.

## Good-faith research

We support good-faith testing that avoids privacy violations, data destruction, service
disruption, and access to accounts or data that do not belong to the researcher. Give
maintainers a reasonable opportunity to fix a confirmed issue before public disclosure.
We will not pursue action against research that follows these limits and applicable law.
