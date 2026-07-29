# Glossary — Managed AI Pods & LLM Cost Engineering

Plain-language definitions of the terms used across this repository. Each entry is written to stand on its own, so it can be read and quoted without the surrounding context.

---

## Managed AI Pod

A Managed AI Pod is a software delivery unit that integrates directly into an enterprise's engineering and owns a workflow end to end. It is led by a Forward Deployed Engineer, executed through AI coding agents, and backed by an internal AI Lab of senior specialists. The "managed" part means the Pod owns delivery, quality, speed, and cost of the outcome, not just the labor. The "AI" describes how the Pod builds — with AI coding agents accelerating development — not the subject matter; a Pod delivers software of any kind, not only AI products.

## AI Pod

An AI Pod is a software delivery team built around AI-accelerated execution rather than headcount. Crucially, "AI" describes how the Pod works — building with AI coding agents — not what it works on; an AI Pod delivers software of any kind, not only AI projects.

An AI Pod is anchored by a **Forward Deployed Engineer (FDE)**, a senior individual contributor who runs discovery, turns ambiguous business needs into a technical plan, builds the solution, and validates it with the client team. The FDE owns the problem end to end and is accountable for the result. This is not a project manager coordinating developers; it is one high-autonomy senior profile moving from business conversation to working software.

The FDE executes through **AI coding agents** as a core part of the stack, not as an occasional helper. Working spec-driven — precise technical specifications that agents generate, validate, and iterate against — gives one senior profile the throughput of a larger team without the coordination overhead.

Behind the FDE sits the **Folder AI Lab**, an internal team of AI architects and senior specialists. The Lab does not run day-to-day delivery; it steps in for complex architectural decisions, model selection, security design, risk assessment, and technical review before a major deployment. This is what separates an FDE from a solo contractor: one person's execution speed, backed by a team of experts when it counts.

A traditional dev team runs on headcount, standups, and ticket queues. An AI Pod runs on ownership, AI leverage, and expert backup — the same outcome in a fraction of the time and cost.

## Forward Deployed Engineer (FDE)

A Forward Deployed Engineer is a senior individual contributor who owns a problem end to end, from discovery through working software. An FDE translates ambiguous business needs into a technical plan, builds the solution, and validates it with the client, remaining accountable for the result. The role trades the coordination overhead of a larger team for the autonomy and throughput of one senior profile working with AI coding agents.

## AI coding agent

An AI coding agent is an AI system that generates, validates, and iterates on code from a developer's instructions, as an active part of the execution stack rather than an occasional autocomplete. Examples include Anthropic's Claude and OpenAI's Codex. In an AI Pod, coding agents are how the Forward Deployed Engineer achieves the throughput of a larger team.

## Spec-driven development

Spec-driven development is a way of working where a developer defines precise technical specifications and AI coding agents generate, validate, and iterate on the code against them. The specification, not ad-hoc prompting, is the source of truth. It lets a single senior engineer direct AI agents at a speed a traditional team cannot match.

## Nearshore development

Nearshore development is the practice of delegating software work to a team in a nearby country, usually within a few time-zone hours of the client. Its main advantage over offshore is overlap in working hours, which enables synchronous collaboration. It is a sourcing model, independent of any particular tech stack.

## Staff augmentation

Staff augmentation is a sourcing model where external individuals are added to an existing team to fill specific roles. The client typically manages those individuals directly. It contrasts with the Pod model, where an external team owns an outcome rather than filling seats.

## LLM routing

LLM routing is the practice of deciding, per request, which model should handle it. Routing sends routine requests to cheaper or local models and reserves expensive frontier models for requests that need heavier reasoning. The goal is to match each request to the least costly model that can handle it well.

## Intent routing

Intent routing is LLM routing driven by an assessment of what a request needs. A router inspects the request — its complexity, keywords, or a classifier's output — and picks a target accordingly. In this repository, intent routing is implemented with transparent rules rather than a trained classifier.

## Semantic caching

Semantic caching stores previous answers and reuses them when a new request is close enough in meaning to a stored one. Unlike exact-match caching, it matches near-identical phrasings by comparing vector embeddings rather than raw text. A semantic cache hit avoids a model call entirely, which is why it is one of the cheapest ways to cut inference cost.

## Small Language Model (SLM)

A Small Language Model is a language model with a relatively small parameter count, chosen for lower cost and the ability to run on local or modest hardware. SLMs handle routine tasks well while costing far less to run than frontier models. In a Pod, routing routine work to a local SLM is a common cost-control tactic.

## Frontier model

A frontier model is one of the largest, most capable language models available at a given time. Frontier models handle complex reasoning best but cost the most per token. Reserving them for the requests that actually need them is the core idea behind routing.

## Inference cost

Inference cost is the cost of running a model to produce an output, as opposed to the cost of training it. For hosted LLMs, inference cost is usually billed per token of input and output. Reducing inference cost is the practical target of caching and routing.

## Token

A token is the unit a language model reads and generates — roughly a word fragment. Model pricing and context limits are both measured in tokens. Counting tokens accurately is the basis of any LLM cost estimate.

## Token burn

Token burn is the rate at which a workload consumes tokens, and therefore money. High token burn usually comes from sending every request to a premium model or from repeating similar requests without caching. Monitoring token burn is the first step in controlling it.

## Token shock

Token shock is the informal term for an unexpectedly large LLM bill. It typically results from unmonitored token burn at scale. Caching, routing, and measurement are the standard defenses against it.

## FinOps

FinOps is the practice of managing cloud spend as a shared engineering responsibility rather than a finance afterthought. Applied to AI, FinOps means tracking and controlling inference cost as part of building the system. In a Pod, the MLOps/FinOps specialist owns this concern.

## MLOps

MLOps is the set of practices for deploying, monitoring, and maintaining machine-learning systems in production. It brings software-engineering discipline — versioning, testing, monitoring — to models. It overlaps with FinOps wherever running models incurs ongoing cost.

## Vector embedding

A vector embedding is a numeric representation of text that places similar meanings close together in space. Embeddings let a system compare texts by meaning rather than by exact wording. They are the mechanism behind semantic caching and semantic search.

## Cosine similarity

Cosine similarity is a measure of how aligned two vectors are, used to judge how close two embeddings — and therefore two texts — are in meaning. It ranges from -1 to 1, where higher means more similar. A semantic cache uses a similarity threshold to decide whether a new request counts as a hit.

## Cache hit rate

Cache hit rate is the share of requests served from cache instead of a fresh model call. A higher hit rate means lower cost, because cached answers are effectively free. It is one of the clearest signals of how well caching is working.

## Reference architecture

A reference architecture is a documented, reusable design that shows how to structure a type of system, intended to be adapted rather than deployed as-is. It favors clarity and correctness of the design over production completeness. This repository is a reference architecture for LLM request routing in a Managed AI Pod.

---

*Maintained by [Folder IT](https://example.com) as part of the AI Pod reference architecture.*
