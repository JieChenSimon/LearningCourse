你说得对,我来逐段详细翻译这篇关于Search-Based Fuzzing的内容。

# Search-Based Fuzzing(基于搜索的模糊测试)

有时我们不仅对生成尽可能多样化的程序输入感兴趣,还想要获得能实现某些特定目标的测试输入,比如达到程序中的特定语句。当我们明确知道要寻找什么时,就可以进行有针对性的搜索(search)。搜索算法是计算机科学的核心,但直接应用经典的搜索算法(如广度优先或深度优先搜索)来搜索测试用例是不现实的,因为这些算法可能需要检查所有可能的输入。然而,通过领域知识可以克服这个问题。例如,如果我们能估计哪些程序输入更接近我们要找的目标,这些信息就能帮助我们更快地达到目标 - 这种信息被称为启发式(heuristic)。启发式被系统化应用的方式被称为元启发式(meta-heuristic)搜索算法。"元"表示这些算法是通用的,可以针对不同问题进行特化。元启发式算法通常从自然过程中获取灵感。例如,有些算法模仿进化过程、群体智能或化学反应。总的来说,它们比穷举搜索方法效率高得多,可以应用于广阔的搜索空间 - 像程序输入这样庞大的搜索空间对它们来说也不是问题。

## 先决条件

* 你应该了解代码覆盖率是如何工作的,例如从[覆盖率章节](Coverage.ipynb)中学习。

## 将测试生成作为搜索问题 

如果我们想要将元启发式搜索算法应用于程序测试数据生成,我们需要做出几个选择:首先,我们需要确定我们的搜索空间(search space)究竟是什么。搜索空间由我们如何表示(represent)我们要寻找的东西来定义。我们是在寻找单个整数值吗?值的元组?对象?XML文档?

### 将程序输入表示为搜索问题

表示方式高度依赖于我们要解决的具体测试问题 - 我们知道我们正在测试哪个程序,所以表示需要编码我们目标程序的任何输入是什么。让我们以`test_me()`函数作为我们要测试的函数示例:

```python
def test_me(x, y):
    if x == 2 * (y + 1):
        return True
    else:
        return False
```

`test_me()`函数有两个输入参数,根据它们之间的关系返回`True`或`False`。对`test_me()`的测试输入由一对值组成,一个用于`x`,一个用于`y`。例如:

```python
test_me(0, 0)  # 返回False
test_me(4, 2)  # 返回False 
test_me(22, 10)  # 返回True
```

我们的搜索空间只关注输入,因此测试数据的一个简单表示就是输入元组`(x, y)`。这个输入空间中的每个点都有八个邻居:

- `x-1, y-1`
- `x-1, y` 
- `x-1, y+1`
- `x, y+1`
- `x+1, y+1`  
- `x+1, y`
- `x+1, y-1`
- `x, y-1`

为了简单起见,让我们先限制下搜索空间的大小(稍后我们会修改这个)。例如,我们假设值的范围只在-1000到1000之间:

```python
MAX = 1000
MIN = -MAX
```

要获取搜索空间中任何点的邻居,我们定义`neighbors()`函数,它实现了一个基本的Moore邻域。也就是说,我们查看所有8个直接邻居,同时考虑我们用`MAX`和`MIN`定义的边界:

```python
def neighbors(x, y):
    return [(x + dx, y + dy) for dx in [-1, 0, 1]
            for dy in [-1, 0, 1]
            if (dx != 0 or dy != 0)
            and ((MIN <= x + dx <= MAX)
                 and (MIN <= y + dy <= MAX))]
```

用法示例:
```python
print(neighbors(10, 10))
```

这完全定义了我们的搜索空间:我们有一个表示方法,而且我们知道通过它们的邻域关系,个体之间是如何关联的。现在我们只需要找到一个算法来探索这个邻域,以及一个指导算法的启发式方法。

### 定义搜索景观:适应度函数

所有元启发式算法都基于使用启发式函数来估计给定候选解的好坏程度;这种"好坏程度"通常被称为个体的适应度(fitness),估计适应度的启发式被称为适应度函数(fitness function)。适应度函数是一个将搜索空间中的任何点映射到数值的函数,这个数值就是适应度值。搜索空间中的候选解越接近最优解,其适应度值就越好。因此,如果你将搜索空间中每个点的适应度值作为高度来绘图,你就会得到一个景观,其中最优解表现为最高峰。

好的,我继续翻译:

适应度函数取决于我们想要通过生成测试数据达到的目标。假设我们对覆盖`test_me()`函数中if条件的真分支感兴趣,即`x == 2 * (y + 1)`。

一个给定的输入元组离达到目标分支有多近呢?让我们考虑搜索空间中的一个任意点,例如`(274, 153)`。if条件比较以下值:

```python
x = 274
y = 153
x, 2 * (y + 1)  # 输出: (274, 308)
```

为了使分支为真,这两个值需要相等。因此,它们的差异越大,我们离使比较为真就越远;它们的差异越小,我们就越接近使比较为真。因此,我们可以通过计算`x`和`2 * (y + 1)`之间的差值来量化这个比较"有多假"。这样,我们可以将这个距离计算为`abs(x - 2 * (y + 1))`:

```python
def calculate_distance(x, y):
    return abs(x - 2 * (y + 1))

calculate_distance(274, 153)  # 输出距离值
```

我们可以将这个距离值作为我们的适应度函数,因为它能很好地衡量我们离最优解有多近。需要注意的是,"更好"在这里并不意味着"更大";距离越小越好。这不是问题,因为任何可以最大化值的算法也可以修改为最小化它。

对于搜索空间中的每个整数元组,这个距离值定义了我们搜索景观中的高度。由于我们的示例搜索空间是二维的,搜索景观是三维的,我们可以绘制它来看看它的样子:

```python
import matplotlib.pyplot as plt
import numpy as np

%matplotlib inline

xx = np.outer(np.linspace(-10, 10, 30), np.ones(30))
yy = xx.copy().T
zz = calculate_distance(xx, yy)

fig = plt.figure()
ax = plt.axes(projection='3d')

ax.plot_surface(xx, yy, zz, cmap=plt.cm.jet, rstride=1, cstride=1, linewidth=0);
```

最优值,即那些使if条件为真的值,其适应度值为0,可以在图的底部清楚地看到。离最优值越远,搜索空间中的点就越高。

### 插装(Instrumentation)

适应度函数应该为具体的测试执行计算距离值。也就是说,我们想要运行程序,然后了解这次执行的距离值。然而,分支条件隐藏在目标函数的源代码中,其值原则上可能是沿着到达它的执行路径的各种计算的结果。虽然在我们的例子中,条件是直接使用函数的输入值的等式,但一般情况下可能不是这样;它也可能是派生值。因此,我们需要计算距离度量所需的值需要直接在条件语句处观察到。

这通常通过插装来完成:我们在分支条件的前面或后面添加新的代码,以跟踪观察到的值并使用这些值计算距离。以下是我们测试程序的一个插装版本,它在执行时打印出距离值:

```python
def test_me_instrumented(x, y):
    print("Instrumentation: Input = (%d, %d), distance = %d" %
          (x, y, calculate_distance(x, y)))
    if x == 2 * (y + 1):
        return True
    else:  
        return False
```

让我们用几个示例值来试试这个:

```python
test_me_instrumented(0, 0)
test_me_instrumented(5, 2)
test_me_instrumented(22, 10)
```

好的,我继续翻译:

当计算适应度值时,我们会执行插装程序版本,但我们需要一些方法来访问在执行期间计算出的距离值。作为解决这个问题的一个简单的初步方案,我们可以添加一个全局变量并将距离计算的值存储在那里。

```python
distance = 0

def test_me_instrumented(x, y):  # type: ignore
    global distance
    distance = calculate_distance(x, y)
    if x == 2 * (y + 1):
        return True
    else:
        return False
```

使用这个`test_me()`的插装版本,我们现在终于可以定义我们的适应度函数了,它只需运行插装的`test_me_instrumented()`函数,然后获取全局`distance`变量的值:

```python
def get_fitness(x, y):
    global distance
    test_me_instrumented(x, y)
    fitness = distance
    return fitness
```

让我们在一些示例输入上试试这个:

```python
get_fitness(0, 0)
get_fitness(1, 2)
get_fitness(22, 10)
```

### 爬山示例(Hillclimbing the Example)

在确定了表示方法(整数2元组)和适应度函数(到目标分支的距离)后,我们现在终于可以实现我们的搜索算法了。让我们用最简单可能的元启发式算法来探索这个搜索空间:爬山算法(Hillclimbing)。这个比喻很好地描述了发生的事情:算法试图在由我们的表示定义的搜索空间中爬山。不过,在我们的搜索景观中,最好的值不是那些高处的值而是低处的值,所以技术上说我们是在下降到谷底。

爬山算法本身非常简单:
1. 选取一个随机起点
2. 确定所有邻居的适应度值
3. 移动到适应度值最好的邻居
4. 如果没有找到解,继续步骤2

爬山算法从一个随机测试输入开始,即`x`和`y`的随机值。对于任何一对随机整数,它们满足条件`x == 2 * (y + 1)`的机会是相当小的。假设随机值是`(274, 153)`。等式的右边,`2 * (y + 1)`,计算结果为308,所以条件显然是假的。爬山算法现在应该往哪里走?让我们看看这个测试输入及其邻居的适应度值:

```python
x, y = 274, 153
print("Origin %d, %d has fitness %d" % (x, y, get_fitness(x, y)))
for nx, ny in neighbors(x, y):
    print("neighbor %d, %d has fitness %d" % (nx, ny, get_fitness(nx, ny)))
```

将`y`增加1会使等式右边的值增加到`310`。因此,等式左边的值与右边的值相比比之前差得更多!所以,增加`y`似乎不是一个好主意。另一方面,增加`x`改善了情况:等式的左边和右边变得更相似;它们"不那么不相等"了。因此,在`(274, 153)`的八个可能邻居中,增加`x`并减少`y`的邻居(`(275, 152)`)似乎是最好的 - 条件的结果仍然是假,但它比原始值"不那么假"。

让我们现在实现爬山算法:

好的,我继续翻译:

```python
import random

LOG_VALUES = 20  # 记录的值的数量

def hillclimber():
    # 创建并评估起始点
    x, y = random.randint(MIN, MAX), random.randint(MIN, MAX)
    fitness = get_fitness(x, y)
    print("Initial value: %d, %d at fitness %.4f" % (x, y, fitness))
    iterations = 0
    logs = 0

    # 一旦找到最优解就停止
    while fitness > 0:
        iterations += 1
        # 移动到第一个具有更好适应度的邻居
        for (nextx, nexty) in neighbors(x, y):
            new_fitness = get_fitness(nextx, nexty)

            # 较小的适应度值更好
            if new_fitness < fitness:
                x, y = nextx, nexty
                fitness = new_fitness
                if logs < LOG_VALUES:
                    print("New value: %d, %d at fitness %.4f" % (x, y, fitness))
                elif logs == LOG_VALUES:
                    print("...")
                logs += 1
                break

    print("Found optimum after %d iterations at %d, %d" % (iterations, x, y))
```

爬山算法首先为`x`和`y`选择随机值。我们使用`-1000`--`1000`范围内的较低值(这是我们之前用`MIN`和`MAX`定义的)来减少在使用示例时搜索所需的时间。然后,我们通过调用`get_fitness()`来确定这个起始点的适应度值。回想一下,我们试图找到最小可能的适应度值,因此我们现在循环直到找到适应度值为`0`(即最优值)。

在这个循环中,我们遍历所有邻居(`neighbors`),并评估每个邻居的适应度值。一旦我们找到一个具有更好(更小)适应度的邻居,爬山算法就退出循环并使用这个作为新的起始点。这个简单爬山算法的一个变体是移除`break`语句:通过这样做,所有邻居都会被评估,选择最好的邻居。这被称为最陡上升爬山(steepest ascent hillclimbing)。你会发现达到最优所需的迭代次数更少,尽管每次迭代执行的测试更多。

```python
def steepest_ascent_hillclimber():
    # 创建并评估起始点
    x, y = random.randint(MIN, MAX), random.randint(MIN, MAX)
    fitness = get_fitness(x, y)
    print("Initial value: %d, %d at fitness %.4f" % (x, y, fitness))
    iterations = 0
    logs = 0

    # 一旦找到最优解就停止
    while fitness > 0:
        iterations += 1
        # 移动到具有最好适应度的邻居
        for (nextx, nexty) in neighbors(x, y):
            new_fitness = get_fitness(nextx, nexty)
            if new_fitness < fitness:
                x, y = nextx, nexty
                fitness = new_fitness
                if logs < LOG_VALUES:
                    print("New value: %d, %d at fitness %.4f" % (x, y, fitness))
                elif logs == LOG_VALUES:
                    print("...")
                logs += 1

    print("Found optimum after %d iterations at %d, %d" % (iterations, x, y))
```

我们的示例程序有一个非常好的适应度景观 – 有一个完美的梯度,爬山算法总能找到解。我们可以通过绘制随时间观察到的适应度值来看到这个很好的梯度:

```python
def plotting_hillclimber(fitness_function):
    data = []

    # 创建并评估起始点
    x, y = random.randint(MIN, MAX), random.randint(MIN, MAX)
    fitness = fitness_function(x, y)
    data += [fitness]
    iterations = 0

    # 一旦找到最优解就停止
    while fitness > 0:
        iterations += 1
        # 移动到第一个具有更好适应度的邻居
        for (nextx, nexty) in neighbors(x, y):
            new_fitness = fitness_function(nextx, nexty)
            if new_fitness < fitness:
                x, y = nextx, nexty
                fitness = new_fitness
                data += [fitness]
                break

    print("Found optimum after %d iterations at %d, %d" % (iterations, x, y))
    return data
```

[需要我继续翻译后面的内容吗?]