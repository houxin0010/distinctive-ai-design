# Distinctive AI Design

[中文](README.md) | **English**

A design workflow skill for Codex that helps AI move beyond familiar templates and develop a clear, distinctive visual direction for websites, applications, and game interfaces.

It organizes design work into **Discover → Define → Deliver**: explore alternatives, turn a direction into a coherent interface, and refine the result using real screenshots and deliberate removal of unnecessary elements. Visual decisions stay grounded in the target user and their primary task.

## When to use it

- Explore visual concepts for a new product, landing page, or game interface.
- Redesign a functional page that lacks identity or clear hierarchy.
- Reduce the template feel of repetitive cards, mechanical layouts, and purposeless decoration.
- Improve consistency across typography, composition, imagery, and interaction within an existing aesthetic.
- Get specific feedback from real screenshots, then make a bounded set of improvements.

Routine feature changes, isolated styling fixes, and clearly defined small problems can be handled directly without the full exploration process. Existing brand guidelines, the user's chosen direction, and the project's technology stack remain constraints.

## Core techniques

| Technique | How it works | Expected output |
| --- | --- | --- |
| Explore distinct directions | Offer roughly three concepts that differ in composition, information structure, typography, or interaction metaphor | Short, comparable direction proposals |
| Write a concrete creative brief | Translate user preferences, dislikes, and product purpose into actionable constraints | A shared basis for design decisions |
| Use a real random seed | When ideas keep repeating, use a local random source to inspire rhythm, grouping, or contrast | Fresh exploration cues; the seed stays out of the product |
| Review screenshots independently | When delegation is permitted, let a fresh review context examine screenshots and the brief | Specific issues, suggested changes, and an indicative score |
| Generate media selectively | Use images or video when they support the core message, then check integration with the page | Purposeful assets and a fallback plan |
| Refine by subtraction | Remove redundant explanations, unnecessary containers, and distracting effects | Clearer hierarchy and primary actions |

These are optional techniques. A task does not have to use random seeds, generate images, or produce video.

## Installation

### Option 1: Ask Codex to install it

In a Codex environment with `skill-installer`, enter:

```text
Use skill-installer to install the skill at the root of https://github.com/houxin0010/distinctive-ai-design, named distinctive-ai-design.
```

### Option 2: Clone it manually

The following commands target the default user skill directory on macOS/Linux:

```sh
mkdir -p ~/.codex/skills
git clone https://github.com/houxin0010/distinctive-ai-design.git ~/.codex/skills/distinctive-ai-design
```

If `CODEX_HOME` is set, install under its `skills/distinctive-ai-design` directory. On Windows, clone or extract the repository into `.codex/skills/distinctive-ai-design` under your user directory.

The destination directory must not already exist. For an existing installation, inspect local changes before replacing anything. Invoke the skill in a Codex session that supports loading local skills; if the current session does not recognize it, try a new session.

### Updating

For a Git-cloned installation with no local modifications:

```sh
git -C ~/.codex/skills/distinctive-ai-design pull --ff-only
```

If Git reports local changes or cannot fast-forward, preserve and resolve those changes before updating.

## Quick start

In your target project, provide the page location, primary task, and constraints, then invoke the skill:

```text
Use $distinctive-ai-design to improve the current homepage.
The audience is independent developers, and the main action is to explore the product and start a trial.
First propose three meaningfully different visual directions, then implement the most suitable one.
Keep the existing stack and components, review real screenshots, and refine the result.
```

The skill's execution instructions are currently written in Chinese. You can request work in Chinese or English. This English README documents the same skill; it is not a separate English-language skill package.

## Examples

### Explore before implementing

```text
Use $distinctive-ai-design to explore main-menu directions for my office-themed game.
I want a restrained office atmosphere with a little humor; avoid neon and excessive skeuomorphism.
Give me three concepts with different composition and interaction structure, explaining how each highlights “Start game.”
Only provide concepts and briefs this round. Wait for my selection before implementing.
```

### Refine an established direction

```text
Use $distinctive-ai-design to improve the product detail page.
Keep the existing brand colors and content, using an editorial layout and clear typographic hierarchy.
Skip direction exploration. Implement the key view, then use screenshots to identify the three most consequential visual issues.
```

### Focus on subtraction

```text
Use $distinctive-ai-design to polish the current dashboard.
Preserve business functionality and necessary status feedback. Look for redundant explanations, decorative containers, and purposeless glow effects.
Improve the experience through removal and hierarchy changes before adding new visual assets.
Verify primary actions and narrow-screen layout, and state what remains unverified.
```

### Use visual assets when they help

```text
Use $distinctive-ai-design to improve this product showcase page.
If a hero image would help communicate the product's purpose, use an available image-generation tool.
Align the asset with the page's composition, palette, and whitespace. Use existing platform capabilities for ordinary animation.
Do not connect new paid services. If generation is unavailable, use a static approach that still supports the primary task.
```

## Workflow and deliverables

1. **Discover:** Read the current interface and constraints; identify the audience, primary task, and intended feeling. Propose comparable concepts when the direction is unclear.
2. **Define:** Write a brief for the chosen direction and implement a representative page or key state using the existing stack and components.
3. **Review:** Capture screenshots of the running interface. Examine composition, hierarchy, typography, asset integration, and details; prioritize one to three major issues.
4. **Deliver:** Remove elements that do not serve the purpose. Verify primary actions, relevant states, and narrow-screen behavior, then report results and limitations.

A brief typically covers the audience and primary task, intended feeling, visual metaphor, composition and hierarchy, colors and typography, key interactions, elements to avoid, and the minimum scope of the first version.

The result should include implementation or design artifacts, the most important changes, and evidence of actual verification. Report aesthetic review separately from functional validation: a screenshot cannot establish that interactions, performance, or accessibility behavior work correctly.

## Review boundaries and environment requirements

| Capability | When needed | If unavailable |
| --- | --- | --- |
| Project file access and implementation tools | Changing a real interface | Keep the task at concept or recommendation level and state the scope |
| A running environment and screenshot tools | Verifying the visual result | Mark visual verification as incomplete |
| An independent subagent | Delegation is permitted and an independent review is useful | Review against the same dimensions and label it a self-review |
| Image or video generation | Media has clear value for the core message | Use existing assets or a static approach and explain the limitation |

The skill does not bundle a browser, generation service, API key, or independent review model. It does not require a particular framework, model version, or paid platform. Optional capabilities depend on the current environment, authorization, and budget.

The critic receives screenshots, the user task, an aesthetic brief, and necessary references—not code, historical rationales, or a target score. Start with at most two rounds, fixing the most important issues each time. If improvement stalls, report the remaining gaps and reconsider the direction rather than chasing scores indefinitely. `9/10` may serve as an internal aspiration; it is not a release guarantee or an objective quality certification.

## Repository structure

```text
distinctive-ai-design/
├── SKILL.md                         # Skill entry point and Chinese execution instructions
├── agents/openai.yaml               # Codex display metadata and default invocation prompt
├── references/review-and-media.md   # Critic prompt and media guidance
├── README.md                        # Chinese documentation
└── README.en.md                     # English documentation
```

[Read the full skill](SKILL.md) · [Read the review and media reference](references/review-and-media.md)

## Source and adaptation scope

This skill draws on Anshu Chimala's [How to turn your AI into a world-class designer](https://www.lennysnewsletter.com/p/how-to-turn-your-ai-into-a-world), published in Lenny's Newsletter. The publicly accessible text was read on **October 7, 2026**.

The material read covers techniques 1–6: random seeds, specific and ambitious prompts, independent critique loops, image generation, video generation, and removal of unnecessary elements. Only the heading of technique 7 was visible. The subsequent subscriber-only text was neither included nor inferred.

This repository contains an independently written operational adaptation, not a copy of the article. Roughly three candidate directions, a two-round review budget, runtime verification, and authorization boundaries are local adaptations rather than fixed requirements from the source. Neither this documentation nor the skill guarantees a particular level of aesthetic quality.
