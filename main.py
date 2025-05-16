import sys
import string
import secrets
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QSpinBox, QCheckBox, QPushButton, QSlider,
    QGroupBox, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon


class PasswordGenerator:
    """密码生成器类，负责生成安全的随机密码"""
    
    def __init__(self):
        # 字符集
        self.lowercase_chars = string.ascii_lowercase
        self.uppercase_chars = string.ascii_uppercase
        self.digit_chars = string.digits
        self.special_chars = "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?"
        
    def generate_password(self, length=12, use_lowercase=True, use_uppercase=True,
                         use_digits=True, use_special=True, custom_special=None):
        """
        生成随机密码
        
        参数:
            length: 密码长度
            use_lowercase: 是否使用小写字母
            use_uppercase: 是否使用大写字母
            use_digits: 是否使用数字
            use_special: 是否使用特殊字符
            custom_special: 自定义特殊字符集
        
        返回:
            生成的随机密码
        """
        # 确定字符集
        chars = ""
        if use_lowercase:
            chars += self.lowercase_chars
        if use_uppercase:
            chars += self.uppercase_chars
        if use_digits:
            chars += self.digit_chars
        if use_special:
            if custom_special:
                chars += custom_special
            else:
                chars += self.special_chars
                
        # 验证字符集是否为空
        if not chars:
            raise ValueError("字符集为空，无法生成密码")
            
        # 使用cryptographically strong RNG生成密码
        password = ''.join(secrets.choice(chars) for _ in range(length))
        
        # 确保密码满足复杂性要求
        has_requirements = self._password_meets_requirements(
            password, use_lowercase, use_uppercase, use_digits, 
            use_special, custom_special
        )
        
        # 如果不满足要求，重新生成
        while not has_requirements:
            password = ''.join(secrets.choice(chars) for _ in range(length))
            has_requirements = self._password_meets_requirements(
                password, use_lowercase, use_uppercase, use_digits, 
                use_special, custom_special
            )
            
        return password
    
    def _password_meets_requirements(self, password, use_lowercase, use_uppercase,
                                   use_digits, use_special, custom_special):
        """
        检查密码是否满足要求
        """
        # 如果要求的字符类型没有在密码中出现，则返回False
        if use_lowercase and not any(c in self.lowercase_chars for c in password):
            return False
        if use_uppercase and not any(c in self.uppercase_chars for c in password):
            return False
        if use_digits and not any(c in self.digit_chars for c in password):
            return False
        if use_special:
            special_set = custom_special if custom_special else self.special_chars
            if not any(c in special_set for c in password):
                return False
                
        return True


class PasswordGeneratorApp(QMainWindow):
    """密码生成器应用界面"""
    
    def __init__(self):
        super().__init__()
        
        self.password_generator = PasswordGenerator()
        
        # 设置窗口属性
        self.setWindowTitle("密码生成器")
        self.setMinimumSize(500, 400)
        
        # 创建中央部件和布局
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # 创建界面元素
        self._create_password_display()
        self._create_length_settings()
        self._create_character_settings()
        self._create_special_chars_settings()
        self._create_buttons()
        
        # 初始生成一个密码
        self._generate_password()
        
    def _create_password_display(self):
        """创建密码显示区域"""
        password_group = QGroupBox("生成的密码")
        password_layout = QVBoxLayout()
        
        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        self.password_display.setFont(QFont("Consolas", 14))
        
        password_layout.addWidget(self.password_display)
        password_group.setLayout(password_layout)
        
        self.main_layout.addWidget(password_group)
        
    def _create_length_settings(self):
        """创建密码长度设置区域"""
        length_group = QGroupBox("密码长度")
        length_layout = QVBoxLayout()
        
        slider_layout = QHBoxLayout()
        self.length_slider = QSlider(Qt.Orientation.Horizontal)
        self.length_slider.setMinimum(4)
        self.length_slider.setMaximum(64)
        self.length_slider.setValue(16)
        self.length_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.length_slider.setTickInterval(4)
        
        self.length_spinbox = QSpinBox()
        self.length_spinbox.setMinimum(4)
        self.length_spinbox.setMaximum(64)
        self.length_spinbox.setValue(16)
        
        # 连接滑块和数字选择框
        self.length_slider.valueChanged.connect(self.length_spinbox.setValue)
        self.length_spinbox.valueChanged.connect(self.length_slider.setValue)
        
        slider_layout.addWidget(self.length_slider)
        slider_layout.addWidget(self.length_spinbox)
        
        length_layout.addLayout(slider_layout)
        length_group.setLayout(length_layout)
        
        self.main_layout.addWidget(length_group)
        
    def _create_character_settings(self):
        """创建字符类型设置区域"""
        char_group = QGroupBox("字符类型")
        char_layout = QVBoxLayout()
        
        self.use_lowercase = QCheckBox("小写字母 (a-z)")
        self.use_lowercase.setChecked(True)
        
        self.use_uppercase = QCheckBox("大写字母 (A-Z)")
        self.use_uppercase.setChecked(True)
        
        self.use_digits = QCheckBox("数字 (0-9)")
        self.use_digits.setChecked(True)
        
        self.use_special = QCheckBox("特殊字符")
        self.use_special.setChecked(True)
        
        char_layout.addWidget(self.use_lowercase)
        char_layout.addWidget(self.use_uppercase)
        char_layout.addWidget(self.use_digits)
        char_layout.addWidget(self.use_special)
        
        char_group.setLayout(char_layout)
        
        self.main_layout.addWidget(char_group)
        
    def _create_special_chars_settings(self):
        """创建特殊字符设置区域"""
        special_group = QGroupBox("自定义特殊字符集")
        special_layout = QVBoxLayout()
        
        self.special_chars_edit = QLineEdit()
        self.special_chars_edit.setPlaceholderText("自定义特殊字符，如果为空则使用默认值")
        self.special_chars_edit.setText("!@#$%^&*()-_=+")
        
        special_layout.addWidget(self.special_chars_edit)
        special_group.setLayout(special_layout)
        
        self.main_layout.addWidget(special_group)
        
    def _create_buttons(self):
        """创建按钮区域"""
        button_layout = QHBoxLayout()
        
        self.generate_button = QPushButton("生成密码")
        self.generate_button.clicked.connect(self._generate_password)
        
        self.copy_button = QPushButton("复制密码")
        self.copy_button.clicked.connect(self._copy_password)
        
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.copy_button)
        
        self.main_layout.addLayout(button_layout)
        
    def _generate_password(self):
        """生成并显示密码"""
        # 检查至少选择了一种字符类型
        if not any([
            self.use_lowercase.isChecked(),
            self.use_uppercase.isChecked(),
            self.use_digits.isChecked(),
            self.use_special.isChecked()
        ]):
            QMessageBox.warning(
                self, 
                "警告", 
                "请至少选择一种字符类型"
            )
            return
        
        try:
            password = self.password_generator.generate_password(
                length=self.length_spinbox.value(),
                use_lowercase=self.use_lowercase.isChecked(),
                use_uppercase=self.use_uppercase.isChecked(),
                use_digits=self.use_digits.isChecked(),
                use_special=self.use_special.isChecked(),
                custom_special=self.special_chars_edit.text() if self.use_special.isChecked() else None
            )
            
            self.password_display.setText(password)
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成密码时出错: {str(e)}")
            
    def _copy_password(self):
        """复制密码到剪贴板"""
        if self.password_display.text():
            # 使用QApplication的剪贴板功能
            QApplication.clipboard().setText(self.password_display.text())
            
            # 显示短暂的提示信息
            QMessageBox.information(self, "成功", "密码已复制到剪贴板")


def main():
    app = QApplication(sys.argv)
    window = PasswordGeneratorApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
