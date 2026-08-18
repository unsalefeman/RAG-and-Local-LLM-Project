# Test Results

## Test 1: Out-of-context question
**Query:** "who is the president of united states of america"
**Result:** ✅ Correctly declined — stated the context does not contain this information, did not fabricate an answer.

## Test 2: In-context conceptual question
**Query:** "can you explain the purpose of fourier series?"
**Result:** ⚠️ Answered using retrieved context, but content appeared to describe Taylor series rather than Fourier series — likely a retrieval mismatch (top-k chunks didn't include true Fourier content), not a model hallucination.

## Test 3: Out-of-context simple arithmetic
**Query:** "can you confirm that 10+10 = 1000?"
**Result:** ⚠️ Model correctly computed 10+10=20 and flagged the false claim, but used outside knowledge (basic arithmetic) rather than strictly relying on context — a known limitation of the current system prompt.

## Test 4: In-context mathematical property question
**Query:** "what can you say about the derivative and integral function of natural number e?"
**Result:** ✅ Correct and well-grounded answer, directly referencing the theorem found in context (d/dx eˣ = eˣ, ∫eˣ dx = eˣ + C).

## Summary
The system correctly avoids fabricating answers when context is missing (Test 1) and gives accurate, context-grounded answers when relevant material is retrieved (Test 4). Two limitations were observed: (1) retrieval sometimes returns semantically similar but topically distinct content (Test 2), and (2) the model occasionally falls back on its own general knowledge for simple reasoning tasks despite instructions to rely only on context (Test 3).
