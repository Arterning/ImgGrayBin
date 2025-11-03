"""图片灰度处理模块"""
import numpy as np
from PIL import Image
from pathlib import Path


def convert_to_grayscale(image_path: str, output_path: str = "output_grayscale.png"):
    """
    读取图片文件，转换为灰度图片并输出

    参数:
        image_path: 输入图片路径
        output_path: 输出图片路径

    返回:
        gray_matrix: 灰度值矩阵 (numpy array)
    """
    # 1. 读取图片文件的字节流
    with open(image_path, 'rb') as f:
        image_bytes = f.read()

    print(f"读取图片字节流成功，大小: {len(image_bytes)} bytes")

    # 2. 解码图片
    from io import BytesIO
    image = Image.open(BytesIO(image_bytes))
    print(f"图片解码成功，尺寸: {image.size}, 模式: {image.mode}")

    # 3. 转换为 RGB 模式（如果不是的话）
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # 4. 将图片转换为 numpy 数组
    image_array = np.array(image)
    height, width, channels = image_array.shape
    print(f"图片数组形状: {image_array.shape}")

    # 5. 使用指定公式计算灰度值: R * 0.2126 + G * 0.7152 + B * 0.0722
    # 提取 RGB 通道
    r = image_array[:, :, 0]
    g = image_array[:, :, 1]
    b = image_array[:, :, 2]

    # 计算灰度值
    gray_matrix = r * 0.2126 + g * 0.7152 + b * 0.0722
    gray_matrix = gray_matrix.astype(np.uint8)

    print(f"灰度矩阵计算完成，形状: {gray_matrix.shape}")

    # 6. 创建灰度图片
    gray_image = Image.fromarray(gray_matrix, mode='L')

    # 7. 保存输出图片
    gray_image.save(output_path)
    print(f"灰度图片已保存到: {output_path}")

    # 8. 返回灰度矩阵
    return gray_matrix


def save_gray_matrix(gray_matrix: np.ndarray, output_path: str = "gray_matrix.txt", format: str = "txt"):
    """
    保存灰度矩阵到文件

    参数:
        gray_matrix: 灰度值矩阵
        output_path: 输出文件路径
        format: 输出格式 ('txt', 'csv', 'npy')
    """
    if format == "txt":
        # 保存为文本文件，每行一个像素行
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"灰度矩阵 (形状: {gray_matrix.shape[0]}x{gray_matrix.shape[1]})\n")
            f.write("=" * 80 + "\n\n")
            for row in gray_matrix:
                f.write(" ".join(f"{val:3d}" for val in row) + "\n")
        print(f"灰度矩阵已保存到文本文件: {output_path}")

    elif format == "csv":
        # 保存为 CSV 文件
        np.savetxt(output_path, gray_matrix, fmt='%d', delimiter=',')
        print(f"灰度矩阵已保存到 CSV 文件: {output_path}")

    elif format == "npy":
        # 保存为 NumPy 二进制文件
        np.save(output_path, gray_matrix)
        print(f"灰度矩阵已保存到 NumPy 文件: {output_path}")

    else:
        raise ValueError(f"不支持的格式: {format}，请使用 'txt', 'csv' 或 'npy'")


def print_gray_matrix(gray_matrix: np.ndarray, max_rows: int = 10, max_cols: int = 10):
    """
    打印灰度矩阵（可选择只显示部分）

    参数:
        gray_matrix: 灰度值矩阵
        max_rows: 最多显示的行数
        max_cols: 最多显示的列数
    """
    height, width = gray_matrix.shape
    print(f"\n灰度矩阵 (形状: {height}x{width}):")
    print("=" * 50)

    # 显示部分矩阵（如果太大的话）
    display_rows = min(max_rows, height)
    display_cols = min(max_cols, width)

    for i in range(display_rows):
        row_values = []
        for j in range(display_cols):
            row_values.append(f"{gray_matrix[i, j]:3d}")

        row_str = " ".join(row_values)
        if width > max_cols:
            row_str += " ..."
        print(row_str)

    if height > max_rows:
        print("...")

    print("=" * 50)
    print(f"灰度值范围: [{gray_matrix.min()}, {gray_matrix.max()}]")
    print(f"平均灰度值: {gray_matrix.mean():.2f}")
