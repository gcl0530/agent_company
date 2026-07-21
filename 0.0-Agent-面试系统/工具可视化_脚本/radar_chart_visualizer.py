# radar_chart_visualizer.py

# --- 针对 Windows 环境和 Python 3.10+ 类型提示的配置 ---
# 在 Windows 环境下，matplotlib 通常可以自动找到合适的显示后端，
# 无需手动设置 'Agg'。plt.show() 会弹出图形窗口。
# import matplotlib
# matplotlib.use('Qt5Agg') # 或者 'TkAgg', 'wxAgg' 等，通常不需要手动指定
# ------------------------------------------------------------

import json
import matplotlib.pyplot as plt
import numpy as np
import os
# 在 Python 3.10+ 中，list, tuple, Optional 等可以直接使用，无需 typing 模块
# from typing import List, Tuple, Optional # 可选，但通常不需要了

class MemberSkillsVisualizer:
    """
    一个集成的类，用于加载 JSON 配置、创建成员数据并绘制能力雷达图。
    """
    def __init__(self, config_path: str):
        """
        初始化可视化工具。

        Args:
            config_path (str): 团队成员配置文件的路径 (JSON格式)。
        """
        self.config_path = config_path
        self.data = self._load_config()
        if not self.data:
            # 如果加载失败，抛出异常
            raise ValueError("Configuration loading failed. Please check file path and format.")

        self.skill_dimensions: list[str] = self.data.get("skill_dimensions", [])
        self.max_score: int = self.data.get("max_score", 5)
        self.members_data: dict[str, dict[str, int]] = self.data.get("members", {})

        if not self.skill_dimensions or not self.members_data:
            print("Warning: No skill dimensions or members found in configuration. Cannot plot.")
            self.num_vars = 0
            self.angles = []
            # 允许继续，plot_radar_charts 会检查并处理空数据
            return

        self.num_vars = len(self.skill_dimensions)
        # 计算角度
        self.angles: list[float] = np.linspace(0, 2 * np.pi, self.num_vars, endpoint=False).tolist()
        # 使图形闭合，需要将第一个角度复制到末尾
        self.angles += self.angles[:1]

    def _load_config(self) -> dict:
        """
        从 JSON 文件加载配置数据。

        Returns:
            dict: 配置文件中的数据。
        """
        print(f"Attempting to load config from: '{os.path.abspath(self.config_path)}'") # 打印绝对路径
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file not found at '{self.config_path}'")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON file '{self.config_path}': {e}")
            return {}
        except Exception as e:
            print(f"An unexpected error occurred while loading config: {e}")
            return {}

    # 使用 Python 3.10+ 的类型提示
    def _prepare_scores_for_plotting(self, member_name: str) -> tuple[list[int], str] | None:
        """
        为指定成员准备用于雷达图绘图的分数列表。

        Args:
            member_name (str): 成员的姓名。

        Returns:
            tuple[list[int], str] | None: (用于绘图的分数列表, 成员姓名) 或 None 如果成员不存在。
        """
        member_skills = self.members_data.get(member_name)
        if not member_skills:
            print(f"Warning: Member '{member_name}' not found in configuration.")
            return None

        # 确保所有维度都有分数，不存在的默认为 0
        # 技能值应该是整数
        scores: list[int] = [member_skills.get(dim, 0) for dim in self.skill_dimensions]
        scores_for_plot = scores + scores[:1] # 闭合图表
        return scores_for_plot, member_name

    # 使用 Python 3.10+ 的类型提示
    def plot_radar_charts(self, member_names: list[str] | None = None):
        """
        绘制一个或多个成员的能力雷达图。

        Args:
            member_names (list[str] | None): 要绘制的成员姓名列表。
                                             如果为 None，则绘制所有成员。
        """
        if not self.skill_dimensions or not self.members_data:
            print("No skills or members loaded. Cannot plot.")
            return

        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        ax.set_title("Team Skill Radar Chart", va='bottom', y=1.1)

        # 绘制网格线和标签
        # 将角度转换为度数用于 set_thetagrids
        ax.set_thetagrids(np.degrees(self.angles[:-1]), self.skill_dimensions)
        ax.yaxis.set_tick_params(pad=5) # 调整y轴刻度标签的间距

        # 设置y轴刻度范围
        ax.set_ylim(0, self.max_score)
        # 设置y轴刻度为整数
        ax.set_yticks(np.arange(0, self.max_score + 1, 1))
        # 显示y轴刻度标签
        ax.set_yticklabels([str(i) for i in range(self.max_score + 1)])

        # 确定要绘制的成员
        members_to_plot = member_names if member_names is not None else list(self.members_data.keys())

        # 绘制每个成员的雷达图
        for name in members_to_plot:
            plot_data = self._prepare_scores_for_plotting(name)
            if plot_data:
                scores_for_plot, member_name_label = plot_data
                ax.plot(self.angles, scores_for_plot, marker='o', label=member_name_label, linestyle='-')
                ax.fill(self.angles, scores_for_plot, alpha=0.25) # 填充区域

        # 添加图例
        # bbox_to_anchor 参数调整图例的位置，使其在图形之外
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

        # --- 在 Windows 环境下，直接显示图形窗口 ---
        print("Displaying radar chart window...")
        plt.show()
        # plt.show() 会阻塞程序直到用户关闭图形窗口
        # 在窗口关闭后，程序将继续执行后面的代码（如果有的话）
        # 脚本执行完毕后，窗口会自行关闭

# --- 主程序逻辑 ---
if __name__ == "__main__":
    # 获取当前脚本所在目录，用于找到配置文件
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 假设 team_members.json 在同一目录下
    config_file_path = os.path.join(current_dir, 'team_members.json')

    try:
        # 1. 初始化可视化器
        # __init__ 中已经包含了对配置加载的错误处理和打印信息
        visualizer = MemberSkillsVisualizer(config_file_path)

        # 2. 检查 visualizer 是否成功加载了数据，只有在有数据时才绘制
        if visualizer.skill_dimensions and visualizer.members_data:
            visualizer.plot_radar_charts()
        else:
            print("Skipping plotting due to missing or invalid configuration data.")

    except ValueError as ve:
        # 捕获 __init__ 中抛出的加载失败异常
        print(f"Initialization error: {ve}")
    except Exception as e:
        # 捕获其他任何意外错误
        print(f"An unexpected error occurred during execution: {e}")