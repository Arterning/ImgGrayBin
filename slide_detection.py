"""滑动验证码缺口检测模块"""
import numpy as np
from PIL import Image, ImageDraw
from io import BytesIO


def detect_slide_gap(image_path: str, output_path: str = "output_detected.png", threshold: int = 100, marker_color: tuple = (255, 255, 0), marker_size: int = 2):
    """
    检测滑动验证码的缺口位置

    参数:
        image_path: 输入图片路径
        output_path: 输出标记后的图片路径
        threshold: 二值化阈值
        marker_color: 标记点的颜色，默认为黄色 (255, 255, 0)
        marker_size: 标记点的大小（半径）

    返回:
        gap_x: 检测到的缺口 x 坐标
        edge_points: 边缘点列表 [(x, y), ...]
    """
    # 1. 读取原始图片（用于后续标记）
    with open(image_path, 'rb') as f:
        image_bytes = f.read()

    original_image = Image.open(BytesIO(image_bytes))
    print(f"原始图片尺寸: {original_image.size}, 模式: {original_image.mode}")

    # 2. 转换为 RGB 模式
    if original_image.mode != 'RGB':
        original_image = original_image.convert('RGB')

    # 3. 进行二值化处理
    image_array = np.array(original_image)
    height, width, channels = image_array.shape

    # 计算灰度值
    r = image_array[:, :, 0]
    g = image_array[:, :, 1]
    b = image_array[:, :, 2]
    gray_matrix = (r * 0.2126 + g * 0.7152 + b * 0.0722).astype(np.uint8)

    # 二值化
    binary_matrix = np.zeros_like(gray_matrix, dtype=np.uint8)
    binary_matrix[gray_matrix > threshold] = 255
    binary_matrix[gray_matrix <= threshold] = 0

    print(f"二值化处理完成，阈值: {threshold}")

    # 4. 检测边缘：统计每列的 255→0 变化次数
    print("\n开始检测边缘...")
    edge_changes = []  # 存储每列的变化次数

    for x in range(width):
        changes = 0
        for y in range(1, height):
            # 检测从白色(255)到黑色(0)的变化
            if binary_matrix[y-1, x] == 255 and binary_matrix[y, x] == 0:
                changes += 1
        edge_changes.append(changes)

    # 5. 找到变化次数最多的列
    max_changes = max(edge_changes)
    gap_x = edge_changes.index(max_changes)

    print(f"\n检测结果:")
    print(f"  - 缺口位置 x 坐标: {gap_x}")
    print(f"  - 该列的边缘变化次数: {max_changes}")

    # 6. 收集该列所有的边缘点
    edge_points = []
    for y in range(1, height):
        if binary_matrix[y-1, gap_x] == 255 and binary_matrix[y, gap_x] == 0:
            edge_points.append((gap_x, y))

    print(f"  - 检测到 {len(edge_points)} 个边缘点")

    # 7. 在原始图片上标记边缘点
    marked_image = original_image.copy()
    draw = ImageDraw.Draw(marked_image)

    for x, y in edge_points:
        # 画一个小圆点
        draw.ellipse(
            [(x - marker_size, y - marker_size), (x + marker_size, y + marker_size)],
            fill=marker_color,
            outline=marker_color
        )

    # 8. 画一条垂直线标记缺口位置
    draw.line([(gap_x, 0), (gap_x, height)], fill=marker_color, width=2)

    # 9. 保存标记后的图片
    marked_image.save(output_path)
    print(f"\n标记后的图片已保存到: {output_path}")

    return gap_x, edge_points


def detect_slide_gap_detailed(image_path: str, output_path: str = "output_detected.png", threshold: int = 100, min_changes: int = 5):
    """
    检测滑动验证码的缺口位置（详细版本，输出更多统计信息）

    参数:
        image_path: 输入图片路径
        output_path: 输出标记后的图片路径
        threshold: 二值化阈值
        min_changes: 被认为是边缘的最小变化次数

    返回:
        gap_x: 检测到的缺口 x 坐标
        edge_points: 边缘点列表
        edge_changes: 每列的变化次数列表
    """
    # 1. 读取原始图片
    with open(image_path, 'rb') as f:
        image_bytes = f.read()

    original_image = Image.open(BytesIO(image_bytes))
    print(f"原始图片尺寸: {original_image.size}, 模式: {original_image.mode}")

    # 2. 转换为 RGB 模式
    if original_image.mode != 'RGB':
        original_image = original_image.convert('RGB')

    # 3. 进行二值化处理
    image_array = np.array(original_image)
    height, width, channels = image_array.shape

    # 计算灰度值
    r = image_array[:, :, 0]
    g = image_array[:, :, 1]
    b = image_array[:, :, 2]
    gray_matrix = (r * 0.2126 + g * 0.7152 + b * 0.0722).astype(np.uint8)

    # 二值化
    binary_matrix = np.zeros_like(gray_matrix, dtype=np.uint8)
    binary_matrix[gray_matrix > threshold] = 255
    binary_matrix[gray_matrix <= threshold] = 0

    print(f"二值化处理完成，阈值: {threshold}")

    # 4. 检测边缘：统计每列的 255→0 变化次数
    print("\n开始检测边缘...")
    edge_changes = []

    for x in range(width):
        changes = 0
        for y in range(1, height):
            if binary_matrix[y-1, x] == 255 and binary_matrix[y, x] == 0:
                changes += 1
        edge_changes.append(changes)

    # 5. 找到变化次数最多的列
    max_changes = max(edge_changes)
    gap_x = edge_changes.index(max_changes)

    print(f"\n检测结果:")
    print(f"  - 缺口位置 x 坐标: {gap_x}")
    print(f"  - 该列的边缘变化次数: {max_changes}")

    # 6. 统计超过阈值的列
    significant_edges = [(x, changes) for x, changes in enumerate(edge_changes) if changes >= min_changes]
    print(f"  - 边缘变化超过 {min_changes} 次的列数: {len(significant_edges)}")

    if len(significant_edges) > 0:
        print(f"  - 前5个显著边缘列:")
        for x, changes in sorted(significant_edges, key=lambda item: item[1], reverse=True)[:5]:
            print(f"      x={x}, 变化次数={changes}")

    # 7. 收集该列所有的边缘点
    edge_points = []
    for y in range(1, height):
        if binary_matrix[y-1, gap_x] == 255 and binary_matrix[y, gap_x] == 0:
            edge_points.append((gap_x, y))

    print(f"  - 在 x={gap_x} 处检测到 {len(edge_points)} 个边缘点")

    # 8. 在原始图片上标记
    marked_image = original_image.copy()
    draw = ImageDraw.Draw(marked_image)

    # 标记主要的缺口位置（黄色）
    for x, y in edge_points:
        draw.ellipse([(x - 2, y - 2), (x + 2, y + 2)], fill=(255, 255, 0), outline=(255, 255, 0))

    # 画垂直线
    draw.line([(gap_x, 0), (gap_x, height)], fill=(255, 255, 0), width=3)

    # 9. 保存标记后的图片
    marked_image.save(output_path)
    print(f"\n标记后的图片已保存到: {output_path}")

    return gap_x, edge_points, edge_changes


def save_edge_analysis(edge_changes: list, output_path: str = "edge_analysis.txt"):
    """
    保存边缘分析结果到文件

    参数:
        edge_changes: 每列的变化次数列表
        output_path: 输出文件路径
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("边缘检测分析结果\n")
        f.write("=" * 80 + "\n\n")
        f.write("列索引(x) | 边缘变化次数\n")
        f.write("-" * 80 + "\n")

        for x, changes in enumerate(edge_changes):
            if changes > 0:
                f.write(f"{x:8d} | {changes:4d} | {'█' * changes}\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write(f"最大变化次数: {max(edge_changes)}\n")
        f.write(f"最大变化位置: x = {edge_changes.index(max(edge_changes))}\n")

    print(f"边缘分析结果已保存到: {output_path}")
