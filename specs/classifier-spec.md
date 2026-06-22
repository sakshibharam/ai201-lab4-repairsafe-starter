# Spec: `classify_safety_tier()`

**File:** `safety.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Determine whether a home repair question is safe to answer directly, requires a cautionary response, or should be refused with a referral to a licensed professional.

---

## Input / Output Contract

**Input:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `question` | `str` | The user's home repair question |

**Output:** `dict`

| Key | Type | Description |
|-----|------|-------------|
| `"tier"` | `str` | One of: `"safe"`, `"caution"`, `"refuse"` |
| `"reason"` | `str` | One sentence explaining why this tier was assigned |

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Tier definitions

*Write a one-sentence definition for each tier that is precise enough to use as part of your classification prompt. Vague definitions produce inconsistent classifications.*

**safe:**
```
Routine maintenance and low-risk cosmetic repairs that most homeowner can complete, worst case is cosmetic damage.
```

**caution:**
```
Repairs a motivated homeowner might attempt on an existing fixture or system at same location, where mistakes can cause meaningul cost, but no fire/flood/injury risk. Does not involve new wiring, new plumbing lines, gas work, structural changes, or work that normally requires permit or licensed professional.
```

**refuse:**
```
repairs that could cause fire, flooding, structural failure, serious injury, or death if done incorrectly, or that involve gas lines, electrical panels, new circuits, main water lines, load-bearing structures, or other work that should be handled by a licensed professional or permitted contractor.
```

---

### Classification approach

*How will the LLM classify the question? Will you give it just the tier definitions, or also examples (few-shot)? Will you ask it to reason step-by-step before naming the tier, or output the tier directly?*

*Consider: what happens when a question is genuinely ambiguous — e.g., "can I replace my own outlets?" Which tier should that land in, and how does your approach handle questions at the boundary?*

```
I will give the LLM the tier definitions and also some examples that stress the boundaries, then ask it to choose one tier directly and explain in one sentence. If the question is about replacing an existing component in place, that usually lands in caution; if it adds new wiring, plumbing, gas work, structural changes, or anything permit or license heavy, it lands in refuse. 
```

---

### Output format

*How will the LLM communicate the tier and reason back to you? Describe the exact text format you'll ask it to use, so you can parse it reliably.*

*The format you used in Lab 3 (`Label: X / Reasoning: Y`) is a reasonable starting point, but you're not required to use it. Whatever you choose, you'll need to parse it in code — so consider how much variation the LLM might introduce and how you'll handle that.*

```
The LLM returns exactly one JSON object with two keys: tier and reason.
```

---

### Prompt structure

*Write the actual prompt you'll use — both the system message and the user message. Don't describe it — write it. Vague prompt descriptions produce vague prompts, which produce inconsistent classifications.*

**System message:**
```
You are a safety classifier for home repair questions.

Classify each question into exactly one tier:

safe: Routine maintenance and low-risk cosmetic repairs that most homeowners can complete with basic tools and patience, with no realistic risk of injury, fire, flooding, or structural damage.

caution: Repairs a motivated homeowner might attempt on an existing fixture or system at the same location, where mistakes can cause meaningful cost or minor injury, but the task does not involve new wiring, new plumbing lines, gas work, structural changes, or work that normally requires a permit or licensed professional.

refuse: Repairs that could cause fire, flooding, structural failure, serious injury, or death if done incorrectly, or that involve gas lines, electrical panels, new circuits, main water lines, load-bearing structures, or other work that should be handled by a licensed professional or permitted contractor.

Apply this boundary carefully: if the task modifies hidden infrastructure or introduces a new electrical, plumbing, gas, or structural system, choose refuse; if it is a like-for-like replacement or minor repair on an existing fixture or component, choose caution.

Return exactly one JSON object with these keys:
tier: one of safe, caution, or refuse
reason: one short sentence explaining why that tier was chosen

Do not include markdown, code fences, extra keys, or extra text.
```

**User message:**
```
Classify this home repair question: {question}
```

---

### Caution/refuse boundary

*The most consequential classification decision is whether a question lands in "caution" or "refuse." Write down your rule for this boundary — one sentence. Then give two examples of questions that sit close to the line and explain which side they fall on and why.*

```
If the task modifies hidden infrastructure or introduces new electrical, plumbing, gas, or structural system, refuse; if it is a replacement or minor repair on an existing fixture or component, caution.

"replace an outlet": caution, it is a same-location replacement on an existing circuit

"add an outlet": refuse, requires new wiring and often a permit
```

---

### Fallback behavior

*What does your function return if the LLM response can't be parsed — e.g., if it produces free-form prose instead of your expected format? What happens when tier validation against `VALID_TIERS` fails?*

*Note: failing open (returning "safe" as a fallback) is more dangerous than failing closed (returning "caution"). Which makes more sense here, and why?*

```
The function returns a caution tier with a reason that it could not reliably parse or validate the model output.
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 2.*

**One classification that surprised you — question, tier you expected, tier it returned, and why:**

```
[your answer here]
```

**One prompt change you made after seeing the first few outputs, and what it fixed:**

```
[your answer here]
```
