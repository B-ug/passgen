import os
import PyInstaller.__main__

# 定义图标文件路径
icon_path = 'password_lock.ico'

# 定义打包参数
pyinstaller_args = [
    'main.py',  # 主程序文件
    '--name=密码生成器',  # 可执行文件名称
    '--onefile',  # 打包成单个文件
    f'--icon={icon_path}',  # 应用图标
    '--windowed',  # 不显示控制台窗口
    '--clean',  # 清理临时文件
    '--noconfirm',  # 不询问确认
]

# 执行PyInstaller打包
print("开始打包...")
PyInstaller.__main__.run(pyinstaller_args)
print("打包完成！") 