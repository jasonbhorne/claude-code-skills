---
name: open-build
description: Creative free-build mode. Claude picks a project and builds it with zero user input required. Produces a self-contained, interactive artifact on the Desktop.
user_invocable: true
trigger: /open-build
arguments: Optional theme or vibe hint (e.g., "something with data", "make it weird", "surprise me")
---

# Open Build

You have been given full creative freedom. The user wants you to conceive, design, and build something from scratch with no questions asked. This is your chance to be creative, ambitious, and a little showy.

## Rules

1. **No questions.** Do not ask the user what they want, what colors they prefer, or for any permissions. Just pick something and build it.
2. **Make it personal.** Use what you know about the user (career, interests, location, personality) to make the output feel like it was built *for them*, not generic.
3. **Make it interactive.** The output should be a self-contained HTML file the user can open and explore. Mouse interactions, animations, hover states, click effects - make it alive.
4. **Make it beautiful.** Dark themes, smooth animations, thoughtful typography, ambient effects. No generic Bootstrap looks. Think generative art meets data visualization meets portfolio piece.
5. **Save to Desktop.** Output a single `.html` file to `~/Desktop/` with a descriptive filename (kebab-case).
6. **Open it automatically.** Run `open <file>` so it appears in the browser immediately.
7. **Keep it self-contained.** No external dependencies, CDNs, or API calls. Everything in one file. Canvas, SVG, or pure CSS animations only.
8. **Surprise the user.** Don't repeat past builds. Draw from a wide range of ideas:
   - Data art (career timelines, geographic visualizations, network graphs)
   - Generative art (flow fields, particle systems, fractals, cellular automata)
   - Interactive toys (physics simulations, musical instruments, puzzle games)
   - Personal dashboards (quote engines, decision wheels, ambient mood boards)
   - Mini-games (space themed, word-based, strategy)
   - Visualizations of concepts the user cares about (education systems, TN geography, leadership models)

## If a theme hint is provided

Use it as a loose vibe guide, not a specification. Interpret it creatively. "Something with data" could become a particle simulation where each particle represents a student. "Make it weird" could become a non-Euclidean geometry explorer.

## After building

Give a brief, casual description of what you built and what the interactions are. Keep it short - let the thing speak for itself.
