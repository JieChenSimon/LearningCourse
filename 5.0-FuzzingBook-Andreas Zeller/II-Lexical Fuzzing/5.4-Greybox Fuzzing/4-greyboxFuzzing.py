from fuzzingbook.GreyboxFuzzer import GreyboxFuzzer, FunctionCoverageRunner, Mutator, PowerSchedule, http_program
# from fuzzingbook.MutationFuzzer import FunctionCoverageRunner, http_program

def main():
    # 1. 设置初始种子输入
    seed_input = "http://www.google.com/search?q=fuzzing"
    seeds = [seed_input]
    
    # 2. 创建变异器
    mutator = Mutator()
    
    # 3. 创建能量调度器
    schedule = PowerSchedule()
    
    # 4. 初始化灰盒模糊测试器
    greybox_fuzzer = GreyboxFuzzer(
        seeds=seeds,
        mutator=mutator,
        schedule=schedule
    )
    
    # 5. 创建覆盖率运行器
    http_runner = FunctionCoverageRunner(http_program)
    
    # 6. 运行模糊测试
    outcomes = greybox_fuzzer.runs(http_runner, trials=10000)
    
    # 7. 检查结果
    print("Fuzzing completed!")
    print(f"Number of tests executed: {len(outcomes)}")
    
    # 8. 获取和显示种群信息
    population = greybox_fuzzer.population

    print(f"Final population size: {len(population)}")
    
    # 9. 可选：显示发现的有趣输入
    for idx, input_value in enumerate(population[:20]):
        print(f"Seed {idx}: {input_value}")


if __name__ == "__main__":
    main()