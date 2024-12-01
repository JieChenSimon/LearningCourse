---
source: https://www.fuzzingbook.org/slides/MutationFuzzer.slides.html#/3
---



**Most randomly generated inputs are syntactically _invalid_ and thus are quickly rejected by the processing program.** To exercise functionality beyond input processing, we must increase chances to obtain valid inputs. One such way is so-called _mutational fuzzing_ – that is, introducing small changes to **existing inputs** that may still keep the input valid, yet exercise new behavior. We show how to create such mutations, and how to guide them towards yet uncovered code, applying central concepts from the popular AFL fuzzer.


### Mutating Inputs

The alternative to generating random strings from scratch is to **start with a given _valid_ input**, and then to subsequently _mutate_ it. A _mutation_ in this context is a simple string manipulation - say, inserting a (random) character, deleting a character, or flipping a bit in a character representation. This is called _mutational fuzzing_ – in contrast to the _generational fuzzing_ techniques discussed earlier.



### 实际例子--Mutating URLs



### Guiding by Coverage