from fuzzingbook.Coverage import Location
from typing import Set, Union, List, Sequence, Dict
import random

# use the Location class from the Coverage module
class Seed:
    """代表一个测试输入"""
    def __init__(self, data: str) -> None:
        self.data = data
        self.coverage: Set[Location] = set()  # 记录覆盖的代码位置
        self.distance: Union[int, float] = -1 # 到目标的距离
        self.energy = 0.0                     # 能量值
    
    def __str__(self) -> str:
        return self.data
    
    __repr__ = __str__

class PowerSchedule:
    """定义能量调度策略"""
    def __init__(self) -> None:
        self.path_frequency: Dict = {}
    
    def assignEnergy(self, population: Sequence[Seed]) -> None:
        """分配能量"""
        for seed in population:
            seed.energy = 1
    
    def normalizedEnergy(self, population: Sequence[Seed]) -> List[float]:
        """归一化能量值"""
        energy = list(map(lambda seed: seed.energy, population))
        sum_energy = sum(energy)
        assert sum_energy != 0
        norm_energy = list(map(lambda nrg: nrg / sum_energy, energy))
        return norm_energy
    
    def choose(self, population: Sequence[Seed]) -> Seed:
        """选择种子"""
        self.assignEnergy(population)
        norm_energy = self.normalizedEnergy(population)
        return random.choices(population, weights=norm_energy)[0]

class ImprovedPowerSchedule(PowerSchedule):
    """改进的能量调度策略"""
    def assignEnergy(self, population: Sequence[Seed]) -> None:
        """根据覆盖率分配能量"""
        for seed in population:
            seed.energy = len(seed.coverage)

# 示例程序
def example_program(input_str: str) -> Set[Location]:
   """示例程序：模拟一个简单的登录验证过程
   
   参数:
       input_str: 输入字符串，用于测试不同的登录场景
   
   返回:
       Set[Location]: 包含所有被执行到的代码位置集合
   """
   locations = set()
   
   # 首先检查输入是否为空
   if len(input_str) > 0:  # 位置1：检查基本输入有效性
       locations.add(("example_program", 1))
       print(f"位置1被覆盖 - 输入'{input_str}'长度大于0")
       
       # 检查是否以admin开头（管理员检查）
       if input_str.startswith("admin"):  # 位置2：管理员账户检查
           locations.add(("example_program", 2))
           print(f"位置2被覆盖 - 输入'{input_str}'以admin开头")
           
           # 检查是否包含password（密码验证）
           if "password" in input_str:  # 位置3：密码有效性检查
               locations.add(("example_program", 3))
               print(f"位置3被覆盖 - 输入'{input_str}'包含password")
               
   return locations

# 测试和演示函数
def run_basic_schedule_demo():
    """运行基础调度演示"""
    print("\n=== 基础调度演示 ===")
    seeds = [Seed("user"), Seed("admin"), Seed("admin_password")]
    schedule = PowerSchedule()
    
    # 收集覆盖率
    for seed in seeds:
        print(f"\n种子 '{seed.data}' 覆盖的位置:")
        seed.coverage = example_program(seed.data)
        for loc in seed.coverage:
            print(f"- 函数: {loc[0]}, 行: {loc[1]}")
    
    # 测试选择过程
    hits = {"user": 0, "admin": 0, "admin_password": 0}
    for _ in range(1000):
        chosen_seed = schedule.choose(seeds)
        hits[chosen_seed.data] += 1
    
    print("\n选择统计 (基础调度):")
    for seed_data, count in hits.items():
        percentage = (count / 1000) * 100
        print(f"{seed_data}: {count} 次 ({percentage:.1f}%)")

def run_improved_schedule_demo():
    """运行改进调度演示"""
    print("\n=== 改进调度演示 ===")
    seeds = [Seed("user"), Seed("admin"), Seed("admin_password")]
    schedule = ImprovedPowerSchedule()
    
    # 收集覆盖率
    for seed in seeds:
        seed.coverage = example_program(seed.data)
    
    # 测试选择过程
    hits = {"user": 0, "admin": 0, "admin_password": 0}
    for _ in range(1000):
        chosen_seed = schedule.choose(seeds)
        hits[chosen_seed.data] += 1
    
    print("\n选择统计 (改进调度):")
    for seed_data, count in hits.items():
        percentage = (count / 1000) * 100
        print(f"{seed_data}: {count} 次 ({percentage:.1f}%)")

def main():
    """主函数"""
    print("启动PowerSchedule演示...")
    
    # 运行基础版本演示
    run_basic_schedule_demo()
    
    # 运行改进版本演示
    run_improved_schedule_demo()

if __name__ == "__main__":
    main()