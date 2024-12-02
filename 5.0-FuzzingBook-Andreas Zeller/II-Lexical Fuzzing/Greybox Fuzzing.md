In the previous chapter, we have introduced **mutation-based fuzzing**, a technique that **generates fuzz inputs by applying small mutations to given input**s. In this chapter, we show **how to guide these mutations towards specific goals such as coverage.** The algorithms in this chapter stem from the popular American Fuzzy Lop (AFL) fuzzer, in particular from its AFLFast and AFLGo flavors. We will explore the greybox fuzzing algorithm behind AFL and how we can exploit it to solve various problems for automated vulnerability detection.

this chapter is in this chapter pretty much builds on the insights that we had already from the last chapter namely we are getting coverage we are evolving a population of inputs towards a target but this time we are doing this in a more elaborated fashion by making our fuzzers more parameterized in the sense that we can come up with various algorithms we can come up with various ways to direct our fuzzing towards specific locations and more.


本章介绍如何通过特定目标(如覆盖率)来引导基于变异的模糊测试（mutation-based fuzzing）生成测试输入。

灰盒测试通过参数化模糊测试的多个方面，使基于变异的模糊测试更加系统化。 灰盒测试通过参数化模糊测试的多个方面，使基于变异的模糊测试更加系统化。

----------------------------------------------------------------
灰盒测试通过参数化模糊测试的多个方面，使基于变异的模糊测试更加系统化。 allowing us to actually parameterize many aspects of the fuzzer，变得更加系统和详细）

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

### AFL 

AFL is a mutation-based fuzzer. Meaning, AFL generates new inputs by slightly modifying a seed input (i.e., mutation), or by joining the first half of one input with the second half of another (i.e., splicing). 

AFL is **also a greybox fuzzer** (not blackbox nor whitebox). Meaning, AFL leverages coverage-feedback to learn how to reach deeper into the program. It is not entirely blackbox because AFL leverages at least some program analysis. It is not entirely whitebox either because AFL does not build on heavyweight program analysis or constraint solving. Instead, AFL uses lightweight program instrumentation to glean some information about the (branch) coverage of a generated input. If a generated input increases coverage, it is added to the seed corpus for further fuzzing.


To instrument a program, AFL injects a piece of code right after every conditional jump instruction. When executed, this so-celled trampoline assigns the exercised branch a unique identifier and increments a counter. that is associater with this branch. For efficiency, only a coarse branch hit count is maintained. In other wards, for each input the fuzzer knows which branches and roughly how often they are exercised. The instrumentation is usually done at compile-time, i.e., when the program source code is compiled te an executable binary. However, it is possible to run AFL on uninstrumented binaries using tools such as a virtual machine (e.g.
GEMU) or a dynamic instrumentation tool (e.g, Intel PinTool). For Python programs, we can collect coverage information without any instrumentation.

AFL是一个基于变异的模糊测试器。它通过轻微修改种子输入（即变异），或者将一个输入的前半部分与另一个输入的后半部分拼接（即拼接）来生成新的输入。AFL也是一个灰盒模糊测试器（既不是黑盒也不是白盒）。

这意味着AFL利用覆盖率反馈来学习如何深入程序。它不完全是黑盒测试因为AFL至少利用了一些程序分析；也不完全是白盒测试因为AFL不依赖重量级程序分析或约束求解。相反，AFL使用轻量级程序插桩来获取生成输入的（分支）覆盖信息。如果生成的输入增加了覆盖率，它就会被添加到种子语料库中用于进一步测试。

为了插桩程序，AFL在每个条件跳转指令后注入一段代码。执行时，这个所谓的trampoline会为执行的分支分配唯一标识符并增加与该分支相关的计数器。为了效率，只维护粗略的分支命中计数。换句话说，对于每个输入，模糊测试器知道哪些分支被执行以及大致的执行频率。插桩通常在编译时完成，即当程序源代码被编译成可执行二进制文件时。然而，通过使用虚拟机（如QEMU）或动态插桩工具（如Intel PinTool），也可以在未插桩的二进制文件上运行AFL。对于Python程序，我们可以在不需要任何插桩的情况下收集覆盖率信息。

---------------
Note：
<span style="background:#fff88f">trampoline（蹦床）</span>在AFL中指的是一段被注入的短小监控代码。它的作用是：

1. 记录分支执行情况
2. 分配分支ID
3. 更新执行计数

之所以叫"蹦床"，是因为这段代码执行完后会立即跳回到原程序继续执行，类似于在蹦床上短暂跳起后落回原处的动作。


### Power Schedules

Now we introduce a new concept: **the power schedule**. A power schedule distributes the precious fuzzing time among the seeds in the population, meaning that in a population of many inputs, it determines which inputs should receive the highest amount of fuzzing energy and have the greatest chance to evolve and mutate to produce more offspring.

现在我们介绍一个新概念：能量调度。**能量调度负责在种子群中分配宝贵的模糊测试时间，这意味着在包含多个输入的种子群中**，<u>它决定哪些输入应该获得最多的模糊测试能量，并有最大的机会进行演化和变异以产生更多的后代。</u>

This concept of power scheduling is extremely important for fuzzing because it defines how efficient a fuzzer will be. The more efficiently a fuzzer distributes its time toward reaching its goals, the higher its chances of actually achieving those goals. To accomplish this, we assign energy values to individual seeds in our population.

能量调度这个概念对模糊测试极其重要，因为它决定了模糊器的效率。模糊器越能高效地分配时间来达成目标，就越有可能真正实现这些目标。为了实现这一点，我们给种子群中的每个种子都分配能量值。

Our objective is to **maximize the time spent fuzzing those (most progressive) seeds which lead to higher coverage increase in shorter time.** <u>We call the likelihood with which a seed is chosen from the population as the seed's energy.</u> Throughout a fuzzing campaign, we would like to prioritize seeds that are more promising. Simply said, we do not want to waste energy fuzzing non-progressive seeds. We call the procedure that decides a seed's energy as the fuzzer's power schedule. For instance, AFL's schedule assigns more energy to seeds that are shorter, that execute faster, and yield coverage increases more often.

我们的目标是最大化将时间用在那些（最具进展性的）种子上，这些种子能在更短时间内带来更高的覆盖率提升。**我们将种子从种子群中被选中的可能性称为该种子的能量**。在整个模糊测试过程中，我们希望优先选择那些更有希望的种子。简单来说，我们不想把能量浪费在没有进展的种子上。我们将决定种子能量的过程称为模糊器的能量调度。例如，AFL的调度会给更多能量给那些更短、执行更快以及更频繁产生覆盖率提升的种子。


```python
from fuzzingbook.GreyboxFuzzer import GreyboxFuzzer, FunctionCoverageRunner, Mutator, PowerSchedule, http_program
# 1. 设置初始种子输入
seed_input = "http://www.google.com/search?q=fuzzing"
seeds = [seed_input]
# 2. 使用库中定义好的类
mutator = Mutator()
schedule = PowerSchedule()
# 3. 初始化灰盒模糊测试器
greybox_fuzzer = GreyboxFuzzer(seeds=seeds, mutator=mutator, schedule=schedule)
# 4. 使用库中的示例HTTP程序
http_runner = FunctionCoverageRunner(http_program)
# 5. 运行模糊测试
outcomes = greybox_fuzzer.runs(http_runner, trials=10000)
# 6. 查看结果
print("Fuzzing completed!")
print(f"Number of tests executed: {len(outcomes)}")
print(f"Final population size: {len(greybox_fuzzer.population)}")
```


**除了简单的 `PowerSchedule`，我们还可以使用一些高级的能量调度：**

* `AFLFastSchedule` 为不经常执行的"不寻常"路径分配高能量。
* `AFLGoSchedule` 为接近未覆盖程序位置的路径分配高能量。
`AFLGoSchedule` 类的构造函数需要一个从每个节点到目标位置的 `distance` 度量，这个度量是通过分析程序代码来确定的。详细信息请参阅本章内容。


### AFL灰盒模糊测试详解

#### 1. 高级能量调度方案（Power Schedule）

####  概念解释
能量调度是指如何分配有限的模糊测试时间到不同的测试用例（种子）上。就像在有限的时间内复习考试，我们会优先复习重点章节一样，模糊测试也需要决定把时间花在哪些测试用例上。

####  三种调度方案详解
1. **基础调度 (PowerSchedule)**
```python
class PowerSchedule:
    def assignEnergy(self, population: Sequence[Seed]) -> None:
        """基础版本：所有种子获得相同的能量值"""
        for seed in population:
            seed.energy = 1
```
简单但效率可能不高，因为它对待所有测试用例都一视同仁。

2. **AFLFastSchedule**
- 为什么需要：某些程序路径很少被执行到，这些路径可能隐藏着bug
- 工作原理：对较少执行的路径给予更多测试时间
- 类比：就像在复习时，对不太熟悉的知识点多花时间

3. **AFLGoSchedule**
- 特点：考虑代码位置的"距离"概念
- 原理：优先测试那些接近未覆盖代码的测试用例
- 类比：像玩游戏时会优先探索离当前位置近的未知区域

#### 2. 变异策略（Mutation）

####  概念解释
变异是指通过修改现有的测试用例来生成新的测试用例，就像生物进化中的DNA变异。

####  具体实现
```python
class Mutator:
    def __init__(self):
        """初始化三种基本变异操作"""
        self.mutators = [
            self.delete_random_character,  # 随机删除一个字符
            self.insert_random_character,  # 随机插入一个字符
            self.flip_random_character     # 随机改变一个字符
        ]
    
    def insert_random_character(self, s: str) -> str:
        """插入操作：在随机位置插入随机字符"""
        pos = random.randint(0, len(s))
        random_character = chr(random.randrange(32, 127))
        return s[:pos] + random_character + s[pos:]
```

####  为什么需要变异？
- 自动生成新的测试用例
- 探索程序的不同执行路径
- 可能触发未发现的bug

#### 3. 种子管理（Seed）

####  概念解释
种子是模糊测试的基础测试用例，就像农作物的种子一样，它们会经过变异产生新的测试用例。

####  实现细节
```python
class Seed:
    def __init__(self, data: str) -> None:
        self.data = data          # 实际的测试数据
        self.coverage = set()     # 记录这个种子触发了哪些代码路径
        self.distance = -1        # 到目标代码的距离
        self.energy = 0.0         # 被选中进行变异的概率
```

####  种子的重要属性
- **coverage**：记录代码覆盖情况
- **distance**：评估到目标的距离
- **energy**：决定被选中的机会

####  4. 覆盖率收集（Coverage）

####  概念解释
覆盖率是指程序中被测试执行到的代码比例。就像检查试卷，我们要知道哪些知识点已经复习到了。

####  示例实现
```python
def crashme(s: str) -> None:
    """一个简单的示例程序，展示如何收集覆盖率"""
    if len(s) > 0 and s[0] == 'b':    # 路径1
        if len(s) > 1 and s[1] == 'a': # 路径2
            if len(s) > 2 and s[2] == 'd': # 路径3
                if len(s) > 3 and s[3] == '!': # 路径4
                    raise Exception()
```

####  覆盖率收集的重要性
1. 指导测试方向
2. 评估测试效果
3. 帮助发现未测试区域

#### 5. 实践应用

#### 完整的测试流程
```python
# 1. 设置初始配置
seed_input = "http://www.google.com/search?q=fuzzing"
seeds = [seed_input]
mutator = Mutator()
schedule = PowerSchedule()

# 2. 创建并运行模糊测试器
greybox_fuzzer = GreyboxFuzzer(seeds, mutator, schedule)
http_runner = FunctionCoverageRunner(HTTPExample.http_program)
outcomes = greybox_fuzzer.runs(http_runner, trials=10000)
```
