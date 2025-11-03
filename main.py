from gray_scale import convert_to_grayscale, print_gray_matrix, save_gray_matrix


def main():
    print("=" * 60)
    print("图片灰度处理测试")
    print("=" * 60)

    # 测试图片路径（请替换为你的实际图片路径）
    input_image = "demo.png"  # 你需要准备一张测试图片
    output_image = "output_grayscale.png"

    try:
        # 转换图片为灰度图
        gray_matrix = convert_to_grayscale(input_image, output_image)

        # 打印灰度矩阵（只显示前 10x10 的部分）
        print_gray_matrix(gray_matrix, max_rows=10, max_cols=10)

        # 保存完整的灰度矩阵到文件
        print("\n保存灰度矩阵到文件...")
        save_gray_matrix(gray_matrix, "gray_matrix.txt", format="txt")
        save_gray_matrix(gray_matrix, "gray_matrix.csv", format="csv")
        save_gray_matrix(gray_matrix, "gray_matrix.npy", format="npy")

        print("\n处理完成！")
        print("生成的文件:")
        print(f"  - 灰度图片: {output_image}")
        print("  - 灰度矩阵 (文本): gray_matrix.txt")
        print("  - 灰度矩阵 (CSV): gray_matrix.csv")
        print("  - 灰度矩阵 (NumPy): gray_matrix.npy")

    except FileNotFoundError:
        print(f"\n错误: 找不到图片文件 '{input_image}'")
        print("请在项目目录下放置一张测试图片，或修改 main.py 中的图片路径。")
    except Exception as e:
        print(f"\n处理出错: {e}")


if __name__ == "__main__":
    main()
