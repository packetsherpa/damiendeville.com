# There Is No Such Thing as "AI Security"

One of the biggest mistakes I see organizations make is talking about **AI security** as though it's a single initiative.

It isn't.

In practice, enterprises are facing several fundamentally different architectural problems. Each has different trust boundaries. Each has different ownership. Each requires different governance, controls, and operational practices.

Treating them as one security program inevitably creates gaps.

Understanding those differences is one of the most important conversations security leaders can have today.

## The Problem Isn't AI

Security teams naturally think in terms of discovering and mitigating new vulnerabilities.

Find the weakness.

Patch the weakness.

Move on.

Generative AI doesn't fit neatly into that model.

An attacker doesn't have to compromise the model itself.

They only have to influence what the model reads.

Think of malicious instructions embedded inside HTML comments or hidden white text on a webpage. If a large language model has access to sensitive information and the ability to perform actions, those instructions can manipulate the model into exposing data or taking unintended actions.

The objective isn't new.

It's as old as information security itself: steal valuable information.

Prompt injection doesn't represent a new attacker objective.

It represents a new delivery mechanism for an old objective: data exfiltration.

Many of the risks we're discussing today aren't software defects waiting to be patched.

They're properties of how these systems are designed.

Security researcher Simon Willison summarizes this with what he calls the **Lethal Trifecta**:

- The AI can access private data.
- The AI can consume untrusted content.
- The AI can perform actions that communicate with the outside world.

Individually, none of those capabilities is particularly remarkable.

Together, they create something fundamentally different.

## 1. Employees Using Commercial AI Services

The first category is the one most organizations encounter first.

Employees use ChatGPT, Claude, Gemini, Microsoft Copilot, or AI capabilities embedded into commercial SaaS applications.

Here, the model lives somewhere else.

You don't control its architecture.

You don't patch it.

You don't determine how it's trained.

The model isn't your asset.

Your data is.

That shifts the conversation back toward familiar security disciplines:

- Visibility into AI usage
- Identity and access management
- Data loss prevention
- Governance and contractual controls
- Acceptable use policies

The objective isn't protecting the model.

It's protecting your information before it leaves your organization.

## 2. Building AI Applications

The second category looks completely different.

Here, your engineering teams are building retrieval-augmented generation (RAG) systems, copilots, assistants, customer-facing chatbots, and autonomous agents.

Now you own the architecture.

You own the development lifecycle.

You own the CI/CD pipeline.

You choose the models.

You decide which tools the agent can invoke.

You assign identities and permissions.

The software supply chain now includes models, datasets, prompts, embeddings, vector databases, orchestration frameworks, and AI-specific dependencies alongside traditional software components.

Every design decision becomes part of your security posture.

## 3. Agentic Software on the Endpoint

The third category may prove to be the most disruptive.

Coding assistants, desktop agents, and computer-use systems don't ask you to upload information.

They come to where the information already lives.

They inherit your credentials.

They read local files.

They execute shell commands.

They browse the web.

They install packages.

They commit code.

They push to Git.

In other words, the Lethal Trifecta already exists before anyone writes a single prompt.

Traditional endpoint security wasn't designed for software making legitimate decisions using legitimate credentials.

The challenge isn't malware.

The challenge is intent.

## The Security Boundary Keeps Moving

Although these three scenarios all involve AI, they don't share the same control points.

With commercial AI, the security boundary sits at the organizational edge. Your objective is controlling what leaves your environment and what returns.

With internally developed AI, the boundary moves into your architecture and software supply chain. Your objective is designing secure systems from the beginning.

With agentic endpoint software, the boundary shifts again—to the endpoint itself. Your objective becomes constraining what powerful software can do with legitimate access.

Treating these as one security program inevitably produces gaps because each requires different controls, different operational models, and different ownership.

That's why there is no single "AI security" solution.

There are multiple AI security problems.

Each deserves its own architecture.

Each deserves its own governance model.

And each requires security leaders to think less about protecting AI itself and more about understanding **where the trust boundary actually exists.**