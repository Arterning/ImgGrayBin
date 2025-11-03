"""图片二值化测试脚本"""
from binarization import convert_to_binary, print_binary_matrix, save_binary_matrix


def main():
    print("=" * 60)
    print("图片二值化处理测试")
    print("=" * 60)

    # 测试图片路径（请替换为你的实际图片路径）
    input_image = "demo.png"  # 你需要准备一张测试图片
    output_image = "output_binary.png"
    threshold = 200  # 二值化阈值

    try:
        print(f"\n使用阈值: {threshold}")
        print(f"  - 灰度值 > {threshold} → 白色 (255)")
        print(f"  - 灰度值 ≤ {threshold} → 黑色 (0)\n")

        # 转换图片为二值化图片
        binary_matrix = convert_to_binary(input_image, output_image, threshold)

        # 打印二值化矩阵的可视化预览
        print_binary_matrix(binary_matrix, max_rows=20, max_cols=60)

        # 保存完整的二值化矩阵到文件
        print("\n保存二值化矩阵到文件...")
        save_binary_matrix(binary_matrix, "binary_matrix.txt", format="txt")
        save_binary_matrix(binary_matrix, "binary_matrix.csv", format="csv")
        save_binary_matrix(binary_matrix, "binary_matrix.npy", format="npy")

        print("\n处理完成！")
        print("生成的文件:")
        print(f"  - 二值化图片: {output_image}")
        print("  - 二值化矩阵 (文本): binary_matrix.txt")
        print("  - 二值化矩阵 (CSV): binary_matrix.csv")
        print("  - 二值化矩阵 (NumPy): binary_matrix.npy")

        # 提示：可以尝试不同的阈值
        print("\n提示：你可以修改 threshold 参数来尝试不同的二值化效果")
        print("  - threshold 越小，黑色区域越多")
        print("  - threshold 越大，白色区域越多")

    except FileNotFoundError:
        print(f"\n错误: 找不到图片文件 '{input_image}'")
        print("请在项目目录下放置一张测试图片，或修改脚本中的图片路径。")
    except Exception as e:
        print(f"\n处理出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
