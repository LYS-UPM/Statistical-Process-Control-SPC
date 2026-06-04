import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 设定工业生产参数 (汽车传动轴加工)
# ==========================================
target_mean = 50.00       # 目标轴径 50.00 mm
tolerance = 0.05          # 公差 ±0.05 mm
USL = target_mean + tolerance  # 规格上限
LSL = target_mean - tolerance  # 规格下限
std_dev_base = 0.008      # 正常的机床加工标准差

n_subgroups = 30          # 抽取 30 个批次
n_samples = 5             # 每个批次抽检 5 个零件

# ==========================================
# 2. 生成模拟数据 (注入工业缺陷)
# ==========================================
np.random.seed(42) # 保证每次生成的数据一样
data = np.zeros((n_subgroups, n_samples))

for i in range(n_subgroups):
    current_mean = target_mean
    current_std = std_dev_base
    
    # 注入缺陷 1：刀具磨损 (Tool Wear)
    # 从第 15 批次开始，刀具磨损导致加工尺寸均值慢慢变大
    if i >= 15:
        current_mean += (i - 14) * 0.003 
        
    # 注入缺陷 2：机床异常震动 (Machine Vibration)
    # 第 25 批次时，机床轴承松动，导致波动瞬间变大
    if i == 25:
        current_std = std_dev_base * 4 

    data[i] = np.random.normal(current_mean, current_std, n_samples)

# ==========================================
# 3. SPC 核心计算 (X-bar 和 R)
# ==========================================
x_bar = np.mean(data, axis=1) # 计算每批次的平均值
r = np.max(data, axis=1) - np.min(data, axis=1) # 计算每批次的极差 (最大值-最小值)

# 计算中心线 (Center Lines)
x_bar_bar = np.mean(x_bar)
r_bar = np.mean(r)

# 查表常数 (当 n=5 时)
A2, D3, D4 = 0.577, 0, 2.114

# 计算控制界限 (Control Limits)
UCL_x = x_bar_bar + A2 * r_bar
LCL_x = x_bar_bar - A2 * r_bar
UCL_r = D4 * r_bar
LCL_r = D3 * r_bar

# ==========================================
# 4. 计算制程能力指数 (Cpk) - 取前 14 个健康批次计算
# ==========================================
healthy_data = data[:14].flatten()
overall_mean = np.mean(healthy_data)
overall_std = np.std(healthy_data, ddof=1)
Cp = (USL - LSL) / (6 * overall_std)
Cpk = min((USL - overall_mean)/(3 * overall_std), (overall_mean - LSL)/(3 * overall_std))

# ==========================================
# 5. 数据可视化 (绘制 X-bar 和 R Chart)
# ==========================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# --- 绘制 X-bar Chart ---
ax1.plot(x_bar, marker='o', color='b', linestyle='-', label='Subgroup Mean')
ax1.axhline(x_bar_bar, color='g', linestyle='-', label='Center Line (CL)')
ax1.axhline(UCL_x, color='r', linestyle='--', label='UCL / LCL')
ax1.axhline(LCL_x, color='r', linestyle='--')
# 标出超标的点
out_of_control_x = np.where((x_bar > UCL_x) | (x_bar < LCL_x))[0]
ax1.plot(out_of_control_x, x_bar[out_of_control_x], 'ro', markersize=8, label='Out of Control (Tool Wear)')
ax1.set_title('X-bar Chart: Monitoring Process Mean (Tool Wear Detection)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Mean Dimension (mm)')
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend(loc='upper left')

# --- 绘制 R Chart ---
ax2.plot(r, marker='s', color='darkorange', linestyle='-', label='Subgroup Range')
ax2.axhline(r_bar, color='g', linestyle='-', label='Center Line (CL)')
ax2.axhline(UCL_r, color='r', linestyle='--', label='UCL / LCL')
ax2.axhline(LCL_r, color='r', linestyle='--')
# 标出超标的点
out_of_control_r = np.where((r > UCL_r) | (r < LCL_r))[0]
ax2.plot(out_of_control_r, r[out_of_control_r], 'ro', markersize=8, label='Out of Control (Vibration)')
ax2.set_title('R Chart: Monitoring Process Variability (Vibration Detection)', fontsize=12, fontweight='bold')
ax2.set_xlabel('Subgroup Number')
ax2.set_ylabel('Range (mm)')
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.legend(loc='upper left')

# 添加 Cpk 文本框
textstr = '\n'.join((
    r'Process Capability Analysis (Healthy Phase):',
    r'$C_p=%.2f$' % (Cp, ),
    r'$C_{pk}=%.2f$' % (Cpk, )))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax1.text(0.75, 0.95, textstr, transform=ax1.transAxes, fontsize=11,
        verticalalignment='top', bbox=props)

plt.tight_layout()
plt.show()