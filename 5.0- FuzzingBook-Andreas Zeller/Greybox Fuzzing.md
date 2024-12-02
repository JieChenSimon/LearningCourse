In the previous chapter, we have introduced **mutation-based fuzzing**, a technique that **generates fuzz inputs by applying small mutations to given input**s. In this chapter, we show **how to guide these mutations towards specific goals such as coverage.** The algorithms in this chapter stem from the popular American Fuzzy Lop (AFL) fuzzer, in particular from its AFLFast and AFLGo flavors. We will explore the greybox fuzzing algorithm behind AFL and how we can exploit it to solve various problems for automated vulnerability detection.

本章介绍如何通过特定目标(如覆盖率)来引导基于变异的模糊测试（mutation-based fuzzing）生成测试输入。

灰盒测试通过参数化模糊测试的多个方面，使基于变异的模糊测试更加系统化。 灰盒测试通过参数化模糊测试的多个方面，使基于变异的模糊测试更加系统化。
（灰盒测试通过参数化模糊测试的多个方面，使基于变异的模糊测试更加系统化。 allowing us to actually parameterize many aspects of the fuzzer，变得更加系统和详细）
----------------------------------------------------------------
在模糊测试中，population of inputs 指的是当前维护的一组测试输入样本集合。这些输入会被用来生成新的测试用例，通常通过变异（mutation）或交叉（crossover）等操作来产生。

---------------------------------------------------------------
### What does graybox fuzzing mean
A: we distinguish several perspectives on a program depending on how much information we have. 

1. We do have white box fuzzing, which means we have the source code. We can execute the program and retrieve all the information we want at will, for instance, by instrumenting it or altering the source code. Everything is laid bare to us - we can fully look into our program at hand. <u>**this is actually the perspective you typically have when you're building the software yourself**</u>
2. We have black box fuzzing: black box fuzzing means we're treating the program as a black box, out of which we have little to no information at all, except maybe for the fact that it occasionally passes or fails a test. In black box fuzzing, you have no knowledge about the program code, or practically no knowledge, and you also have no capabilities to modify the program code, so you cannot inject things or change it at will. If you do black box fuzzing or generally black box testing, what you have to work with is a **specification of the input language and possibly a specification of what makes correct behavior.** Without such specifications, there is no sense in testing a black box because you need to generate inputs and you need to be able to interpret its results.
3. Now between white box fuzzing (where you have everything) and black box fuzzing (where you have nothing), there is gray box fuzzing. **Gray box fuzzing means you don't have all the information as in white box fuzzing, but you also don't have no information at all. Instead, you have limited information - what "limited" means in this context is somewhat open to interpretation. One of these limited pieces of information that can be examined is notably information that is easy to gain and obtain, meaning it requires little effort and there are generic techniques for retrieving it.** The typical information we use in fuzzing is coverage, specifically which parts of the program have been executed. Coverage is easy to get from almost every programming language because they all have built-in support for measuring it. Why? Because measuring coverage is essential for assessing testing quality - if your tests have 10% coverage, it means 90% of your code isn't even executed during testing. This means your test needs significant improvement since it can only find bugs in the parts it actually executes. Therefore, almost every programming language and environment has means to gather coverage data from runs, and since coverage is ubiquitous, this is what's used in gray box fuzzing.

1. 白盒模糊测试指我们拥有源代码，可以执行程序并获取所需的所有信息。例如，通过修改源代码进行插桩，我们可以完全了解程序的内部工作。这通常是开发者自己构建软件时的视角。

2. 黑盒模糊测试是将程序作为黑盒处理，几乎没有任何内部信息，只能知道测试是通过还是失败。在黑盒测试中，你对程序代码几乎一无所知，也无法注入或随意更改代码。进行黑盒测试时，你只能依靠输入语言规范和正确行为的规范来工作。如果没有这些规范，测试黑盒就毫无意义，因为你既需要生成输入，又需要能够解释测试结果。
3. 介于白盒模糊测试（可获取所有信息）和黑盒模糊测试（几乎无信息）之间的是灰盒模糊测试。灰盒测试能获取有限的信息，这里的"有限"定义比较灵活。通常我们会获取那些容易得到且有通用获取技术的信息，典型的就是程序覆盖率信息 - 即程序的哪些部分被执行了。几乎所有编程语言都支持覆盖率测量，因为这对评估测试质量至关重要 - 如果测试覆盖率只有10%，意味着90%的代码未被执行测试，这表明测试需要大幅改进，因为只有被执行的代码中的bug才可能被发现。正因为几乎所有编程环境都提供了收集运行时覆盖率的方法，且覆盖率数据普遍可得，它成为了灰盒模糊测试中的关键信息。

--------------------------------------------------------------------