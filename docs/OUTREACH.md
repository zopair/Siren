# Industry Outreach Kit

This document is a practical, opt-in outreach plan for the Siren-Trap research prototype. It is not an announcement of partnerships, endorsements, review, or affiliation with any organization listed below.

## Project positioning

Siren-Trap is an open-source Python **alpha research prototype** for defensive physical-layer and multimodal AI security research. Its current scope includes a fixed inert acoustic canary, a localhost-first instrumented decoy service, observation checks, passive WAV analysis, and structured telemetry.

The project is relevant to discussions about:
- Defensive AI red teaming and evaluation.
- Audio and multimodal input handling.
- Trust boundaries and untrusted data.
- Reproducible security experiments and telemetry.

Be precise about limitations. Do not claim verified physical transmission/reception, broad hardware compatibility, production containment, model vulnerabilities, or successful agent-policy findings unless supported by published, reproducible evidence. The encoder/decoder round-trip and hardware compatibility work remain roadmap items.

## Recommended target order

| Priority | Organization / channel | Why it is relevant | Best first contact |
|---|---|---|---|
| 1 | Microsoft AI Red Team / PyRIT | Direct overlap with AI red teaming and open evaluation tooling | Ask a focused technical question in the PyRIT community after reviewing its contribution guidance |
| 2 | NVIDIA AI Security / Open Secure AI Alliance | Explicit interest in reproducible AI security research, multimodal risks, and practical defensive artifacts | Share a concise research note through an appropriate alliance or research channel |
| 3 | Hugging Face Audio community | Relevant community for audio processing, evaluation, and open-source projects | Share a project introduction in the audio study/discussion community and request technical feedback |
| 4 | OpenAI evaluation / audio ecosystem | Relevant public work on evaluation frameworks and audio/voice-agent evaluation | Share a narrowly scoped comparison or reproducibility question in the relevant public project context |
| 5 | Google DeepMind audio research | Relevant audio and multimodal research context | Share a research-oriented note linked to the relevant public audio work; avoid implying direct project fit beyond the technical overlap |
| 6 | Anthropic AI safety research | Broad relevance to safety, interpretability, and reliable AI systems | Use a public research/community channel only when a concrete technical question or result is available |

## Verified public destinations

### Microsoft
- AI Red Team guidance: https://learn.microsoft.com/en-us/security/ai-red-team/
- PyRIT repository and community: https://github.com/microsoft/pyrit
- LinkedIn company page: https://www.linkedin.com/company/microsoft/
- X: https://x.com/Microsoft

### NVIDIA
- AI Security research: https://research.nvidia.com/ai-security/
- Open Secure AI Alliance information is linked from the AI Security research page.
- Audio Intelligence repository: https://github.com/NVIDIA/audio-intelligence
- LinkedIn company page: https://www.linkedin.com/company/nvidia/
- X account: confirm the current official research/developer account from NVIDIA's own site before tagging; do not substitute unrelated product or regional accounts.

### Hugging Face
- Official Discord community: https://hf.co/join/discord
- Audio course community guidance: https://huggingface.co/learn/audio-course/en/chapter0/community
- LinkedIn company page: https://www.linkedin.com/company/huggingface/
- X: https://x.com/huggingface

### OpenAI
- Official communication channels and social handles: https://help.openai.com/en/articles/11725090-verifying-communications-from-openai
- OpenAI Evals: https://github.com/openai/evals
- OpenAI Cookbook audio voice-agent evaluation: https://github.com/openai/openai-cookbook/tree/main/examples/audio/duplex_voice_agent_evaluation
- LinkedIn company page: https://www.linkedin.com/company/openai/
- Official X handles listed by OpenAI: @OpenAI and @OpenAIDevs

### Google DeepMind
- DeepMind research repository: https://github.com/google-deepmind/deepmind-research
- PhaseCoder spatial-audio research: https://github.com/google-deepmind/phasecoder
- LinkedIn company page: https://www.linkedin.com/company/googledeepmind/
- X: verify the current account through the official DeepMind website before tagging.

### Anthropic
- Official website: https://www.anthropic.com/
- Open-source organization: https://github.com/anthropics
- LinkedIn company page: https://www.linkedin.com/company/anthropicresearch/
- X: verify the current account through Anthropic's official website before tagging.

## Ready-to-adapt messages

Replace the repository URL with https://github.com/zopair/Siren and include one relevant technical link. Do not mass-post identical messages. Use one organization-specific message at a time.

### Microsoft / PyRIT

> We have been developing Siren-Trap, an open-source Python alpha research prototype focused on defensive physical-layer and multimodal AI security. It provides a fixed inert acoustic canary, a localhost-first decoy service, observation checks, passive WAV analysis, and structured telemetry. Given the work around PyRIT and AI red teaming, we'd value feedback on how best to frame reproducible audio-input trust-boundary evaluations. https://github.com/zopair/Siren

### NVIDIA AI Security

> Sharing Siren-Trap, an open-source alpha research prototype exploring defensive acoustic canaries and multimodal AI security evaluation. The current implementation emphasizes an inert marker, controlled local testing, passive audio analysis, and inspectable telemetry. We are interested in feedback on reproducibility and evaluation methodology—not claiming validated hardware performance. https://github.com/zopair/Siren

### Hugging Face Audio community

> Project introduction: Siren-Trap is an open-source Python alpha prototype for controlled research into audio-input trust boundaries. It combines a fixed inert canary, local test service, passive WAV analysis, and JSONL telemetry. We would appreciate feedback from the audio community on test design, receiver compatibility, and reproducibility. https://github.com/zopair/Siren

### OpenAI evaluation / audio ecosystem

> We are sharing Siren-Trap, an open-source alpha research prototype for defensive multimodal and acoustic-input evaluation. It is intentionally limited to a fixed inert marker, localhost-first testing, passive WAV analysis, and structured telemetry. We are exploring how to make audio trust-boundary experiments more reproducible and would welcome technical feedback. https://github.com/zopair/Siren

### Google DeepMind audio research

> Siren-Trap is an open-source alpha research prototype studying defensive audio-input trust boundaries through controlled acoustic test artifacts and offline telemetry. We are interested in research feedback on measurement methodology and reproducibility, while keeping physical-layer claims limited to what has actually been validated. https://github.com/zopair/Siren

### Anthropic research

> We are sharing Siren-Trap, an open-source alpha prototype for defensive multimodal AI security research. Its narrow focus is controlled audio-input experiments using a fixed inert marker, a local decoy service, observation checks, and structured telemetry. We would value feedback on research framing and evaluation design. https://github.com/zopair/Siren

## Social post drafts

### X post
> Introducing Siren-Trap: an open-source Python alpha research prototype for defensive acoustic and multimodal AI security evaluation. Fixed inert canary, localhost-first test service, passive WAV analysis, and structured telemetry. Research prototype—not a production containment system. https://github.com/zopair/Siren

### LinkedIn post
> **Introducing Siren-Trap — defensive acoustic and multimodal AI security research**
>
> Siren-Trap is an open-source Python alpha research prototype designed to support controlled experiments around audio-input trust boundaries and defensive AI red teaming.
>
> The current implementation includes a fixed inert acoustic canary, a localhost-first instrumented decoy service, observation checks, passive WAV analysis, and structured security telemetry.
>
> The project is intentionally transparent about its limits: it is not a production containment system, and physical receiver compatibility and end-to-end encoder/decoder validation remain open research tasks.
>
> Repository: https://github.com/zopair/Siren
>
> Technical feedback on reproducibility, test methodology, and defensive evaluation is welcome.

## GitHub engagement rules

1. Prefer an existing relevant discussion, contribution guide, community channel, or issue explicitly requesting feedback.
2. Open an issue only when there is a specific, reproducible technical question that belongs in that repository. Explain the connection and ask one concise question.
3. Never open generic "please notice my project" issues, tag maintainers indiscriminately, or post the same message across unrelated repositories.
4. Do not imply that an organization uses, reviews, sponsors, endorses, or collaborates on Siren-Trap.
5. Keep all claims tied to current code, tests, and documented evidence.
6. Follow each community's rules and rate limits; stop if a moderator or maintainer asks you to.
7. Do not send private messages to employees based on guessed personal contact details.

## Suggested sequence

1. Review the current README, threat model, roadmap, and test evidence before each outreach.
2. Start with the PyRIT and Hugging Face Audio communities because they offer the clearest public technical feedback paths.
3. Publish one concise project post on LinkedIn and one on X, then make only relevant, contextual mentions.
4. Approach NVIDIA, OpenAI, Google DeepMind, and Anthropic with organization-specific notes only after a concrete reproducible evaluation result or a well-scoped technical question is ready.
5. Record the date, destination, exact message, response, and next action in a private outreach tracker. Do not publish private replies without permission.

## Evidence and source links

- Microsoft AI Red Team: https://learn.microsoft.com/en-us/security/ai-red-team/
- Microsoft PyRIT: https://github.com/microsoft/pyrit
- NVIDIA AI Security: https://research.nvidia.com/ai-security/
- Hugging Face Discord community: https://huggingface.co/discord-community
- Hugging Face Audio community: https://huggingface.co/learn/audio-course/en/chapter0/community
- OpenAI official account verification: https://help.openai.com/en/articles/11725090-verifying-communications-from-openai
- OpenAI Evals: https://github.com/openai/evals
- OpenAI audio evaluation examples: https://github.com/openai/openai-cookbook/tree/main/examples/audio/duplex_voice_agent_evaluation
- Google DeepMind PhaseCoder: https://github.com/google-deepmind/phasecoder
- Google DeepMind research: https://github.com/google-deepmind/deepmind-research
