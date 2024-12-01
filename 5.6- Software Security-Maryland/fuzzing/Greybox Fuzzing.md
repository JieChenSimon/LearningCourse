In the previous chapter, we have introduced **mutation-based fuzzing**, a technique that **generates fuzz inputs by applying small mutations to given input**s. In this chapter, we show **how to guide these mutations towards specific goals such as coverage.** The algorithms in this chapter stem from the popular American Fuzzy Lop (AFL) fuzzer, in particular from its AFLFast and AFLGo flavors. We will explore the greybox fuzzing algorithm behind AFL and how we can exploit it to solve various problems for automated vulnerability detection.

本章介绍如何通过特定目标(如覆盖率)来引导基于变异的模糊测试（mutation-based fuzzing）生成测试输入。

灰盒测试通过参数化模糊测试的多个方面，使基于变异的模糊测试更加系统化。 灰盒测试通过参数化模糊测试的多个方面，使基于变异的模糊测试更加系统化。
（灰盒测试通过参数化模糊测试的多个方面，使基于变异的模糊测试更加系统化。 allowing us to actually parameterize many aspects of the fuzzer，变得更加系统和详细）