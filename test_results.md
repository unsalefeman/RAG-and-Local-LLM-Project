# Test Results

## Source document
Tests below were run against *Thomas' Calculus* (Pearson), used locally for educational/testing purposes only. The file itself is not distributed with this repository, see README for details.

## Test 1: Out-of-context question
**Query:** "Who is the president of united states of america?"
**Result:** "According to the context provided, there is no specific information about the current president of the United States of America. To answer this question accurately, one would need additional information beyond the given context."
✅ Correctly declined, stated the context does not contain this information, did not fabricate an answer.

## Test 2: In-context conceptual question
**Query:** "Can you explain the purpose of fourier series?"
**Result:** "Fourier series are used to represent periodic functions as the sum of simpler sinusoidal functions, specifically sines and cosines. The purpose of Fourier series is to break down complex, periodic waveforms into these simpler components, making it easier to analyze, understand, and synthesize the original signal. This is particularly useful in fields such as signal processing, acoustics, and heat transfer, where periodic phenomena are common.
In essence, any periodic function can be approximated by a Fourier series, which consists of a constant term (the DC component), sine terms, and cosine terms, each with their own amplitude and phase. The coefficients of these terms are determined by the original function's behavior at various points in its cycle. By studying these coefficients, one can gain insights into the frequency spectrum of the signal, which is essential for tasks like filtering, compression, and noise reduction.
Fourier series also facilitate the solving of partial differential equations in physics, where they can be used to separate variables and simplify the equations into ordinary differential equations that are easier to solve.
In summary, Fourier series serve as a powerful tool for decomposing complex periodic signals into their constituent frequencies, thereby enabling a deeper understanding and manipulation of these signals in various scientific and engineering applications."
✅ Correct and well-grounded answer, directly referencing the theorem found in context.

## Test 3: Out-of-context simple arithmetic
**Query:** "What is the derivative of f(x) = (2x^13 + 89)(12x^2 - 41) ?"
**Result:** "To find the derivative of the function f(x) = (2x^13 + 89)(12x^2 - 41), we will use the product rule, which states that the derivative of two multiplied functions is the derivative of the first function times the second function plus the first function times the derivative of the second function.
Let u = (2x^13 + 89) and v = (12x^2 - 41).
First, we find the derivatives of u and v:
u' = d(2x^13)/dx = 26x^12
v' = d(12x^2)/dx = 24x
Now, apply the product rule:
f'(x) = u'v + uv'
f'(x) = (26x^12)(12x^2 - 41) + (2x^13 + 89)(24x)
Expand and simplify:
f'(x) = 312x^14 - 1066x^12 + 24x(2x^13) + 2184x
f'(x) = 312x^14 - 1066x^12 + 48x^14 + 2184x
f'(x) = 360x^14 - 1066x^12 + 2184x
Thus, the derivative of f(x) is f'(x) = 360x^14 - 1066x^12 + 2184x."
❌ Incorrect. The model correctly identified and applied the product rule structure, but made an arithmetic error in the final simplification: it computed (2x^13 + 89)(24x) as 48x^14 + 2184x, when the correct expansion is 48x^14 + 2136x (89 × 24 = 2136, not 2184). This demonstrates that while the model can reproduce the correct method for out-of-context computations, it is not reliable for the underlying arithmetic errors that can appear in a fully confident, well-formatted response with no indication of uncertainty.
## Summary
The evaluation demonstrates that the system correctly abstains from hallucinations when context is completely missing for out-of-domain queries (Test 1) and delivers accurate, fully grounded responses when relevant material is retrieved (Test 2). A key limitation was identified in Test 3: for computational tasks not covered by the retrieved context, the model does not decline the prompt but instead relies on its own training-derived knowledge to attempt a solution. In this case, the model reproduced the correct method (product rule) but made a silent arithmetic error in the final answer, presenting it with the same confidence as a correct result. This shows that correctness on out-of-context computation is not guaranteed, and errors are not signaled to the user, which is a risk for any application relying on this system for numerical accuracy.
