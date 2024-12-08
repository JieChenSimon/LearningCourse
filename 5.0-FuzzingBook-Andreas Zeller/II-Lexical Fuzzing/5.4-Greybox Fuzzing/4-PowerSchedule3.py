"""相对应之前的PowerSchedule2.py, 主要的改变是在example_program函数中不需要手动定义locations = set()，然后使用locations.add(("example_program", 1))来加入了"""

from fuzzingbook.Coverage import Location
from fuzzingbook.MutationFuzzer import FunctionCoverageRunner
from typing import Set, Union, List, Sequence, Dict
import random


class Seed:
   def __init__(self, data: str) -> None:
       self.data = data
       self.coverage: Set[Location] = set()
       self.distance: Union[int, float] = -1
       self.energy = 0.0
   
   def __str__(self) -> str:
       return self.data
   
   __repr__ = __str__

class PowerSchedule:
   def __init__(self) -> None:
       self.path_frequency: Dict = {}
   
   def assignEnergy(self, population: Sequence[Seed]) -> None:
       for seed in population:
           seed.energy = 1
   
   def normalizedEnergy(self, population: Sequence[Seed]) -> List[float]:
       energy = list(map(lambda seed: seed.energy, population))
       sum_energy = sum(energy)
       assert sum_energy != 0
       norm_energy = list(map(lambda nrg: nrg / sum_energy, energy))
       return norm_energy
   
   def choose(self, population: Sequence[Seed]) -> Seed:
       self.assignEnergy(population)
       norm_energy = self.normalizedEnergy(population)
       return random.choices(population, weights=norm_energy)[0]

class ImprovedPowerSchedule(PowerSchedule):
   def assignEnergy(self, population: Sequence[Seed]) -> None:
       for seed in population:
           seed.energy = len(seed.coverage)

def example_program(input_str: str) -> None:
   """
   测试程序，包含三个关键检查点并展示详细的覆盖信息
   """
   # 位置1: 基本输入检查
   if len(input_str) > 0:                
       print(f"位置1被覆盖 - 输入'{input_str}'长度大于0")
       # 位置2: 管理员检查
       if input_str.startswith("admin"): 
           print(f"位置2被覆盖 - 输入'{input_str}'以admin开头")
           # 位置3: 密码检查
           if "password" in input_str:    
               print(f"位置3被覆盖 - 输入'{input_str}'包含password")
               return

def run_basic_schedule_demo():
   print("\n=== 基础调度演示 ===")
   seeds = [Seed("user"), Seed("admin"), Seed("admin_password")]
   schedule = PowerSchedule()
   
   # 使用FunctionCoverageRunner收集覆盖率
   runner = FunctionCoverageRunner(example_program)
   
   for seed in seeds:
       print(f"\n种子 '{seed.data}' 覆盖的位置:")
       runner.run(seed.data) #这里通过使用FunctionCoverageRunner构建的runner, 把seed.data作为输入传入example_program
       seed.coverage = set(runner.coverage())
       for loc in seed.coverage:
           print(f"- 函数: {loc[0]}, 行: {loc[1]}")
   
   hits = {"user": 0, "admin": 0, "admin_password": 0}
   for _ in range(1000):
       chosen_seed = schedule.choose(seeds)
       hits[chosen_seed.data] += 1
   
   print("\n选择统计 (基础调度):")
   for seed_data, count in hits.items():
       percentage = (count / 1000) * 100
       print(f"{seed_data}: {count} 次 ({percentage:.1f}%)")

def run_improved_schedule_demo():
   print("\n=== 改进调度演示 ===")
   seeds = [Seed("user"), Seed("admin"), Seed("admin_password")]
   schedule = ImprovedPowerSchedule()
   runner = FunctionCoverageRunner(example_program)
   
   for seed in seeds:
       runner.run(seed.data)
       seed.coverage = set(runner.coverage())
   
   hits = {"user": 0, "admin": 0, "admin_password": 0}
   for _ in range(1000):
       chosen_seed = schedule.choose(seeds)
       hits[chosen_seed.data] += 1
   
   print("\n选择统计 (改进调度):")
   for seed_data, count in hits.items():
       percentage = (count / 1000) * 100
       print(f"{seed_data}: {count} 次 ({percentage:.1f}%)")

def main():
   print("启动PowerSchedule演示...")
   run_basic_schedule_demo()
   run_improved_schedule_demo()

if __name__ == "__main__":
   main()