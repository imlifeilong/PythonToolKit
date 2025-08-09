# 导入必要的库
import os  # 用于文件和目录操作
import tkinter as tk  # 用于创建图形用户界面
from tkinter import filedialog, ttk, messagebox  # tkinter的扩展模块，提供文件选择、高级控件和消息框
from PIL import Image  # 用于图片处理和格式转换
import threading  # 用于多线程处理，避免界面冻结


class ImageConverterApp:
    """图片格式转换工具的主类，封装了所有界面和功能逻辑"""

    def __init__(self, root):
        """初始化方法，设置界面基本属性和初始变量"""
        self.root = root  # 接收主窗口对象
        self.root.title("图片格式转换工具")  # 设置窗口标题
        self.root.geometry("600x400")  # 设置窗口初始大小
        self.root.resizable(True, True)  # 允许窗口在水平和垂直方向调整大小

        # 设置中文字体支持，确保界面中文正常显示
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("SimHei", 10))  # 标签字体
        self.style.configure("TButton", font=("SimHei", 10))  # 按钮字体
        self.style.configure("TCombobox", font=("SimHei", 10))  # 下拉框字体

        # 定义变量存储用户选择
        self.selected_directory = tk.StringVar()  # 存储选中的目录路径
        self.original_format = tk.StringVar(value="webp")  # 原始图片格式，默认webp
        self.target_format = tk.StringVar(value="png")  # 目标图片格式，默认png

        # 调用方法创建界面控件
        self.create_widgets()

    def create_widgets(self):
        """创建并布局所有界面控件"""
        # 创建主框架，用于统一管理控件布局
        main_frame = ttk.Frame(self.root, padding="20")  # 内边距20像素
        main_frame.pack(fill=tk.BOTH, expand=True)  # 填充整个窗口并随窗口大小变化

        # 目录选择部分
        ttk.Label(main_frame, text="选择图片目录:").grid(  # 标签
            row=0, column=0, sticky=tk.W, pady=5)  # 放置在第0行第0列，左对齐，上下间距5

        # 创建目录选择的子框架（输入框+按钮）
        dir_frame = ttk.Frame(main_frame)
        dir_frame.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=5)  # 跨两列，左右拉伸

        # 目录路径输入框
        ttk.Entry(
            dir_frame,
            textvariable=self.selected_directory,  # 绑定到存储目录的变量
            width=50
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))  # 左对齐，水平填充

        # 浏览目录按钮
        ttk.Button(
            dir_frame,
            text="浏览...",
            command=self.browse_directory  # 点击调用浏览目录方法
        ).pack(side=tk.RIGHT)  # 右对齐

        # 格式选择部分
        format_frame = ttk.Frame(main_frame)  # 创建格式选择的子框架
        format_frame.grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=10)  # 跨两列

        # 原始格式标签
        ttk.Label(format_frame, text="原始格式:").pack(side=tk.LEFT, padx=(0, 10))

        # 原始格式下拉框
        original_format_combo = ttk.Combobox(
            format_frame,
            textvariable=self.original_format,  # 绑定到原始格式变量
            values=["webp", "png", "jpg", "jpeg", "bmp", "gif"],  # 支持的格式列表
            state="readonly",  # 只读模式，防止手动输入
            width=10
        )
        original_format_combo.pack(side=tk.LEFT, padx=(0, 20))  # 左对齐，右侧间距20

        # 目标格式标签
        ttk.Label(format_frame, text="转换为:").pack(side=tk.LEFT, padx=(0, 10))

        # 目标格式下拉框
        target_format_combo = ttk.Combobox(
            format_frame,
            textvariable=self.target_format,  # 绑定到目标格式变量
            values=["png", "jpg", "jpeg", "webp", "bmp", "gif"],  # 支持的格式列表
            state="readonly",  # 只读模式
            width=10
        )
        target_format_combo.pack(side=tk.LEFT)  # 左对齐

        # 转换按钮
        ttk.Button(
            main_frame,
            text="开始转换",
            command=self.start_conversion,  # 点击调用开始转换方法
            style="Accent.TButton"
        ).grid(row=3, column=0, columnspan=2, pady=15)  # 跨两列，上下间距15

        # 进度条
        self.progress_var = tk.DoubleVar()  # 存储进度值的变量
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,  # 绑定进度变量
            maximum=100,  # 最大值100（百分比）
            mode="determinate"  # 确定模式（有明确进度）
        )
        self.progress_bar.grid(row=4, column=0, columnspan=2, sticky=tk.EW, pady=5)  # 跨两列，左右拉伸

        # 状态区域
        ttk.Label(main_frame, text="转换状态:").grid(row=5, column=0, sticky=tk.W, pady=5)  # 状态标签

        # 状态文本显示区域（用于显示转换过程信息）
        self.status_text = tk.Text(
            main_frame,
            height=10,  # 高度10行
            width=60,  # 宽度60字符
            state=tk.DISABLED  # 默认禁用编辑
        )
        self.status_text.grid(row=6, column=0, columnspan=2, sticky=tk.NSEW, pady=5)  # 跨两列，随窗口拉伸

        # 为状态文本区域添加滚动条
        scrollbar = ttk.Scrollbar(main_frame, command=self.status_text.yview)  # 绑定文本框的垂直滚动
        scrollbar.grid(row=6, column=2, sticky=tk.NS)  # 放置在文本框右侧，上下拉伸
        self.status_text.config(yscrollcommand=scrollbar.set)  # 文本框滚动与滚动条联动

        # 设置网格权重，使控件随窗口大小调整
        main_frame.columnconfigure(0, weight=1)  # 第0列可拉伸
        main_frame.rowconfigure(6, weight=1)  # 第6行（状态文本）可拉伸
        dir_frame.columnconfigure(0, weight=1)  # 目录框架第0列可拉伸
        format_frame.columnconfigure(0, weight=1)  # 格式框架第0列可拉伸

    def browse_directory(self):
        """打开目录选择对话框，获取用户选择的目录"""
        directory = filedialog.askdirectory()  # 弹出目录选择对话框
        if directory:  # 如果用户选择了目录（不是取消）
            self.selected_directory.set(directory)  # 更新目录变量
            self.update_status(f"已选择目录: {directory}")  # 在状态区显示信息

    def update_status(self, message):
        """更新状态文本区域，显示转换过程信息"""
        self.status_text.config(state=tk.NORMAL)  # 临时启用编辑模式
        self.status_text.insert(tk.END, message + "\n")  # 在末尾添加信息
        self.status_text.see(tk.END)  # 自动滚动到最后一行
        self.status_text.config(state=tk.DISABLED)  # 禁用编辑模式

    def update_progress(self, value):
        """更新进度条显示"""
        self.progress_var.set(value)  # 设置进度值（0-100）

    def convert_image(self, input_path, output_path, target_format):
        """
        转换单张图片的格式
        参数:
            input_path: 输入图片路径
            output_path: 输出图片路径
            target_format: 目标格式
        返回:
            (转换成功标志, 状态信息)
        """
        try:
            with Image.open(input_path) as img:  # 打开图片
                # 特殊处理：透明图片转JPG/JPEG时需要添加白色背景
                if target_format.lower() in ["jpg", "jpeg"] and img.mode in ("RGBA", "LA"):
                    # 创建白色背景（与原图同尺寸）
                    background = Image.new(img.mode[:-1], img.size, (255, 255, 255))
                    # 将原图粘贴到背景上（使用原图的alpha通道作为掩码）
                    background.paste(img, img.split()[-1])
                    img = background  # 替换为带背景的图片

                # 处理JPG格式（PIL中实际使用JPEG作为格式参数）
                if target_format.lower() == 'jpg':
                    target_format = "jpeg"

                # 保存图片为目标格式
                img.save(output_path, target_format.upper())
            return True, f"转换成功: {os.path.basename(output_path)}"
        except Exception as e:
            return False, f"转换失败 {os.path.basename(input_path)}: {str(e)}"

    def process_conversion(self):
        """处理批量转换逻辑（在子线程中运行）"""
        directory = self.selected_directory.get()  # 获取用户选择的目录
        # 定义输出目录（在源目录下创建output文件夹）
        output_directory = os.path.join(directory, "output")
        # 创建输出目录（如果不存在）
        if not os.path.exists(output_directory):
            os.makedirs(output_directory, exist_ok=True)  # exist_ok=True避免目录已存在时报错

        original_ext = self.original_format.get().lower()  # 原始格式（小写）
        target_ext = self.target_format.get().lower()  # 目标格式（小写）

        # 检查目录是否有效
        if not directory:
            messagebox.showerror("错误", "请先选择图片目录")
            return

        # 检查原始格式和目标格式是否相同
        if original_ext == target_ext:
            messagebox.showerror("错误", "原始格式和目标格式不能相同")
            return

        # 筛选目录中所有符合原始格式的文件
        image_files = []
        for filename in os.listdir(directory):
            # 检查文件扩展名是否匹配（不区分大小写）
            if filename.lower().endswith(f".{original_ext}"):
                image_files.append(filename)

        # 如果没有找到符合条件的文件
        if not image_files:
            messagebox.showinfo("提示", f"在所选目录中未找到{original_ext}格式的图片")
            return

        # 开始转换流程
        total_files = len(image_files)  # 总文件数
        self.update_status(f"找到 {total_files} 个{original_ext}格式的图片，开始转换...")
        self.update_progress(0)  # 进度条归零

        success_count = 0  # 成功转换的数量
        fail_count = 0  # 转换失败的数量

        # 遍历所有图片文件进行转换
        for i, filename in enumerate(image_files, 1):  # i从1开始计数
            input_path = os.path.join(directory, filename)  # 输入文件完整路径

            # 生成输出文件名（替换扩展名）
            base_name = os.path.splitext(filename)[0]  # 获取文件名（不含扩展名）
            output_path = os.path.join(output_directory, f"{base_name}.{target_ext}")

            # 避免覆盖已存在的文件：如果文件已存在，添加编号（如image.png → image_1.jpg）
            counter = 1
            while os.path.exists(output_path):
                output_path = os.path.join(output_directory, f"{base_name}_{counter}.{target_ext}")
                counter += 1

            # 转换单张图片
            success, message = self.convert_image(input_path, output_path, target_ext)
            self.update_status(message)  # 显示转换结果

            # 更新成功/失败计数
            if success:
                success_count += 1
            else:
                fail_count += 1

            # 更新进度条（当前进度 = 已处理数/总数 * 100）
            progress = (i / total_files) * 100
            self.update_progress(progress)

        # 转换完成
        self.update_progress(100)  # 进度条拉满
        self.update_status(f"转换完成！成功: {success_count}, 失败: {fail_count}")
        messagebox.showinfo("完成", f"转换完成！成功: {success_count}, 失败: {fail_count}")

    def start_conversion(self):
        """启动转换过程（在新线程中运行，避免界面冻结）"""
        # 检查目录是否有效
        directory = self.selected_directory.get()
        if not directory or not os.path.isdir(directory):
            messagebox.showerror("错误", "请选择有效的目录")
            return

        # 创建子线程运行转换逻辑
        conversion_thread = threading.Thread(target=self.process_conversion)
        conversion_thread.daemon = True  # 设为守护线程，主程序退出时自动结束
        conversion_thread.start()  # 启动线程


# 程序入口
if __name__ == "__main__":
    root = tk.Tk()  # 创建主窗口
    app = ImageConverterApp(root)  # 实例化应用类
    root.mainloop()  # 启动主事件循环
