1. Fuzzing (fuzz testing) 101: Lessons from cyber security expert Dr. David Brumley https://www.youtube.com/watch?v=17ebHty54T4
	1. 静态分析是分析程序，但实际上从未运行它，其分析说哪里哪里可能有bugs，但实际上从未正面存在问题，也就是静态分析实际上就只是从代码中存在模式，looking for patterns。静态分析可能发现更多的错误，但又必须安全人员人工审查what fuzzing is doing is incrementally exploring the program to come up with these to find lots of problems
![[Pasted image 20241128200346.png]]

第一代fuzzers：纯随机的fuzzers
第二代fuzzers：protocol or grammar based fuzzers:需要手动地建立一个模版for how to create those inputs. 这个模版来constrain the set you're going to explore.因为建立这样的protocol或grammar，其可能无意中只检测了程序的一部分(it may end up inadvertently only checking part of the program because you haven't actually said it's possible to go over this far)

第三代是instrumention guided fuzzers： what instrumentation guided fuzzing does is it generates an input and it watches as the robot's executing the path and it learns from that to come up with the next input. and so sometimes this is branded as ai fuzzing. i don't think of it as ai but it is learning the more it executes。

it's learning about which paths it's already looked at and what are the new places out there。


“Coverage guided fuzzing (also known as greybox fuzzing) **uses program instrumentation to trace the code coverage reached by each input fed to a fuzz target**. Fuzzing engines use this information to make informed decisions about which inputs to mutate to maximize coverage.”