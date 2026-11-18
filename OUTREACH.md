# Siren — Research Outreach

**Project:** Siren — Active Semantic Lure & Session Containment Engine for Autonomous AI Agents  
**Author:** Aly Hussein Zopair  
**Repository:** https://github.com/zopair/Siren  
**Documentation:** https://zopair.github.io/Siren/

This is a research-outreach plan and copy bank. It does not imply endorsement, partnership, review, affiliation, or prior contact with any organization. No messages are sent by this document.

## 1. Current project description

Siren is an independent AI-agent security research proof of concept exploring whether controlled semantic lures can make selected agent interactions observable, support session-containment orchestration, and enable more disciplined counterfactual investigation.

Its research workflow is:

**Attract → Capture → Isolate → Investigate → Prove**

The current codebase brings together:

- **Semantic lure:** controlled, synthetic content designed to test whether an agent interacts with a defined lure.
- **Capture and telemetry:** structured records of observed interactions and tool-related events.
- **Sentinel Quarantine:** an orchestration contract for session revocation, egress blocking, child-process containment, and isolation.
- **Causal Proof:** an A/B/C experimental runner and evidence report intended to compare controlled conditions.
- **MCP and demonstration surfaces:** interfaces and a reproducible synthetic demonstration.

### A/B/C reference experiment

- **A — Baseline:** neutral content, without the treatment lure.
- **B — Treatment:** synthetic context containing the defined semantic lure.
- **C — Counterfactual:** remove the specific lure source while preserving the rest of the experiment configuration as far as the harness permits.

The experiment is intended to examine whether the lure source changes observed behavior. A/B/C labels alone do not establish causality; conclusions must follow the actual controls, reset behavior, fingerprints, and recorded evidence.

### Evidence vocabulary

Siren distinguishes:
- **ATTEMPTED:** an action was attempted or represented in the observed trace.
- **DISPATCHED:** a request was sent to the relevant adapter or tool boundary.
- **RECEIVED:** the receiving boundary recorded receipt.
- **EFFECT_CONFIRMED:** an external effect was independently confirmed.
- **NOT_OBSERVED:** the relevant effect was not observed within the experiment's evidence boundary.

A tool call or high severity score alone is not proof of a successful external effect.

### Limitations that must be disclosed

The current reference demonstration uses a synthetic, in-memory simulator. The Sentinel component defines and orchestrates an enforcement-adapter contract; it is not, by itself, a verified host operating-system, process, or network isolation implementation. Do not claim production-grade containment, universal prompt-injection prevention, model-generalized effectiveness, or absolute causal proof.

The demonstration is a research artifact, not a security certification or a production-ready security product. Any claims about external-model testing, hardware, deployment, or independently validated performance must be added only after the corresponding tests and evidence exist.

## 2. Outreach rules

1. Prioritize organizations and research groups whose official pages place the relevant team or institution in the United States, United Kingdom, or Europe.
2. Do not knowingly target an organization, individual, or team with a publicly documented institutional affiliation in Israel. This is a best-effort screen of public institutional information, not a claim that a person's complete career or personal history can be exhaustively verified.
3. Do not infer email addresses from naming conventions, domains, or email-verification services.
4. List an email only when the official project page or the research paper itself publishes the exact address. Otherwise use the official form, repository discussion, or public contribution route.
5. Do not use vulnerability-disclosure addresses or private security reporting portals for general research introductions.
6. Do not send bulk or automated messages. Personalize each note and send only after the author has reviewed and approved it.
7. Do not imply that a recipient's systems were tested, that they endorsed Siren, or that a collaboration exists.
8. One concise follow-up after 10–14 days is sufficient; stop after that if there is no response.
9. Respect each community's contribution, meeting, and posting rules. Never insert generic promotion into unrelated issues or pull requests.

## 3. Target register (official public routes)

The list below is a shortlist of relevant US/UK/European organizations, projects, and research artifacts. A blank direct-email field means no suitable research-introduction email was verified in the official source reviewed; use the linked public route instead.

| # | Organization / research target | Geographic basis | Why it is relevant to Siren | Verified public contact route |
|---:|---|---|---|---|
| 1 | OpenAI — Red Teaming / Safety research | United States | Adversarial evaluation, agent misuse cases, and evaluation methodology. | Red-teaming guidance: https://developers.openai.com/api/docs/guides/red-teaming . No general research email verified. Submit only through a route explicitly intended for research participation; do not submit third-party vulnerability claims. |
| 2 | Anthropic — Safeguards Research | United States / United Kingdom | Automated red teaming, monitoring, jailbreak robustness, and response. | Team overview: https://red.anthropic.com/2025/introducing-safeguards-research-team/ . No general research email verified. |
| 3 | Google DeepMind — AI safety / security research | United States / United Kingdom / Europe | Red teaming, agent safety, and security evaluation. | Official research and safety pages: https://deepmind.google/ and https://ai.google/responsibility/ . No general research email verified. |
| 4 | Microsoft Research — Security and agent research | United States / United Kingdom / Europe | Information-flow control, agent security, and deterministic policy enforcement. | Research area: https://www.microsoft.com/en-us/research/research-area/security-privacy-cryptography/ . No general outreach email verified. |
| 5 | CaMeL paper authors — “Defeating Prompt Injections by Design” | Google / Google DeepMind / ETH Zurich (US/Europe research affiliations listed in the paper) | Directly relevant to untrusted context, control/data-flow boundaries, capabilities, and tool authorization. | Paper: https://arxiv.org/abs/2503.18813 . The paper publishes corresponding-author emails: edoardo.debenedetti@inf.ethz.ch and ilia.shumailov@google.com. Use only for a specific scholarly exchange about the paper. |
| 6 | FIDES authors — “Securing AI Agents with Information-Flow Control” | Microsoft Research (US/UK research organization) | Integrity/confidentiality labels, information-flow tracking, and deterministic enforcement. | Official publication: https://www.microsoft.com/en-us/research/publication/securing-ai-agents-with-information-flow-control/ and code: https://github.com/microsoft/fides . No direct author email verified in the reviewed official publication. |
| 7 | OWASP GenAI Security Project | United States-based global open community | LLM application security, threat taxonomy, evaluation guidance, and practical community review. | Official project page: https://owasp.org/projects/genai-security/ . Publicly listed project contacts include ads.dawson@owasp.org and scott.clinton@owasp.org. General contact form: https://genai.owasp.org/contact/ . |
| 8 | OWASP Agentic AI Security Initiative | United States-based global open community | Autonomous agents, multi-step workflows, agentic application risks, and security guidance. | Initiative page: https://genai.owasp.org/initiatives/agentic-security-initiative/ . The OWASP project page publicly lists john.sotiropoulos@owasp.org for the initiative lead. |
| 9 | Agentic AI Foundation (AAIF) | Linux Foundation ecosystem; United States-based foundation context | Open governance and ecosystem coordination around agentic infrastructure, including MCP. | Official contact form: https://aaif.io/contact . No general technical research email verified. |
| 10 | Model Context Protocol (MCP) project | Open-source project with US-based foundation stewardship and global maintainers | Tool trust boundaries, server/client assumptions, authorization, and session security. | Security policy: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/SECURITY.md . Use project discussions for research discussion; use private GitHub Security Advisories only for actual vulnerabilities. |
| 11 | NIST — Center for AI Standards and Innovation (CAISI) | United States | AI measurement, evaluations, security, and standards-related research. | Official center: https://www.nist.gov/aisi . General NIST contact: https://www.nist.gov/contact . No dedicated independent-project outreach email verified. |
| 12 | UK AI Security Institute (AISI) | United Kingdom | Frontier AI evaluation, safeguards, control, and security research. | Official site: https://www.aisi.gov.uk/ . Research and evaluation information is published there; no general research-introduction email verified. |
| 13 | IEEE SaTML | Europe / international research conference hosted in Europe | Security and trustworthiness of machine learning; relevant venue for research-method feedback and future submissions. | Conference site: https://satml.org/ . Use the current conference contact page and submission system; do not treat a program-chair address as a generic unsolicited review service. |
| 14 | ETH Zurich — Security, Privacy and Society / CaMeL research context | Switzerland | Relevant academic context for the CaMeL paper and secure agent architecture. | Institutional research pages: https://ethz.ch/en.html and the CaMeL paper above. Use the published corresponding-author email only where directly relevant. |
| 15 | Alan Turing Institute — AI security / assurance research | United Kingdom | Research on trustworthy AI, security, and evaluation methods. | Official institute: https://www.turing.ac.uk/ . Use its official contact and research-group routes; no direct email verified for a Siren-specific approach. |

### Geographic screening note

This register uses the institution or research affiliation stated on the linked official pages and papers. Public sources cannot establish every person's complete employment, collaboration, residency, or personal history. The register therefore avoids claiming exhaustive biographical screening. Before addressing an individual, re-check their current official institutional profile and exclude them if an Israel-linked affiliation is identified. Prefer organization-level contact routes where individual affiliation is unclear.

## 4. Tailored outreach templates

Use the placeholders only after verifying the recipient's current role, institution, and the exact paper or initiative being referenced. These are drafts only; no message has been sent.

### A. Major AI companies — AI security and red-team teams

**Subject:** Independent research: semantic lures and counterfactual evidence for agent security

Dear [Research Team / Recipient],

I am introducing **Siren**, an independent research proof of concept exploring active semantic lures, observable agent interactions, session-containment orchestration, and counterfactual security evidence.

Your team's published work on [specific red-teaming, safeguards, monitoring, or agent-security topic] is relevant to the questions Siren investigates.

Siren follows a five-stage research workflow:

**Attract → Capture → Isolate → Investigate → Prove**

Its reference experiment compares a neutral baseline (A), a synthetic-lure treatment (B), and a counterfactual condition (C) in which the specific lure source is removed. The aim is to distinguish observed interaction from dispatched actions and independently confirmed effects.

I would value your feedback on the experiment design or a pointer to the most appropriate public research forum.

The current demonstration uses a synthetic in-memory simulator. Sentinel is an enforcement-adapter orchestration contract, not a verified production host or network isolation implementation. Siren does not claim universal prompt-injection prevention or generalized effectiveness across external models.

**Repository and visual evidence:** https://github.com/zopair/Siren

The repository includes the A/B/C reference benchmark and visual evidence report.

Kind regards,

Aly Hussein Zopair — Independent AI Security Researcher

### B. Academic researchers — CaMeL, FIDES, and prompt-injection research

**Subject:** Research exchange: semantic lures, agent security boundaries, and counterfactual evidence

Dear [Researcher Name],

I am reaching out to introduce **Siren**, an independent research proof of concept focused on observable security behavior in autonomous AI agents.

Your work on [CaMeL / FIDES / exact paper title] addresses important questions around untrusted context, information-flow integrity, and enforcement at tool boundaries. Siren explores a complementary experimental question: can controlled semantic lures help researchers observe selected agent interactions, coordinate containment decisions, and compare behavior under a controlled counterfactual?

Its workflow is:

**Attract → Capture → Isolate → Investigate → Prove**

The A/B/C reference experiment uses a neutral baseline, a synthetic-lure treatment, and a counterfactual condition that removes the lure source while preserving the rest of the harness configuration as far as possible.

I would particularly value your perspective on the controls, evidence hierarchy, and limits of causal interpretation.

The current implementation is a synthetic in-memory demonstration; it does not claim production-grade host isolation or evaluate your system.

**Repository and visual evidence:** https://github.com/zopair/Siren

Thank you for considering this research exchange.

Kind regards,

Aly Hussein Zopair — Independent AI Security Researcher

### C. OWASP / AAIF / MCP working groups

**Subject:** Open research artifact for agentic security discussion — Siren

Dear [Working Group / Initiative],

I would like to share **Siren**, an independent open-source research proof of concept focused on security evaluation and observable behavior in autonomous AI agents.

The project is relevant to ongoing work on agentic application security, untrusted context, tool interactions, MCP trust boundaries, and containment.

Siren organizes its workflow as:

**Attract → Capture → Isolate → Investigate → Prove**

It combines synthetic semantic lures, structured interaction telemetry, a session-quarantine orchestration contract, and an A/B/C counterfactual experiment. The evidence model distinguishes attempted actions, dispatched requests, received events, and independently confirmed effects.

The current demonstration uses an in-memory synthetic simulator; it does not claim production-grade operating-system, process, or network isolation.

**Repository and visual evidence:** https://github.com/zopair/Siren

Would this be appropriate for a working-group discussion, community meeting, or contribution channel? I would appreciate guidance on the correct route and any feedback on the methodology.

Kind regards,

Aly Hussein Zopair — Independent AI Security Researcher

## 5. Recommended contact sequence

1. Start with OWASP Agentic Security Initiative and OWASP GenAI Security Project through their official public routes.
2. Approach the CaMeL corresponding authors with a narrowly scoped academic question tied to their paper.
3. Approach the FIDES authors through the official publication/repository discussion route, not an inferred email.
4. Use AAIF/MCP community channels for standards and trust-boundary discussion, not vulnerability reporting unless an actual vulnerability is being disclosed.
5. Approach OpenAI, Anthropic, Google DeepMind, Microsoft Research, NIST CAISI, and UK AISI only through official routes intended for research engagement.
6. Consider SaTML for a future research submission only after strengthening reproducibility and documenting limitations.

## 6. Pre-send quality gate

Before sending any message:

- [ ] Confirm the recipient's current institution and public role.
- [ ] Re-check the recipient and institution against the geographic exclusion rule.
- [ ] Verify that the email appears verbatim on an official institutional page or the paper itself; otherwise use the official form or public contribution route.
- [ ] Replace the placeholder with one specific publication, initiative, or research question.
- [ ] Open the repository and confirm the README, benchmark report, and visual report links work.
- [ ] Ensure claims match the current implementation and do not overstate isolation, causal inference, or external-model testing.
- [ ] Send individually, manually, only after the author approves the exact message.
- [ ] Record the date and outcome; follow up once after 10–14 days at most.

## 7. Measurement

Track observable outcomes only:
- substantive technical replies or referrals;
- issues, discussions, or pull requests containing actionable feedback;
- reproducibility findings that lead to a documented test or limitation;
- qualified repository visits or referrals, where privacy-conscious analytics are available.

Do not treat impressions, likes, stars, or company mentions as evidence of technical validation, partnership, endorsement, or adoption.

---

**Authorship:** Aly Hussein Zopair (علي حسين زبير ALY HUSSEIN ZOPAIR)  
**Campaign integrity:** This document contains proposed outreach targets and unsent drafts. No message has been sent, no organization has reviewed or endorsed Siren, and no partnership is implied.
