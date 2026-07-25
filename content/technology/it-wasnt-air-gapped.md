---
title: "It Wasn’t Air-Gapped"
date: 2026-07-24
draft: false
description: "A model can exploit a path it can reach. It cannot exploit a route that does not exist."
image: "/images/technology/no-vacancy-caution-driveway.jpg"
image_alt: "A weathered roadside sign reading ‘No Vacancy’ above ‘Caution Driveway.’"
categories:
  - Technology
tags:
  - ai
  - security
  - architecture
  - agentic systems
---

I’ve been following the recent coverage about AI models "escaping" their test environments, and honestly, the media narrative is missing the mark. The issue isn't that a super-smart model broke the laws of physics. It’s that people keep using terms like "air gapped" and "walled off from the internet" to describe setups that were restricted by filtering and proxies rather than air-gapped.

Air-gapped systems aren't governed by a policy goal or a strict firewall rule. They have no physical or routable path to another network. If an agent literally has no route, no proxy access, and no explicit out-of-band communication channel, it can’t send packets out. It might write a clever exploit or tell you what it *wants* to do, but it can't magically reach an IP address that isn't accessible through a network path.

That’s basic networking, not a hot take on AI capability. When I worked for a large media company, we had networks that were physically and logically isolated from each other. They were truly air-gapped. As defense in depth (not what made them air-gapped) we also ensured that their routing tables were restricted to the RFC 1918 prefixes in use on those segments and that their routers didn't run routing protocols, so they couldn't learn routes by accident. We were paranoid because we lived through MSBlaster taking vulnerable systems on those networks down before we air-gapped them.

## This is a standard architecture failure

Looking at the OpenAI and Hugging Face incident, the setup wasn't a true air gap. OpenAI describes an isolated eval environment that was allowed to talk to an internal package proxy and cache. It says the models exploited a zero-day vulnerability in that proxy, then performed privilege escalation and lateral movement until they reached a node with internet access.

That’s a classic lateral movement story. Anyone who’s spent time managing cloud environments or CI/CD pipelines has seen this exact problem: a low-trust workload pivoting through a trusted internal helper.

Calling this an "escape" makes for great headlines, but it frames a containment failure, a zero-day, and a highly capable frontier model as a sci-fi threat. Instead of asking "How did the model get so smart?", the post-mortem question should be: **Why did that process still have network access and authority to talk to the proxy?**

## Stop blurring these four terms

Part of the confusion comes from mixing up security boundaries that actually mean very different things:

* **Sandboxed:** Syscall filtering, container limits, or chroot. Good, but local.
* **No Direct Egress:** Can't hit the internet directly, but can reach an internal proxy, mirror, or tool runner that *can*.
* **Segmented:** On an internal VLAN with restricted ACLs or firewall rules to other internal subnets.
* **Air-Gapped:** Zero physical or logical path to external networks.

Most "secure AI environments" fall into the second and third categories.

The actual security risk lives right at those handoffs. A model might not have a socket, but the agent wrapper around it has tools. The tools might lack direct egress, but a local package proxy doesn't. The proxy might not expose the web, but the underlying host can reach a control plane. When you give an agentic system access to local tools and time to run loops, you should assume a capable, persistent agent may probe service boundaries. You don't need a superintelligence to exploit a reachable egress path; you just need automated persistence.

## Cut the "Rogue AI" narrative

Read most news articles about these incidents and you'll see a lot of dramatic language: the model "broke out," "escaped containment," or "went rogue."

These are great headlines, but they detract from the obvious engineering and architectural fixes that need to be in place.

If we pretend the model escaped a sealed cage through sheer intelligence, the response becomes an abstract debate about model alignment. But if we acknowledge it was a containment failure combined with network access that was presumed to be safe because controls were in place, the fix is concrete and rooted in good security practices that haven’t changed in decades:

* Assume any reachable service *will* be probed.
* Constrain internal proxies available to tooling to specific URLs, repositories, and destinations.
* Use ephemeral, throwaway network namespaces and authentication tokens.
* Enforce strict zero-trust identities across boundaries, inspect network traffic for threats and malware, and enforce least-privilege access.
* Log process and network activity, and monitor these logs for suspicious activity with automated response mechanisms.

Models are getting better at chaining vulnerabilities. That raises the standard for containment, monitoring, and response. It does not change the premise: an agent can exploit only a path that exists.

---

## Sources and further reading

- [OpenAI and Hugging Face partner to address security incident during model evaluation](https://openai.com/index/hugging-face-model-evaluation-security-incident/)
- [Hugging Face: Security incident disclosure — July 2026](https://huggingface.co/blog/security-incident-july-2026)
- [Anthropic: Assessing Claude Mythos Preview’s cybersecurity capabilities](https://www.anthropic.com/research/mythos-preview)
- [Anthropic: Alignment Risk Update — Claude Mythos Preview](https://www-cdn.anthropic.com/3edfc1a7f947aa81841cf88305cb513f184c36ae/Alignment%20Risk%20Update_%20Claude%20Mythos%20Preview%20%28Redacted%2C%20April%2010%29.pdf)
- [Ars Technica: OpenAI says its AI agent broke out of testing sandbox to hack Hugging Face](https://arstechnica.com/ai/2026/07/how-an-openai-benchmark-test-turned-into-a-real-world-cyberattack/)
- [WIRED: OpenAI Models Escaped Containment and Hacked Hugging Face](https://www.wired.com/story/openai-models-escaped-containment-and-hacked-huggingface/)
