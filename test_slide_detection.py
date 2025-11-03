"""滑动验证码缺口检测测试脚本"""
from slide_detection import detect_slide_gap_detailed, save_edge_analysis


def main():
    print("=" * 60)
    print("滑动验证码缺口检测测试")
    print("=" * 60)

    # 测试图片路径
    input_image = "demo.png"  # 请使用滑动验证码图片进行测试
    output_image = "output_detected.png"
    threshold = 200  # 二值化阈值
    min_changes = 5  # 最小边缘变化次数

    try:
        print(f"\n输入图片: {input_image}")
        print(f"二值化阈值: {threshold}")
        print(f"最小边缘变化次数: {min_changes}")
        print("\n" + "-" * 60)

        # 检测缺口位置（详细版本）
        gap_x, edge_points, edge_changes = detect_slide_gap_detailed(
            input_image,
            output_image,
            threshold=threshold,
            min_changes=min_changes
        )

        # 保存边缘分析结果
        print("\n" + "-" * 60)
        save_edge_analysis(edge_changes, "edge_analysis.txt")

        # 输出结果总结
        print("\n" + "=" * 60)
        print("检测完成！")
        print("=" * 60)
        print(f"\n✓ 检测到的缺口位置: x = {gap_x} 像素")
        print(f"✓ 滑块需要移动的距离: {gap_x} 像素")
        print(f"✓ 检测到的边缘点数量: {len(edge_points)} 个")

        print(f"\n生成的文件:")
        print(f"  - 标记后的图片: {output_image}")
        print(f"  - 边缘分析报告: edge_analysis.txt")

        print(f"\n边缘点坐标（前10个）:")
        for i, (x, y) in enumerate(edge_points[:10]):
            print(f"  {i+1}. ({x}, {y})")
        if len(edge_points) > 10:
            print(f"  ... 还有 {len(edge_points) - 10} 个点")

        print("\n提示:")
        print("  - 黄色垂直线标记了检测到的缺口位置")
        print("  - 黄色点标记了该列上所有的边缘点")
        print("  - 如果检测不准确，可以尝试调整 threshold 参数")
        print("  - 查看 edge_analysis.txt 了解每列的边缘变化情况")

    except FileNotFoundError:
        print(f"\n错误: 找不到图片文件 '{input_image}'")
        print("请准备一张滑动验证码图片，或修改脚本中的图片路径。")
    except Exception as e:
        print(f"\n处理出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
