# Dialogue Strategies

Interview strategies that apply throughout all three phases of the blueprinting process.

## Ask 1-2 Questions at a Time

Do not batch questions. Each message focuses on 1-2 key decisions. Users give higher-quality answers with focused single questions.

## Do Not Accept Vague Answers

When the user answers with "roughly", "whatever", "you decide", or "I guess so" — do not accept it:
- **User knows but hasn't articulated** → keep probing until specific
- **User genuinely doesn't know** → provide 2-3 options with trade-off analysis and a clear recommendation

## Approach Guidance

At key decision points (skill decomposition, platform selection, architecture choice, workflow design), propose 2-3 approaches:
- Approach name + one-sentence summary
- Pros / Cons
- Best-fit scenario
- Explicit recommendation + reasoning

## Challenge Over-Scoping

When the requested scope appears disproportionate to the stated problem, push back:
- Name the mismatch: "You described [simple problem], but the requested architecture implies [complex solution]."
- Propose a simpler alternative with reasoning.
- Only proceed with the complex approach if the user provides explicit justification.

Examples:
- User wants 5 platforms but only uses Claude Code → recommend starting with 1
- User wants subagents for a 2-skill project → challenge the need

## Immediate Contradiction Surfacing

Do not wait for Periodic Confirmation to detect contradictions. When a current answer conflicts with a previous answer, immediately:
1. Pause the current question
2. Name both statements and the contradiction
3. Resolve before continuing

Example: "In Phase 1 you said target users are beginners, but now you're requesting a complex workflow chain with subagent dispatch. These seem in tension — which is it?"

## Periodic Confirmation

After completing each phase, restate the collected information and confirm mutual understanding.

## Quick Mode Behavior Summary

| Phase | Quick Mode Behavior |
|-------|---------------------|
| Phase 1 | Ask only questions 1-2; skip 3-5 |
| Phase 2 | Skip steps 4a (Visibility), 5 (Workflow), 6 (Bootstrap), 7 (Advanced) |
| Phase 2 defaults | Claude Code only; skills treated as independent |
| Pipeline | Wire Workflow step simplified (no chains to wire) |
