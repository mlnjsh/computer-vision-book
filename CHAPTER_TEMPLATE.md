# Chapter Template

Every chapter follows this structure. Copy this when starting a new chapter.

## 1. Hook (≈ 200 words)
A concrete real-world problem or surprising result that motivates the chapter.

## 2. Mental Model (≈ 300 words)
The picture the reader should hold in their head before any code.

## 3. Theory You Need to Debug (≈ 600 words)
Just enough math/intuition to reason about failures. Skip rigorous derivations
unless they're load-bearing for understanding the model.

## 4. Code Walkthrough (≈ 1,200 words)
Working code, explained block by block. Notebook is the source of truth — prose
references cells from the notebook in `notebooks/chXX_*.ipynb`.

## 5. Production Note (≈ 300 words)
What changes when this leaves a notebook. Latency, memory, failure modes,
monitoring, common bugs in deployment.

## 6. Exercises (3-5)
- Stretch: extend the project to a new domain
- Diagnostic: break the model in a specific way and explain why
- Synthesis: combine with a previous chapter's technique

## 7. References & Further Reading
- 5-10 canonical papers
- 2-3 blog posts / videos (LearnOpenCV, Stanford CS231n, Two Minute Papers)
- 1-2 GitHub repos to clone and read
