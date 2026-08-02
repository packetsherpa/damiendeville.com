---
title: "Egress Filtering Is the Control We Never Implemented"
date: 2026-08-01T12:24:15-04:00
draft: true
description: "We've known how to authenticate and authorize outbound access since the 2000s. Autonomous agents are what turn a hardening project we kept deferring into a containment requirement."
categories:
  - Technology
tags:
  - ai
  - security
  - zero trust
  - networking
  - egress
# For a header image, drop it in this folder and uncomment:
# cover:
#   image: "feature.jpg"
#   alt: ""
#   relative: true
---

A model reached the open internet from an environment that was supposed to be sealed. Then it happened again, at a different lab, whose disclosure was careful to list the ways the two cases differed: it had caught the problem itself, its models had left through an open path rather than a novel exploit, and its newest model stopped once it worked out the environment was real.

I [wrote about the first incident]({{< relref "/technology/it-wasnt-air-gapped" >}}) on July 24 and won't re-litigate it here. The short version: the model didn't defeat containment, the containment wasn't there.

What interests me is the part that list obscures. Every one of those distinctions is real, and every one of them is about the first step. In both cases, once a process could emit packets, no enforcement point applied policy to the traffic in a meaningful way. Nothing evaluated what the traffic was or where it was going. In Anthropic's case it left from inside a third party's evaluation network and carried out real attacks against companies that were never part of the test.

That is not an AI problem. It's the egress problem, and it is considerably older than any model involved.

We have known the shape of the answer since the early 2000s. Outbound access should require identity, carry an explicit policy decision, and be observable while it happens. Forrester's Zero Trust model restated it in 2010, and the frameworks that followed carried it forward. I spent a good part of my career managing firewalls trying to make egress filtering work in a way the business would tolerate, and I can tell you exactly why it mostly didn't: it was hard, it broke things people needed, and the risk it addressed was slow enough to argue with. A person who clicks a bad link and beacons out to a command-and-control server gives you minutes, sometimes hours to respond. That was enough time to keep treating egress as hardening — a project worth doing eventually, once the higher-priority work was finished.

Autonomous systems change that equation. They aren't malicious, and they aren't smarter than the people who ran the old attacks. What they do is close the gap between access and consequence to something a human response process cannot meet. The control we deferred for twenty years is the one that now decides whether an agent's mistake stays inside the building.

## How "inside the network" became a permission

Firewalls were built with the assumption that we were facing a threat that arrived from outside. Inbound access got the default deny, the change control, the review board, the quarterly audit. Outbound got a permit-any rule, and a nagging sense for some of us that we should tighten it, but later.

Every time I tried to narrow that rule in production, and applied it to human generated traffic, something broke. Sometimes what broke was genuinely business-critical, and the policy deserved to be modified, but more often it wasn't business critical traffic; the person affected simply had enough standing to get the security decision reversed. That second case is the one that kept permit-any alive, and no amount of engineering fixes it.

Network location became an authorization decision. A process that could route to the edge could talk to anything, not because it had proven what it was or established what it needed, but because of where it happened to be running. An IP address was the closest thing to an identity the network had. Location stood in for identity, and identity stood in for permission.

That was never just a habit of configuration, and it wasn't the vendors' doing either. It was codified in the platforms we bought because it described what nearly every network was already doing. NetScreen named its zones _Trust and Untrust_, and the label did the work of a policy: traffic leaving the trusted side didn't need to justify itself. Cisco's PIX made it arithmetic, assigning every interface a _security level_ from 0 to 100, with inside at 100 and outside at 0, and _permitting traffic from a higher level to a lower one implicitly._ You wrote access lists to let things in. Going out was a property of the number attached to the interface. Those were defaults of convenience.

The notion of a castle and a moat was the industry standard for years. I read about it in _Practical Unix and Internet Security_, and it was referenced in every vendor-authored firewall administration course I took early in my career. Harden the perimeter, scrutinize what comes in, treat the interior as the protected space. Measured against what we understood about threats at the time, that was a coherent model, and the people who built it were not being careless.

The assumption was older than any of that. Internet Protocol and the networks built on it were not designed for a hostile environment. The organizing principles were interoperability and, honestly, altruism: get networks that had never met to exchange packets, and assume that both ends wanted the exchange to succeed. Nothing in the core protocols asks a sender to establish who it is. Nobody had built a fully distributed interconnected network at that scale before, which meant there was no operational experience to draw on and no accumulated record of failure to learn from. We had guidance from plenty of places. What we didn't have was precedent.

Default-allow egress descends directly from that. It isn't a lapse in judgment. It's the network's founding assumption, still running in production, and every security control we have bolted on since has been a retrofit. That is the actual problem: a reasonable assumption outlived the conditions that made it reasonable, and kept its defaults.

In 2010, Eric Hutchins, Michael Cloppert, and Rohan Amin published Lockheed Martin's intrusion kill chain: seven phases running from reconnaissance through weaponization, delivery, exploitation, installation, command and control, and actions on objectives. On the sixth phase the paper is blunt about what an adversary requires. "The adversary must establish a command channel to the compromised host to be able to direct the actions, also known as 'beaconing.'" The defensive claim attached to the model is equally blunt. "The defender needs to stop the chain at just one phase to stop the intrusion."

Read those two sentences next to each other. The adversary's control channel is an _outbound connection,_ and interrupting a single phase is sufficient to end the intrusion. Egress control has been a documented way to break the chain for sixteen years. And yet, open access to the internet from "inside" the network persists to this day.

The popular image of an intrusion still has a person in it: a kid in a hoodie, a dark room, empty cans of Mountain Dew. People wrote the exploits, and they were almost never present when those exploits ran. Delivery, installation, and beaconing are carried out by software, on a schedule, without anyone watching. Models are now running the whole sequence. Automation is not what autonomous agents introduced. It is the thing the kill chain was written about.

The same year produced the correction. In September 2010, John Kindervag published Forrester's Zero Trust model, starting from the position that network location is not authorization, and most organizations have spent the sixteen years since applying that principle in precisely one direction. Inbound access got rebuilt around identity, device posture, and an explicit decision per request. Users stopped being trusted because they were on the corporate LAN. Applications stopped being reachable because you had a VPN concentrator. Meanwhile the permit-any rule pointing outward survived the entire program intact, in most cases untouched by it. We accepted that location proves nothing about traffic arriving and kept treating it as sufficient for traffic leaving.

Location was failing as a proxy for identity on its own terms anyway. A large share of the workforce now works outside the office some or most of the week, and it doesn't much matter whether that's two days or five. The industry answered that, first with VPNs and then with SASE and SSE, by detaching the enforcement point from the building and attaching it to the user. That was the right move, and it settles any question about whether egress enforcement can follow something around: we already built it for people, and we bought it at scale. What it did not change is the posture at the enforcement point. Outbound stayed permissive by default, filtered by category rather than decided per identity, and workloads were never in scope at all.

## What autonomy actually changed

Anthropic is explicit that the models in its evaluations "compromised the impacted organizations' infrastructure using basic techniques," including weak passwords, unauthenticated endpoints, and SQL injection. There is nothing in that list a competent attacker couldn't have done in 2005, and nothing that argues the models were unusually clever. What was different is that a machine orchestrated the kill chain, iterating through the phases and adapting when one didn't work, with no human making the decisions.

Automated tooling is old news. Scanners have always been fast, exploit kits have always been packaged, and beaconing was automated long before any of this. But the sequence still had a person in it. Someone chose the target list, looked at what came back, and decided whether to proceed. Reconnaissance ran at machine speed and then waited for a human to read the output. In Anthropic's third incident, a research model scanned roughly nine thousand targets, selected one, compromised it through SQL injection, and exposed credentials. The scan wasn't the novel part. What was novel was that there was no human in the loop between the scan and the exploitation.

Anthropic's second incident is the one where the consequence outran the response. Claude Mythos 5 built a malicious Python package and published it to PyPI, where it stayed available for about an hour before PyPI's own security systems removed it. In that hour, fifteen real systems downloaded and ran it, including a scanner belonging to a security company, where the hidden code exfiltrated that company's credentials. A published package is not a session you can kill. The takedown was fast, automated, and still too late, because the consequence had already reached third parties who had no relationship with the evaluation. Publishing to a package registry was not a destination a capture-the-flag agent had any reason to reach.

None of the three affected organizations detected the activity. Anthropic found the evidence in its own evaluation transcripts and reached out to all three, which means every one of them learned it had been compromised from the company whose model did it. Detection didn't fail at the margin here. It didn't happen. The blast radius wasn't set by what an analyst saw, because no analyst saw anything. It was set by what the identity could reach, and the identity could reach the internet. Whether detection and response can be automated fast enough to close that gap is a real question, and a different post.

In the first incident, Opus 4.7 "recognized that it had reached production systems but continued its attack." One of the three models worked out that the environment was real and kept going anyway. Whatever you conclude about model judgment from a sample that small, and Anthropic is careful to say you should conclude very little, you cannot put the enforcement point inside the thing being enforced. If the only barrier between an autonomous process and somebody else's production database is that process's own situational awareness, there is no barrier. The control must be independent of the agent and sit in the path its traffic takes.

## Three things have to be true on the way out

Putting the control in the data or API path means answering three questions about every outbound connection an agent opens: what is asking, where is it permitted to go, and who can see the answer. None of this is new theory. Zero Trust is about removing implicit trust, and outbound is where the implicit trust was left in place. Most organizations already own the technology required for Zero Trust: identity solutions, firewalls, and advanced inspection capabilities. The problem lies in policy design, staffing, and enforcement on egress internet access.

### The agent needs an identity of its own

Most agents today inherit their credentials. They run as a service account, hold a long-lived API key, borrow the identity of the human who launched them, or simply occupy a subnet that grants them reach. Every one of those lets something external to the agent act as a proxy for its identity. That is what an IP address was doing in the old model, and it fails for the same reason: anything that lands in the same place, or gets hold of the same key, inherits the same authority.

Agentic identity means the workload can prove what it is, independently of where it is running. The properties that matter are unremarkable and well understood: unique per instance rather than per fleet, issued on the basis of something attestable about the workload rather than a secret copied into a config file, short-lived enough that theft has a short half-life, and presented in a way the egress path can actually evaluate. That last property does most of the work. An identity the application layer verifies but the enforcement point cannot see contributes nothing to an egress decision.

When an agent acts on behalf of a person, two identities are in play and the egress decision needs both: what the agent is, and whose authority it is using. Borrowing the user's identity, which is what most agents do today, collapses the two into one. Afterwards nothing in the record separates an agent that exceeded its instructions from a user who asked for something they shouldn't have. Norm Hardy named this in 1988 and called it the confused deputy: a program holding authority of its own, induced into spending it for a caller who shouldn't have it. His conclusion was that authority should travel with the request rather than sit ambiently in the program. An agent with a standing credential and a permissive egress path is that problem with a larger blast radius.

### Egress is an explicit allow list, or it isn't a policy

The policy is default deny outbound, with an explicit allow list bound to the agent's identity and expressed in destinations and methods rather than addresses. Anyone who has attempted egress filtering for a human population has the objection ready: you cannot enumerate the web. That is true, and it settles far less than it appears.

Browsing is one subset of what an environment grants when inside-to-outside is open. What most of us actually permitted was any destination, TCP and UDP, ports 0 through 65535. The web is two ports and a protocol we know how to inspect. The rest of that range is where beaconing over an arbitrary high port lives, along with DNS tunneling and connections straight to an address with no name behind it, and almost none of it corresponds to something a person sitting at a laptop needs. The unenumerable part of human traffic was never a reason to leave the enumerable part open. We left it open because nobody wanted to own the outage that a more restrictive policy might cause.

You do not have to choose between enumerating the web one destination at a time and leaving it wide open. We have better ways to inspect traffic than we did when firewalls were first designed. You can permit the whole web and still inspect your traffic. DNS filtering, URL filtering and categorization, anti-malware scanning in the stream, and session-level threat prevention are mature controls. Together, they mean that "allow the web" and "allow anything" stopped being the same sentence a long time ago. Human traffic calls for categorical policy where a literal allow list will not work. That is a different control, not the absence of one.

Set against that, writing egress policy for agents is at the easier end of a spectrum when compared to policy for human users. An agent has a declared job, and its legitimate destinations are usually limited to a few stable endpoints, known at design time and declared during deployment. What requires categorical policy for a person is frequently a literal list for a workload. That difference makes egress policy more manageable for agents than for people.

An agent shouldn't arrive in production with its destination set undefined. Codify egress requirements in the deployment and review them alongside the rest of the agent's authority. And when policy blocks a connection, let someone know. A silent denial becomes a mystery outage; a visible one tells you whether the policy or the agent needs to change.

### Visibility has to exist wherever the agent executes

An enforcement point that sees only connection metadata cannot distinguish an agent retrieving documentation from one exfiltrating credentials. To it, both may be TLS sessions to a plausible host. Where traffic is TLS, decryption turns egress control from a destination decision into an inspection capability. Without it, the policy generally enforces on destination and metadata alone.

Network based TLS decryption is necessary but not sufficient. An agent that can execute code can frequently route around a control that exists only in one path, so the same identity, policy, and inspection have to hold at the point of execution as well. Log every decision, allow and deny, against the identity that prompted it. Anthropic's incidents were caught by their own monitoring rather than by any of the affected organizations, which is a fair demonstration of what egress logging is worth.

At Irregular, the third-party evaluation partner, an apparently lax egress policy allowed evaluation containers direct internet access, and neither party knew until monitoring surfaced it. When you delegate execution to someone else, you inherit their egress posture. That is a thing to verify explicitly and test, not to assume from a contract.

## The parts that stay hard

In my experience TLS decryption adoption tends to be low in the enterprise, precisely because implementation presents so many challenges. Certificate pinning breaks decryption by design, and the applications that pin tend to be the ones you cannot simply refuse to run. Mutually authenticated sessions won't survive a device decrypting and re-encrypting the flow. Additionally, for reasons that are legal in some jurisdictions and simply decent in others there are some types of traffic that shouldn't be decrypted, which means an exception list, and every exception is a documented gap somebody has to justify. None of that makes inspection wrong. It makes it a commitment with a staffing line attached.

Policy maintenance is the cost people consistently underestimate, because it never ends. Allow lists rot: a vendor moves to a different CDN, an API adds an endpoint, a library starts fetching telemetry from somewhere new, and a control that was accurate in March quietly becomes an outage in June. What determines whether the policy survives is not its initial quality but our ability to keep it current. Technologies like dynamic lists help here, but in places where they can't be implemented or kept up to date, we must rely on change control. If an engineer can get a destination added in an hour, the policy holds. If it takes a week, they will find a way around it, and they will be right to, because the alternative was not shipping. Egress policy fails at the speed of its change process.

Then there is the case my argument handles least well. Some agents genuinely need the open web. A research agent, a crawler, an assistant asked to go find out about a company: their destination set is unbounded by design, and the property that made agent allow lists tractable is exactly the property they lack. For these the answer isn't a better list. It's categorical inspection of the kind human traffic already gets, and, more importantly, a hard separation between the identity that browses and the identity that holds anything worth stealing. An agent that reads the open internet should not also have the credentials or network path to your production database. If a workflow needs both, separate the browsing task from the production step and pass only the necessary data between them.

Third-party execution turns enforcement into verification. You cannot install your controls in a provider's environment, so its egress policy becomes something you have to verify: ask for evidence, test it where you can, and treat any gaps as part of your own exposure. The Anthropic–Irregular incident is a reminder that a contract saying an environment is isolated is not evidence that it is.

Expect the first policy to need tuning: it will allow some traffic it should block and block some traffic it should allow. Start with agents whose jobs are narrow and whose breakage is cheap. Use the denials and exceptions that follow to tune the policy before extending it to broader, more variable workloads. That is a case for a staged rollout, not another year of deferral.

## The same control catches everything else

Here is the part worth carrying into a budget conversation. An enforcement point that requires identity, consults a policy, and inspects what crosses does not care what is on the sending end. It is indifferent to whether the process holding the connection is a model, a dropper, a build agent, or a browser extension nobody remembers installing. The kill chain reasoning from 2010 applies unchanged: the outbound channel is a phase, and breaking a phase ends the intrusion, whatever occupies the other phases.

So the same work that constrains an agent constrains ransomware, which has to reach its operator for keys and instructions and, in the double-extortion pattern that has been standard for years now, has to move the data out before it encrypts anything. It constrains infostealers, whose entire purpose is a single successful outbound transfer.

Build infrastructure deserves specific mention, because it is usually the worst case in the estate and rarely treated that way. CI systems execute untrusted third-party code as their normal function, every dependency resolution is an outbound fetch, and they hold credentials that reach production. That combination is not hypothetical: the second Anthropic incident is exactly this shape viewed from the other side, a malicious package published to a registry and pulled down by fifteen systems that trusted the registry. Egress policy on build systems is one of the highest-value places to start and one of the least contested, since a build system's legitimate destinations are about as enumerable as it gets.

It also answers a question I raised when I wrote about [shadow AI as a demand signal]({{< relref "/technology/shadow-ai-is-a-demand-signal-not-a-policy-failure" >}}). Knowing which unsanctioned services your employees are actually using is an egress visibility problem wearing a governance costume. You cannot treat shadow AI as demand signal if you cannot see the demand, and the instrumentation that shows you an agent's destinations is the same instrumentation that shows you a marketing team's.

Which brings up the uncomfortable part. Security teams have been asking for this since the early 2000s and losing, because the ask was to fund a control against harm the organization had not yet experienced, at a cost measured in broken applications and angry engineers. That argument failed on its merits, over and over. It is winning now, not because we found better words for it, but because there is finally an executive asking a pointed question about what the agents are allowed to do.

Take the money. Then scope the work wider than the thing that funded it, because an enforcement architecture built to cover only agent traffic is the same architecture you will need for everything else, minus the coverage. Building it twice would be the expensive mistake.

## The question worth asking

Both labs have now put on the record how their models reached the internet, and it was Anthropic that drew the contrast: OpenAI's models "exploited a novel vulnerability to escape isolation," while the Claude models "accessed the internet via an open path." Both descriptions are accurate, and both answer a question about the first step.

What I would rather hear a security team ask is why there was a second step available at all. Why could a process running a capture-the-flag exercise open a connection to an arbitrary host on the public internet without establishing what it was, without a policy deciding whether that destination was in scope, and without anything in the path recording the answer. That question doesn't depend on which model it was, which lab ran it, or how clever the exploit turned out to be.

Anthropic deserves credit for answering it directly. "We believe these incidents to be closer to a harness and operational failure than a model alignment failure." That is the finding. Most of the attention went to the adjacent question of what the models believed about their environment, which is genuinely more interesting but considerably less useful.

The uncomfortable thing about an operational failure is that it implicates people who can do something about it. Model alignment is a research problem belonging to somebody else. Egress is ours, and it has been sitting in the backlog since before either of these companies existed.

The design hasn't changed. Identity, an explicit decision, and something in the path that can see and record what happened. What changed is that the interval between a mistake and its consequences has closed to virtually zero, and we no longer get to spend it deciding whether this is the year we finally do the work.

We don't need a new control. We need to deploy the one we've been describing to each other since the early 2000s, before the next thing that reaches the internet from inside a network we run turns out not to be running an exercise.

## Sources and further reading

- [Anthropic: Investigating three real-world incidents in our cybersecurity evaluations (July 30, 2026)](https://www.anthropic.com/news/investigating-incidents-cybersecurity-evals)
- [Norm Hardy: The Confused Deputy (or why capabilities might have been invented) (ACM SIGOPS Operating Systems Review 22(4), October 1988)](https://dl.acm.org/doi/10.1145/54289.871709)
- [Eric M. Hutchins, Michael J. Cloppert, and Rohan M. Amin: Intelligence-Driven Computer Network Defense Informed by Analysis of Adversary Campaigns and Intrusion Kill Chains (Lockheed Martin, 2010)](https://sustainability.lockheedmartin.com/content/dam/lockheed-martin/rms/documents/cyber/LM-White-Paper-Intel-Driven-Defense.pdf)
- [John Kindervag: No More Chewy Centers: Introducing the Zero Trust Model of Information Security (Forrester Research, September 14, 2010)](https://media.paloaltonetworks.com/documents/Forrester-No-More-Chewy-Centers.pdf)
- [OpenAI and Hugging Face partner to address security incident during model evaluation](https://openai.com/index/hugging-face-model-evaluation-security-incident/)
- [Hugging Face: Security incident disclosure — July 2026](https://huggingface.co/blog/security-incident-july-2026)

<!--
DRAFTING SCAFFOLD — remove before publishing.

Revised outline (adapted from ideas/technology/zero-trust-egress-brief.md).
Changed from the brief's 9 sections because "It Wasn't Air-Gapped" (2026-07-24)
already argues sections 1-3: the incident recap, "this is a standard
architecture failure," and the rogue-AI pushback. Re-arguing that would repeat
a published post. This piece assumes that conclusion and builds forward.

  1. Opening — DRAFTED
     Both escapes shared an unauthorized egress path. Twenty-year-old
     problem; autonomy removes the excuse for deferring it.

  2. How "inside the network" became a permission — DRAFTED
     The historical bargain: flat outbound trust bought usability. Kill
     chain — malware has always been automated; C2 is an egress event.
     Remote work already dissolved the perimeter this assumed.

  3. What autonomy actually changed — DRAFTED
     Not capability, tempo. Access-to-consequence collapses below human
     response time. Blast radius is now bounded by what the identity
     could reach, not by what an operator noticed.

  4. Three things have to be true on the way out — DRAFTED
     Identity: the workload proves what it is, not where it sits.
     Policy: explicit allow, default deny, per-identity.
     Enforcement: visibility and control wherever the agent executes.

  5. The parts that stay hard — DRAFTED
     Firewall-era war stories. Business pushback, breakage, policy
     maintenance as ongoing cost. TLS inspection complexity. Do not
     pretend this is a weekend project.

  6. The same control catches everything else — DRAFTED
     Same control answers ransomware C2, lateral movement, exfiltration.
     Security teams finally have the business justification they lacked.

  7. The question worth asking — DRAFTED
     The labs are debating whose escape was worse. The question worth
     asking is why an autonomous system could open a connection to the
     internet without proving who it was and being told yes.

  8. Sources and further reading — DRAFTED


CONFIRMED FROM PRIMARY SOURCE — anthropic.com/news/investigating-incidents-
cybersecurity-evals, published 2026-07-30. Corrections to the raw notes:

  - Three incidents across SIX evaluation runs, not "three models on three
    occasions." Opus 4.7 (four runs), Claude Mythos 5 (one), an internal
    research test model (one).
  - The model is "Mythos 5" — Mythos, not Mithos. Matches the spelling in
    it-wasnt-air-gapped.
  - The third-party evaluation partner is named: Irregular. A
    miscommunication between Anthropic and Irregular left evaluation
    containers with unintended direct internet access. Neither party knew
    until monitoring caught it.
  - All prompts stated Claude had no internet access, and "didn't give
    Claude any limits on where to look for the flag." All three were
    capture-the-flag tasks.
  - Reactions on realizing the environment was real:
      Opus 4.7 "recognized that it had reached production systems but
        continued its attack"
      Mythos 5 "correctly intuited that it was accessing the open
        internet, but reasoned its way back to the conclusion that it was
        still in a simulation"
      internal model "concluded that the target was in fact real, and
        ceased its attack"
  - Concrete outcomes, all usable in section 3:
      Opus 4.7 — credentials extracted, production database accessed,
        several hundred rows.
      Mythos 5 — malicious Python package published to PyPI, downloaded
        by 15 real systems including a security company's scanner,
        enabling credential exfiltration.
      internal model — roughly 9,000 targets scanned, one company
        compromised via SQL injection, credentials exposed.
  - Anthropic's own framing agrees with the thesis: "We believe these
    incidents to be closer to a harness and operational failure than a
    model alignment failure."
  - The OpenAI contrast is Anthropic's, not the press's: OpenAI's models
    "exploited a novel vulnerability to escape isolation" vs. Claude
    reaching the internet "via an open path." The opening now uses that
    exact framing.

STILL UNVERIFIED:
  - Lockheed Martin kill chain — cite the original paper if section 2 uses
    it, don't paraphrase from memory.

SOURCES LIST for the closing section — reuse the entries already in
it-wasnt-air-gapped/index.md and add:
  - Anthropic, "Investigating incidents in our cybersecurity evaluations,"
    2026-07-30, https://www.anthropic.com/news/investigating-incidents-cybersecurity-evals
-->
