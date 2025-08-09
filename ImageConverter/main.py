from PIL import Image
import os
import sys


def webp_to_png(webp_path, png_path=None):
    """
    将WebP格式图片转换为PNG格式

    参数:
    webp_path (str): WebP图片的路径
    png_path (str, 可选): 输出PNG图片的路径。如果未提供，将在原路径生成同名PNG文件
    """
    try:
        # 打开WebP图片
        with Image.open(webp_path) as img:
            # 如果未指定输出路径，则在原路径生成同名PNG
            if png_path is None:
                # 分离文件名和扩展名
                filename, _ = os.path.splitext(webp_path)
                png_path = f"{filename}.png"

            # 保存为PNG格式
            img.save(png_path, "PNG")
            print(f"转换成功: {png_path}")
            return True

    except FileNotFoundError:
        print(f"错误: 文件 '{webp_path}' 不存在")
    except Exception as e:
        print(f"转换失败: {str(e)}")

    return False


if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("用法: python webp_to_png.py <webp文件路径> [输出png文件路径]")
    #     print("示例: python webp_to_png.py image.webp")
    #     print("示例: python webp_to_png.py image.webp output.png")
    #     sys.exit(1)

    # webp_file = sys.argv[1]
    # png_file = sys.argv[2] if len(sys.argv) > 2 else None

    d = r'C:\Users\Administrator\Desktop\图标'
    for f in os.listdir(d):
        p = os.path.join(d, f)
        new = os.path.join(d, f+'.png')

        webp_to_png(p, new)
