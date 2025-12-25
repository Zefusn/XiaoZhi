import pandas as pd
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
import sqlite3
from tkinter import Scrollbar

class ExcelLabelAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("小志标签处理")
        self.root.geometry("800x800")
        self.root.resizable(False, False)  # 固定窗口大小    

        # 创建 Notebook（分页）
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=BOTH, expand=True)

        # 第一页：Excel 数据分析
        self.page1 = ttk.Frame(self.notebook)
        self.notebook.add(self.page1, text="Excel 数据分析") 

        # 第二页：小志标签处理
        self.page2 = ttk.Frame(self.notebook)
        self.notebook.add(self.page2, text="小志标签处理")   

        # 第三页：SQL 查询和结果展示
        self.page3 = ttk.Frame(self.notebook)
        self.notebook.add(self.page3, text="SQL 查询")        

        # 初始化第一页
        self.init_page1()

        # 初始化第二页
        self.init_page2()

        # 初始化第三页
        self.init_page3()

        # 当前加载的数据
        self.current_data_page1 = None  # 第一页的数据
        self.current_data_page2 = None  # 第二页的数据
        self.conn_page1 = None  # 第一页的 SQLite 连接
        self.conn_page2 = None  # 第二页的 SQLite 连接

    def toggle_function_usage(self):
        """处理功能使用复选框的状态变化"""
        if self.function_usage_var.get():
            # 如果功能使用复选框被选中，取消低量标签复选框的选中状态
            self.low_volume_var.set(False)

    def toggle_low_volume(self):
        """处理低量标签复选框的状态变化"""
        if self.low_volume_var.get():
            # 如果低量标签复选框被选中，取消功能使用复选框的选中状态
            self.function_usage_var.set(False)

    def init_page1(self):
        # 文件选择部分
        self.file_frame = ttk.LabelFrame(self.page1, text="选择 Excel 文件", padding="10")
        self.file_frame.grid(row=0, column=0, sticky=(W, E))
        self.file_entry = ttk.Entry(self.file_frame, width=50)
        self.file_entry.grid(row=0, column=0, padx=5, pady=5)
        self.browse_button = ttk.Button(self.file_frame, text="浏览", command=self.browse_file)
        self.browse_button.grid(row=0, column=1, padx=5, pady=5)

        # 设备 ID 输入部分
        self.device_id_frame = ttk.LabelFrame(self.page1, text="输入需要去除的设备ID（用逗号分隔）", padding="10")
        self.device_id_frame.grid(row=1, column=0, sticky=(W, E), pady=10)
        self.device_id_entry = ttk.Entry(self.device_id_frame, width=50)
        self.device_id_entry.grid(row=0, column=0, padx=5, pady=5)

        # 数据选择部分
        self.data_type_frame = ttk.LabelFrame(self.page1, text="选择数据类型", padding="10")
        self.data_type_frame.grid(row=2, column=0, sticky=(W, E))
        self.initial_data_var = BooleanVar(value=True)
        self.initial_data_check = ttk.Checkbutton(self.data_type_frame, text="初始数据", variable=self.initial_data_var)
        self.initial_data_check.grid(row=0, column=0, padx=5, pady=5)
        self.user_data_var = BooleanVar(value=True)
        self.user_data_check = ttk.Checkbutton(self.data_type_frame, text="用户数据", variable=self.user_data_var)
        self.user_data_check.grid(row=0, column=1, padx=5, pady=5)

        # 平台选择部分
        self.platform_frame = ttk.LabelFrame(self.page1, text="选择平台", padding="10")
        self.platform_frame.grid(row=3, column=0, sticky=(W, E))
        self.platform_var = StringVar(value="安卓")
        self.android_radio = ttk.Radiobutton(self.platform_frame, text="安卓", variable=self.platform_var, value="安卓")
        self.android_radio.grid(row=0, column=0, padx=5, pady=5)
        self.ios_radio = ttk.Radiobutton(self.platform_frame, text="iOS", variable=self.platform_var, value="iOS")
        self.ios_radio.grid(row=0, column=1, padx=5, pady=5)

        # 查询按钮
        self.query_button = ttk.Button(self.page1, text="查询", command=self.analyze_data)
        self.query_button.grid(row=4, column=0, pady=10)

        # 结果显示部分
        self.result_frame = ttk.LabelFrame(self.page1, text="分析结果", padding="10")
        self.result_frame.grid(row=5, column=0, sticky=(W, E))

        # 创建多列 Treeview
        self.tree = ttk.Treeview(self.result_frame, columns=("指标", "初始数据", "用户数据"), show="headings")
        self.tree.heading("指标", text="指标")
        self.tree.heading("初始数据", text="初始数据")
        self.tree.heading("用户数据", text="用户数据")
        self.tree.grid(row=0, column=0, sticky=(W, E))

        # 添加滚动条
        scrollbar = ttk.Scrollbar(self.result_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky=(N, S))

        # 添加右键菜单，支持复制
        self.tree.bind("<Button-3>", lambda event: self.show_context_menu(event, self.tree))
        self.context_menu = Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="复制", command=lambda: self.copy_selection(self.tree))

        # 添加全选按钮
        self.select_all_button = ttk.Button(self.result_frame, text="全选", command=lambda: self.select_all(self.tree))
        self.select_all_button.grid(row=1, column=0, pady=5)

    def init_page2(self):
        # 文件选择部分
        self.file_frame_page2 = ttk.LabelFrame(self.page2, text="选择 Excel 文件", padding="10")
        self.file_frame_page2.grid(row=0, column=0, sticky=(W, E), pady=10)
        self.file_entry_page2 = ttk.Entry(self.file_frame_page2, width=50)
        self.file_entry_page2.grid(row=0, column=0, padx=5, pady=5)
        self.browse_button_page2 = ttk.Button(self.file_frame_page2, text="浏览", command=self.browse_file_page2)
        self.browse_button_page2.grid(row=0, column=1, padx=5, pady=5)

        # 设备 ID 输入部分
        self.device_id_frame_page2 = ttk.LabelFrame(self.page2, text="输入需要去除的设备ID（用逗号分隔）", padding="10")
        self.device_id_frame_page2.grid(row=1, column=0, sticky=(W, E), pady=10)
        self.device_id_entry_page2 = ttk.Entry(self.device_id_frame_page2, width=50)
        self.device_id_entry_page2.grid(row=0, column=0, padx=5, pady=5)

        # 条件选择部分
        self.condition_frame = ttk.LabelFrame(self.page2, text="条件选择", padding="10")
        self.condition_frame.grid(row=2, column=0, sticky=(W, E), pady=10)
        self.platform_var_page2 = StringVar(value="安卓")
        self.android_radio_page2 = ttk.Radiobutton(self.condition_frame, text="安卓", variable=self.platform_var_page2, value="安卓")
        self.android_radio_page2.grid(row=0, column=0, padx=5, pady=5)
        self.ios_radio_page2 = ttk.Radiobutton(self.condition_frame, text="iOS", variable=self.platform_var_page2, value="iOS")
        self.ios_radio_page2.grid(row=0, column=1, padx=5, pady=5)
        self.function_usage_var = BooleanVar()
        self.function_usage_check = ttk.Checkbutton(self.condition_frame, text="功能使用", variable=self.function_usage_var, command=self.toggle_function_usage)
        self.function_usage_check.grid(row=1, column=0, padx=5, pady=5)
        self.low_volume_var = BooleanVar()
        self.low_volume_check = ttk.Checkbutton(self.condition_frame, text="低量标签", variable=self.low_volume_var, command=self.toggle_low_volume)
        self.low_volume_check.grid(row=1, column=1, padx=5, pady=5)
        self.generate_button = ttk.Button(self.condition_frame, text="生成", command=self.generate_results_page2)
        self.generate_button.grid(row=2, column=0, columnspan=2, pady=10)

        # 结果显示部分（第二页）
        self.result_frame_page2 = ttk.LabelFrame(self.page2, text="分析结果", padding="10")
        self.result_frame_page2.grid(row=3, column=0, sticky=(W, E), pady=10)
        self.select_all_button_page2 = ttk.Button(self.result_frame_page2, text="全选", command=lambda: self.select_all(self.tree_page2))
        self.select_all_button_page2.grid(row=0, column=0, pady=5, sticky=W)
        self.tree_page2 = ttk.Treeview(self.result_frame_page2, columns=("标签名称", "数量"), show="headings")
        self.tree_page2.heading("标签名称", text="标签名称")
        self.tree_page2.heading("数量", text="数量")
        self.tree_page2.grid(row=1, column=0, sticky=(W, E))
        scrollbar_page2 = ttk.Scrollbar(self.result_frame_page2, orient=VERTICAL, command=self.tree_page2.yview)
        self.tree_page2.configure(yscroll=scrollbar_page2.set)
        scrollbar_page2.grid(row=1, column=1, sticky=(N, S))
        self.tree_page2.bind("<Button-3>", lambda event: self.show_context_menu(event, self.tree_page2))
        self.context_menu_page2 = Menu(self.root, tearoff=0)
        self.context_menu_page2.add_command(label="复制", command=lambda: self.copy_selection(self.tree_page2))

    def init_page3(self):
        # SQL 查询部分（第三页）
        self.sql_frame = ttk.LabelFrame(self.page3, text="SQL 查询", padding="10")
        self.sql_frame.grid(row=0, column=0, sticky=(W, E), pady=10)
        self.sql_entry = Text(self.sql_frame, width=60, height=10)  # 增大宽度和高度
        self.sql_entry.grid(row=0, column=0, padx=5, pady=5)

        # 添加垂直滚动条
        scrollbar_sql = Scrollbar(self.sql_frame, command=self.sql_entry.yview)
        scrollbar_sql.grid(row=0, column=1, sticky=(N, S))
        self.sql_entry.config(yscrollcommand=scrollbar_sql.set)

        # 执行 SQL 按钮
        self.execute_sql_button = ttk.Button(self.sql_frame, text="执行 SQL", command=self.execute_sql_page3)
        self.execute_sql_button.grid(row=0, column=2, padx=5, pady=5)

        # 结果显示部分（第三页）
        self.result_frame_page3 = ttk.LabelFrame(self.page3, text="分析结果", padding="10")
        self.result_frame_page3.grid(row=1, column=0, sticky=(W, E), pady=10)
        self.select_all_button_page3 = ttk.Button(self.result_frame_page3, text="全选", command=lambda: self.select_all(self.tree_page3))
        self.select_all_button_page3.grid(row=0, column=0, pady=5, sticky=W)
        self.tree_page3 = ttk.Treeview(self.result_frame_page3, columns=("标签名称", "数量"), show="headings")
        self.tree_page3.heading("标签名称", text="标签名称")
        self.tree_page3.heading("数量", text="数量")
        self.tree_page3.grid(row=1, column=0, sticky=(W, E))
        scrollbar_page3 = ttk.Scrollbar(self.result_frame_page3, orient=VERTICAL, command=self.tree_page3.yview)
        self.tree_page3.configure(yscroll=scrollbar_page3.set)
        scrollbar_page3.grid(row=1, column=1, sticky=(N, S))
        self.tree_page3.bind("<Button-3>", lambda event: self.show_context_menu(event, self.tree_page3))
        self.context_menu_page3 = Menu(self.root, tearoff=0)
        self.context_menu_page3.add_command(label="复制", command=lambda: self.copy_selection(self.tree_page3))

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        self.file_entry.delete(0, END)
        self.file_entry.insert(0, file_path)

    def browse_file_page2(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        self.file_entry_page2.delete(0, END)
        self.file_entry_page2.insert(0, file_path)

    def analyze_data(self):
        file_path = self.file_entry.get()
        if not file_path:
            messagebox.showerror("错误", "请先选择Excel文件")
            return

        device_ids = self.device_id_entry.get()
        if not device_ids and self.user_data_var.get():
            messagebox.showerror("错误", "请输入需要去除的设备ID")
            return

        try:
            # 读取Excel文件
            df = pd.read_excel(file_path)
            print("读取的数据：")
            print(df.head())  # 打印前几行数据，检查是否读取正确

            # 将输入的设备ID拆分为列表，并去除空格
            device_id_list = [id.strip() for id in device_ids.split(",")] if device_ids else []
            print("需要去除的设备ID：", device_id_list)  # 打印设备ID列表，检查是否正确拆分

            # 初始数据（未去除设备ID）
            initial_data = df.copy()

            # 用户数据（去除多个设备ID）
            user_data = df[~df['deviceId'].isin(device_id_list)] if device_id_list else df.copy()
            print("用户数据：")
            print(user_data.head())  # 打印用户数据，检查是否正确过滤

            # 根据选择的平台过滤数据
            platform = self.platform_var.get()
            if platform == "安卓":
                platform_label = "安卓"
                platform_initial_data = initial_data[initial_data['pkgName'] == 'com.helloxj.xlook']
                platform_user_data = user_data[user_data['pkgName'] == 'com.helloxj.xlook']
            elif platform == "iOS":
                platform_label = "iOS"
                platform_initial_data = initial_data[initial_data['pkgName'] == 'cs.zero.waterCamera']
                platform_user_data = user_data[user_data['pkgName'] == 'cs.zero.waterCamera']
            else:
                messagebox.showerror("错误", "未知平台")
                return

            # 清空Treeview
            for i in self.tree.get_children():
                self.tree.delete(i)

            # 统计数据
            initial_stats = {
                "总数据量": len(platform_initial_data),
                "使用人数": platform_initial_data['deviceId'].nunique(),
                "给出指令次数": platform_initial_data['directives'].notna().sum(),
                "有帮助次数": platform_initial_data[platform_initial_data['avail'] == '有帮助'].shape[0],
                "无帮助次数": platform_initial_data[platform_initial_data['avail'] == '无帮助'].shape[0]
            }

            user_stats = {
                "总数据量": len(platform_user_data),
                "使用人数": platform_user_data['deviceId'].nunique(),
                "给出指令次数": platform_user_data['directives'].notna().sum(),  # 基于用户数据
                "有帮助次数": platform_user_data[platform_user_data['avail'] == '有帮助'].shape[0],
                "无帮助次数": platform_user_data[platform_user_data['avail'] == '无帮助'].shape[0]
            }

            # 插入数据
            for key in initial_stats.keys():
                initial_value = initial_stats[key] if self.initial_data_var.get() else ""
                user_value = user_stats[key] if self.user_data_var.get() else ""
                self.tree.insert("", "end", values=(f"{platform_label} - {key}", initial_value, user_value))

            # 将数据加载到 SQLite 数据库
            self.current_data_page1 = platform_user_data
            self.conn_page1 = sqlite3.connect(':memory:')
            self.current_data_page1.to_sql('data', self.conn_page1, index=False, if_exists='replace')

        except Exception as e:
            messagebox.showerror("错误", str(e))

    def generate_results_page2(self):
        file_path = self.file_entry_page2.get()
        if not file_path:
            messagebox.showerror("错误", "请先选择Excel文件")
            return

        device_ids = self.device_id_entry_page2.get()
        if not device_ids:
            messagebox.showerror("错误", "请输入需要去除的设备ID")
            return

        try:
            df = pd.read_excel(file_path)
            required_columns = ['question', 'pkgName', 'deviceId', 'userContent']
            if not all(column in df.columns for column in required_columns):
                messagebox.showerror("错误", f"Excel 文件中缺少以下字段之一: {', '.join(required_columns)}")
                return

            # 将输入的设备ID拆分为列表，并去除空格
            device_id_list = [id.strip() for id in device_ids.split(",")] if device_ids else []
            print("需要去除的设备ID：", device_id_list)  # 打印设备ID列表，检查是否正确拆分

            # 去除指定设备ID的数据
            filtered_df = df[~df['deviceId'].isin(device_id_list)]
            
            # 根据选择的平台过滤数据
            platform = self.platform_var_page2.get()
            if platform == "安卓":
                platform_data = filtered_df[filtered_df['pkgName'] == 'com.helloxj.xlook']
            elif platform == "iOS":
                platform_data = filtered_df[filtered_df['pkgName'] == 'cs.zero.waterCamera']
            else:
                messagebox.showerror("错误", "未知平台")
                return
            
            # 根据选择的条件生成结果
            if self.function_usage_var.get():
                # 功能使用分析
                result = platform_data['question'].value_counts().reset_index()
            elif self.low_volume_var.get():
                # 低量标签分析
                result = platform_data['question'].value_counts().reset_index()
                # 过滤出数量较少的标签（例如小于10个）
                result = result[result['count'] < 10]
            else:
                # 默认分析
                result = platform_data['question'].value_counts().reset_index()
            
            # 清空Treeview
            for i in self.tree_page2.get_children():
                self.tree_page2.delete(i)
            
            # 插入数据到Treeview
            for index, row in result.iterrows():
                self.tree_page2.insert("", "end", values=(row['question'], row['count']))
            
            # 将数据加载到SQLite数据库
            self.current_data_page2 = platform_data
            self.conn_page2 = sqlite3.connect(':memory:')
            self.current_data_page2.to_sql('data', self.conn_page2, index=False, if_exists='replace')
            
        except Exception as e:
            messagebox.showerror("错误", str(e))
    
    def execute_sql_page3(self):
        """执行SQL查询并显示结果"""
        sql_query = self.sql_entry.get("1.0", END).strip()
        if not sql_query:
            messagebox.showerror("错误", "请输入SQL查询语句")
            return
        
        try:
            # 检查是否有可用的连接
            conn = self.conn_page1 or self.conn_page2
            if not conn:
                messagebox.showerror("错误", "没有可用的数据连接，请先加载数据")
                return
            
            # 执行SQL查询
            df = pd.read_sql_query(sql_query, conn)
            
            # 清空Treeview
            for i in self.tree_page3.get_children():
                self.tree_page3.delete(i)
            
            # 插入数据到Treeview
            for index, row in df.iterrows():
                self.tree_page3.insert("", "end", values=(row[0], row[1]))
                
        except Exception as e:
            messagebox.showerror("错误", str(e))
    
    def show_context_menu(self, event, tree):
        """显示右键菜单"""
        self.context_menu.post(event.x_root, event.y_root)
    
    def copy_selection(self, tree):
        """复制选中的内容"""
        selected_items = tree.selection()
        if not selected_items:
            return
        
        # 复制选中项的内容
        self.root.clipboard_clear()
        for item in selected_items:
            values = tree.item(item, 'values')
            self.root.clipboard_append('\t'.join(map(str, values)) + '\n')
    
    def select_all(self, tree):
        """全选Treeview中的所有项"""
        items = tree.get_children()
        for item in items:
            tree.selection_add(item)

# 程序入口
if __name__ == "__main__":
    root = Tk()
    app = ExcelLabelAnalyzer(root)
    root.mainloop()