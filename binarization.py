"""图片二值化处理模块"""
import numpy as np
from PIL import Image
from io import BytesIO


def convert_to_binary(image_path: str, output_path: str = "output_binary.png", threshold: int = 100):
    """
    将图片进行二值化处理

    参数:
        image_path: 输入图片路径
        output_path: 输出图片路径
        threshold: 灰度阈值，超过此值设为白色(255)，否则设为黑色(0)

    返回:
        binary_matrix: 二值化矩阵 (numpy array)
    """
    # 1. 读取图片文件的字节流
    with open(image_path, 'rb') as f:
        image_bytes = f.read()

    print(f"读取图片字节流成功，大小: {len(image_bytes)} bytes")

    # 2. 解码图片
    image = Image.open(BytesIO(image_bytes))
    print(f"图片解码成功，尺寸: {image.size}, 模式: {image.mode}")

    # 3. 转换为 RGB 模式（如果不是的话）
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # 4. 将图片转换为 numpy 数组
    image_array = np.array(image)
    height, width, channels = image_array.shape
    print(f"图片数组形状: {image_array.shape}")

    # 5. 使用公式计算灰度值: R * 0.2126 + G * 0.7152 + B * 0.0722
    r = image_array[:, :, 0]
    g = image_array[:, :, 1]
    b = image_array[:, :, 2]

    # 计算灰度值
    gray_matrix = r * 0.2126 + g * 0.7152 + b * 0.0722
    gray_matrix = gray_matrix.astype(np.uint8)

    print(f"灰度矩阵计算完成，形状: {gray_matrix.shape}")
    print(f"原始灰度值范围: [{gray_matrix.min()}, {gray_matrix.max()}]")

    # 6. 进行二值化处理
    # 创建一个新的矩阵用于存储二值化结果
    binary_matrix = np.zeros_like(gray_matrix, dtype=np.uint8)

    # 应用阈值：超过阈值的设为白色(255)，否则设为黑色(0)
    binary_matrix[gray_matrix > threshold] = 255
    binary_matrix[gray_matrix <= threshold] = 0

    print(f"二值化处理完成，阈值: {threshold}")
    print(f"白色像素数量: {np.sum(binary_matrix == 255)}")
    print(f"黑色像素数量: {np.sum(binary_matrix == 0)}")

    # 7. 创建二值化图片
    binary_image = Image.fromarray(binary_matrix, mode='L')

    # 8. 保存输出图片
    binary_image.save(output_path)
    print(f"二值化图片已保存到: {output_path}")

    # 9. 返回二值化矩阵
    return binary_matrix


def save_binary_matrix(binary_matrix: np.ndarray, output_path: str = "binary_matrix.txt", format: str = "txt"):
    """
    保存二值化矩阵到文件

    参数:
        binary_matrix: 二值化矩阵
        output_path: 输出文件路径
        format: 输出格式 ('txt', 'csv', 'npy')
    """
    if format == "txt":
        # 保存为文本文件，用 0 和 1 表示，便于阅读
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"二值化矩阵 (形状: {binary_matrix.shape[0]}x{binary_matrix.shape[1]})\n")
            f.write(f"0 表示黑色, 1 表示白色\n")
            f.write("=" * 80 + "\n\n")
            for row in binary_matrix:
                # 将 255 转换为 1，0 保持为 0，便于查看
                f.write(" ".join("1" if val == 255 else "0" for val in row) + "\n")
        print(f"二值化矩阵已保存到文本文件: {output_path}")

    elif format == "csv":
        # 保存为 CSV 文件（保存原始值 0 和 255）
        np.savetxt(output_path, binary_matrix, fmt='%d', delimiter=',')
        print(f"二值化矩阵已保存到 CSV 文件: {output_path}")

    elif format == "npy":
        # 保存为 NumPy 二进制文件
        np.save(output_path, binary_matrix)
        print(f"二值化矩阵已保存到 NumPy 文件: {output_path}")

    else:
        raise ValueError(f"不支持的格式: {format}，请使用 'txt', 'csv' 或 'npy'")


def print_binary_matrix(binary_matrix: np.ndarray, max_rows: int = 20, max_cols: int = 40):
    """
    打印二值化矩阵（可选择只显示部分）

    参数:
        binary_matrix: 二值化矩阵
        max_rows: 最多显示的行数
        max_cols: 最多显示的列数
    """
    height, width = binary_matrix.shape
    print(f"\n二值化矩阵预览 (形状: {height}x{width}):")
    print("█ 表示白色(255), . 表示黑色(0)")
    print("=" * 50)

    # 显示部分矩阵（如果太大的话）
    display_rows = min(max_rows, height)
    display_cols = min(max_cols, width)

    for i in range(display_rows):
        row_str = ""
        for j in range(display_cols):
            # 使用字符可视化：█ 表示白色，. 表示黑色
            if binary_matrix[i, j] == 255:
                row_str += "█"
            else:
                row_str += "."

        if width > max_cols:
            row_str += " ..."
        print(row_str)

    if height > max_rows:
        print("...")

    print("=" * 50)
    white_pixels = np.sum(binary_matrix == 255)
    black_pixels = np.sum(binary_matrix == 0)
    total_pixels = height * width
    print(f"白色像素: {white_pixels} ({white_pixels/total_pixels*100:.2f}%)")
    print(f"黑色像素: {black_pixels} ({black_pixels/total_pixels*100:.2f}%)")
