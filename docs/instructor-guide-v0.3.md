# Instructor notes — Lab 03

Ask learners first whether every schema change should fail a pipeline. The answer is **no**: compatibility depends on a defined consumer contract. Walk through the four datasets, then have learners categorize each finding as schema, identity, required-value, referential, or type integrity.

Assessment (10 points): distinguishes additive from breaking evolution (2); identifies all five integrity findings (3); states why missing headers block downstream checks (1); describes downstream business risk (2); makes evidence-based hold/retest recommendation (2).

Avoid overstating coverage: v0.3 does not perform full CSV syntax or cross-batch integrity checking. Emphasize the distinction between a passing quality **gate** and universal proof of correctness.
