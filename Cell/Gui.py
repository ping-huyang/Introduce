import os
import sys
# # 控制台输出重定向到一个文件, 主要解决打包后控制台窗口问题
# import ctypes
# sys.stdout = open('./Res/output.txt', 'w')
# if getattr(sys, 'frozen', False):
#     ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
import cv2
import datetime
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QImage, QColor, QTextCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QListWidget, QListWidgetItem, \
    QLabel, QWidget, QVBoxLayout, QHBoxLayout, QDockWidget, QPushButton, QTextEdit, QMessageBox, QRadioButton, QSlider, \
    QDoubleSpinBox, QSplashScreen
project_Path = os.path.dirname(os.path.abspath(__file__))

# 重定向输出到窗口控件
class RedirectOutput:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def write(self, text):
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()

    def flush(self):
        pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 定义变量
        self.error = 200
        self.img = None
        self.garyImg = None
        self.resultImg = None
        self.img_name = None
        self.img_path = None
        self.null_Img = None
        self.kernel_size = 5
        self.threshold = 127
        self.OTUS_threshold = 0
        self.theme_color = "white"
        self.project_path = None
        self.select_Model = "2D_versatile_he"
        self.folder_path = None

        # 设置窗口标题和大小
        self.setWindowTitle("IMG_View_Software")
        self.resize(1600,1050)

        # 获取当前文件交路径
        self.project_path = project_Path;
        # 设置软件图标和主题
        self.setWindowIcon(QIcon(self.project_path + "\Res\ICON.ico"))
        with open(self.project_path + r"\Res\qss\Ubuntu.qss", 'r', encoding="utf-8") as f:
            stylesheet = f.read()
        app.setStyleSheet(stylesheet)

        # 文件
        self.menu = self.menuBar().addMenu("文件")
        self.open_folder_action = QAction("打开所在文件夹", self)
        self.open_folder_action.setShortcut("Ctrl+O")
        self.open_folder_action.triggered.connect(self.open_folder)
        self.menu.addAction(self.open_folder_action)

        # 视图
        self.view_menu = self.menuBar().addMenu("视图")
        self.ImgList_Dock_action = QAction("文件列表", self)
        self.ImgList_Dock_action.setShortcut("Ctrl+H")
        self.ImgList_Dock_action.setCheckable(True)
        self.ImgList_Dock_action.setChecked(True)
        self.view_menu.addAction(self.ImgList_Dock_action)
        self.view_menu.triggered.connect(self.view_menu_triggered)
        self.OutPut_Dock_action = QAction("输出列表", self)
        self.OutPut_Dock_action.setShortcut("Ctrl+J")
        self.OutPut_Dock_action.setCheckable(True)
        self.OutPut_Dock_action.setChecked(True)
        self.view_menu.addAction(self.OutPut_Dock_action)
        self.AI_Model_action = QAction("工具箱", self)
        self.AI_Model_action.setShortcut("Ctrl+K")
        self.AI_Model_action.setCheckable(True)
        self.AI_Model_action.setChecked(True)
        self.view_menu.addAction(self.AI_Model_action)
        self.Algorithm_Dock_action = QAction("参数调节窗口", self)
        self.Algorithm_Dock_action.setShortcut("Ctrl+L")
        self.Algorithm_Dock_action.setCheckable(True)
        self.Algorithm_Dock_action.setChecked(True)
        self.view_menu.addAction(self.Algorithm_Dock_action)

        # 创建图片列表停靠窗口
        self.ImgList_Dock = QDockWidget("Img_List", self)
        self.ImgList_Dock.setMinimumWidth(300)
        self.ImgList_Dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.ImgList_Dock.visibilityChanged.connect(self.handle_dock_widget_visibilityChanged)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.ImgList_Dock)
        self.image_list_widget = QListWidget(self.ImgList_Dock)
        self.image_list_widget.itemDoubleClicked.connect(self.on_image_list_double_clicked)
        self.ImgList_Dock.setWidget(self.image_list_widget)

        # 创建Debug输出停靠窗口
        self.OutPut_Dock = QDockWidget("Output", self)
        self.OutPut_Dock.setMinimumHeight(300)
        self.OutPut_Dock.setAllowedAreas(Qt.BottomDockWidgetArea | Qt.RightDockWidgetArea)
        self.OutPut_Dock.visibilityChanged.connect(self.handle_dock_widget_visibilityChanged)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.OutPut_Dock)
        self.OutputText = QTextEdit()
        self.OutputClearButton = QPushButton("Clear")
        self.OutputClearButton.setMaximumWidth(100)
        self.OutputClearButton.clicked.connect(self.clearOutput)
        self.OutputSaveButton = QPushButton("Save")
        self.OutputSaveButton.setMaximumWidth(100)
        self.OutputSaveButton.clicked.connect(self.saveOutput)
        OutputLayout = QHBoxLayout()
        OutputButtonLayout = QVBoxLayout()
        OutputButtonLayout.addWidget(self.OutputSaveButton)
        OutputButtonLayout.addWidget(self.OutputClearButton)
        OutputLayout.addWidget(self.OutputText)
        OutputLayout.addLayout(OutputButtonLayout)
        Output_widget = QWidget()
        Output_widget.setLayout(OutputLayout)
        self.OutPut_Dock.setWidget(Output_widget)
        self.OutPut_Dock.show();
        # print重定向
        # sys.stdout = RedirectOutput(self.OutputText)

        # 创建AI模型处理停靠窗口
        self.AI_Model_Dock = QDockWidget("工具箱", self)
        self.AI_Model_Dock.setMinimumWidth(300)
        self.AI_Model_Dock.setMinimumHeight(150)
        self.AI_Model_Dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.AI_Model_Dock.visibilityChanged.connect(self.handle_dock_widget_visibilityChanged)
        self.addDockWidget(Qt.RightDockWidgetArea, self.AI_Model_Dock)
        # 搭建AI模型处理停靠窗口的组件
        AI_Model_widget = QWidget()
        AI_Model_Layout = QVBoxLayout()
        self.showGaryImg_Button = QPushButton("显示灰度直方图")
        self.showGaryImg_Button.setEnabled(False)
        self.showGaryImg_Button.clicked.connect(self.showGaryImgHistogram)
        self.showModel_Button = QPushButton("绘制模型处理结果")
        self.showModel_Button.setEnabled(False)
        self.showModel_Button.clicked.connect(self.showModelResult)
        AI_Model_Layout.addWidget(self.showGaryImg_Button)
        AI_Model_Layout.addWidget(self.showModel_Button)
        AI_Model_widget.setLayout(AI_Model_Layout)
        self.AI_Model_Dock.setWidget(AI_Model_widget)
        tipLabel1 = QLabel("选择分割模型")
        tipLabel1.setStyleSheet("color: red; font-size: 25px; max-height: 30px;")
        tipLabel2 = QLabel("阈值分割算法参数调节")
        tipLabel2.setStyleSheet("color: red; font-size: 25px; max-height: 30px;")

        # 创建图像处理算法处理停靠窗口
        self.Algorithm_Dock = QDockWidget("参数调节", self)
        self.Algorithm_Dock.setMinimumWidth(300)
        self.Algorithm_Dock.setMinimumHeight(400)
        self.Algorithm_Dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.Algorithm_Dock.visibilityChanged.connect(self.handle_dock_widget_visibilityChanged)
        self.addDockWidget(Qt.RightDockWidgetArea, self.Algorithm_Dock)
        # 搭建算法停靠窗口的组件
        Algorithm_widget = QWidget()
        Algorithm_HLayout = QVBoxLayout()
        Algorithm_widget.setLayout(Algorithm_HLayout)
        self.Algorithm_Dock.setWidget(Algorithm_widget)
        self.radio_button1 = QRadioButton("2D_versatile_he")
        self.radio_button2 = QRadioButton("2D_paper_dsb2018")
        self.radio_button3 = QRadioButton("2D_versatile_fluo")
        self.radio_button4 = QRadioButton("customize_model")
        self.radio_button_setEnabled(False)
        self.radio_button1.setChecked(True)
        self.radio_button1.clicked.connect(self.on_radio_button_clicked)
        self.radio_button2.clicked.connect(self.on_radio_button_clicked)
        self.radio_button3.clicked.connect(self.on_radio_button_clicked)
        self.radio_button4.clicked.connect(self.on_radio_button_clicked)
        Algorithm_HLayout.addWidget(tipLabel1)
        Algorithm_HLayout.addWidget(self.radio_button1)
        Algorithm_HLayout.addWidget(self.radio_button2)
        Algorithm_HLayout.addWidget(self.radio_button3)
        Algorithm_HLayout.addWidget(self.radio_button4)
        Algorithm_HLayout.addWidget(tipLabel2)
        self.OTSU_threshold_button = QPushButton("大津法最佳阈值")
        self.OTSU_threshold_button.clicked.connect(self.OTSU_threshold_find)
        self.OTSU_threshold_button.setEnabled(False)
        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setRange(0, 255)
        self.threshold_slider.setValue(127)
        self.kernel_size_slider = QDoubleSpinBox()
        self.kernel_size_slider.setDecimals(0)
        self.kernel_size_slider.setMinimumHeight(50)
        self.kernel_size_slider.setMinimum(3)
        self.kernel_size_slider.setMaximum(15)
        self.kernel_size_slider.setSingleStep(2)
        self.kernel_size_slider.setValue(5)
        self.threshold_label = QLabel('Threshold: {}'.format(self.threshold_slider.value()))
        self.kernel_size_label = QLabel('KernelSize: {}'.format(int(self.kernel_size_slider.value())))
        self.threshold_label.setMaximumHeight(20)
        self.kernel_size_label.setMaximumHeight(20)
        Algorithm_HLayout.addWidget(self.threshold_label)
        Algorithm_HLayout.addWidget(self.threshold_slider)
        Algorithm_HLayout.addWidget(self.OTSU_threshold_button)
        Algorithm_HLayout.addWidget(self.kernel_size_label)
        Algorithm_HLayout.addWidget(self.kernel_size_slider)
        self.threshold_slider.setDisabled(True)
        self.kernel_size_slider.setDisabled(True)
        self.threshold_slider.valueChanged.connect(self.update_image)
        self.kernel_size_slider.valueChanged.connect(self.update_image)

        # 主题
        self.theme_menu = self.menuBar().addMenu("主题")
        self.white_theme_action = QAction("白色主题", self)
        self.white_theme_action.setCheckable(True)
        self.white_theme_action.setChecked(True)
        self.white_theme_action.triggered.connect(self.setWhiteTheme)
        self.theme_menu.addAction(self.white_theme_action)
        self.black_theme_action = QAction("黑色主题", self)
        self.black_theme_action.setCheckable(True)
        self.black_theme_action.setChecked(False)
        self.black_theme_action.triggered.connect(self.setBlackTheme)
        self.theme_menu.addAction(self.black_theme_action)

        # 关于
        about_menu = self.menuBar().addMenu("关于")
        about_action = QAction("简介", self)
        about_action.triggered.connect(self.showAbout)
        about_menu.addAction(about_action)
        print_log_action = QAction("打印日志", self)
        print_log_action.triggered.connect(self.printLog)
        about_menu.addAction(print_log_action)

        # 图片按钮提示信息标签
        self.tip1 = QLabel();
        self.tip2 = QLabel();
        self.original_image_label = QLabel()
        self.processed_image_label = QLabel()
        self.original_image_label.setAlignment(Qt.AlignCenter)
        self.processed_image_label.setAlignment(Qt.AlignCenter)
        self.tip1.setMaximumHeight(30)
        self.tip2.setMaximumHeight(30)
        self.tip1.setAlignment(QtCore.Qt.AlignCenter)
        self.tip2.setAlignment(QtCore.Qt.AlignCenter)
        self.tip1.setText("Original_Img")
        self.tip2.setText("Processed_Img")

        # 创建按钮组件
        self.process_button = QPushButton('阈值分割')
        self.process_AI_button = QPushButton('模型分割')
        self.save_button = QPushButton('保存处理结果')
        self.show_result_button = QPushButton('显示统计图')
        self.process_button.setEnabled(False)
        self.process_AI_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.show_result_button.setEnabled(False)
        self.process_button.clicked.connect(self.Img_Process)
        self.process_AI_button.clicked.connect(self.Img_AI_Process)
        self.save_button.clicked.connect(self.Img_Save)
        self.show_result_button.clicked.connect(self.show_result_button_action)

        # 创建布局
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.original_image_label)
        image_layout.addWidget(self.processed_image_label)
        tip_layout = QHBoxLayout()
        tip_layout.addWidget(self.tip1)
        tip_layout.addWidget(self.tip2)
        original_button_layout = QHBoxLayout()
        original_button_layout.addWidget(self.process_button)
        original_button_layout.addWidget(self.process_AI_button)
        processed_button_layout = QHBoxLayout()
        processed_button_layout.addWidget(self.save_button)
        processed_button_layout.addWidget(self.show_result_button)
        button_layout = QHBoxLayout()
        button_layout.addLayout(original_button_layout)
        button_layout.addLayout(processed_button_layout)
        main_layout = QVBoxLayout()
        main_layout.addLayout(tip_layout)
        main_layout.addLayout(image_layout)
        main_layout.addLayout(button_layout)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # 初次加载一个测试文件夹
        self.folder_path = self.project_path + "\Res\img"
        self.loadImg_List(self.folder_path)
        self.null_Img = cv2.imread(self.project_path + "\Res\What.png")
        self.show()

        # 初始时显示默认图片
        self.show_original_img(self.null_Img)
        self.show_processed_img(self.null_Img)

        # 打印测试信息
        self.Init_Message()
        self.printLog()

    # 是否禁用单选框
    def radio_button_setEnabled(self, Open = False):
        if Open:
            self.radio_button1.setEnabled(True)
            self.radio_button2.setEnabled(True)
            self.radio_button3.setEnabled(True)
            self.radio_button4.setEnabled(True)
        else:
            self.radio_button1.setEnabled(False)
            self.radio_button2.setEnabled(False)
            self.radio_button3.setEnabled(False)
            self.radio_button4.setEnabled(False)

    # 显示灰度直方图
    def showGaryImgHistogram(self):
        Process.Show_Gary_Histogram(window, self.garyImg)

    # 绘制模型处理的详细结果
    def showModelResult(self):
        Process.Show_Model_Result(window)

    # 简介
    def showAbout(self):
        about_message = "ImgProcess_Software\r\n" \
                        "ChatGPT + PyQT5 + Opencv\r\n" \
                        "matplotlib + num\r\n" \
                        "Version 1.0\r\n" \
                        "Author: HQP\r\n" \
                        "2023-5-29"
        QMessageBox.about(self, "简介", about_message)

    # 选中的模型
    def on_radio_button_clicked(self):
        radio_button = self.sender()
        self.select_Model = radio_button.text()
        self.Img_AI_Process()

    # 打印日志信息
    def printLog(self):
        # print(self.project_path + "\Res\log.txt")
        try:
            with open(self.project_path + "\Res\log.txt", "r", encoding="utf-8") as f:
                log_text = f.read() + "\r\n"
            self.OutputText.append(log_text)
            self.OutputText.moveCursor(self.OutputText.textCursor().End)
        except Exception as e:
            QMessageBox.warning(self, "警告", "打印日志时发生错误：{}".format(str(e)))

    # 清除输出窗口
    def clearOutput(self):
        self.OutputText.clear()

    # 保存输出信息
    def saveOutput(self):
        # 设置默认的文件名和格式
        default_name = 'Output.txt'
        # 弹出文件对话框，让用户选择要保存的文件路径和名称
        file_path, _ = QFileDialog.getSaveFileName(self, "Save", default_name)
        if file_path:  # 如果用户选择了文件路径，则保存输出文本
            with open(file_path, 'w') as f:
                f.write(self.OutputText.toPlainText())
            self.INFO("保存成功: " + file_path)

    # 打印最初的提示信息
    def Init_Message(self):
        self.OutputText.clear()
        self.INFO('Output test : This is an info message')  # 默认 INFO 模式
        self.INFO('Output test : This is a warning message', mode='WARNING')  # 切换到 WARNING 模式
        self.INFO('Output test : This is an error message', mode='ERROR')  # 切换到 ERROR 本的颜色。以下是扩展后的函数：

    # 切换白色主题
    def setWhiteTheme(self):
        self.theme_color = "white"
        self.white_theme_action.setChecked(True)
        self.black_theme_action.setChecked(False)
        with open(self.project_path + r"\Res\qss\Ubuntu.qss", 'r', encoding="utf-8") as f:
            stylesheet = f.read()
        app.setStyleSheet(stylesheet)
        self.Init_Message()

    # 切换黑色主题
    def setBlackTheme(self):
        self.theme_color = "black"
        self.black_theme_action.setChecked(True)
        self.white_theme_action.setChecked(False)
        with open(self.project_path + r"\Res\qss\OneDark.qss", 'r', encoding="utf-8") as f:
            stylesheet = f.read()
        app.setStyleSheet(stylesheet)
        self.Init_Message()

    # 设置Output打印输出内容
    def INFO(self, *args, mode='INFO'):
        msg = ' '.join(str(arg) for arg in args)
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        mode_str = f'[{timestamp}][{mode:^7}] '
        if(self.theme_color == "white"):
            color = {
                'INFO': QColor(0, 0, 0),
                'WARNING': QColor(0, 0, 156),
                'ERROR': QColor(255, 0, 0),
                'RESULT': QColor(255, 0, 21)
            }[mode]
        else:
            color = {
                'INFO': QColor(255, 255, 255),
                'WARNING': QColor(0, 255, 0),
                'ERROR': QColor(255, 0, 0),
                'RESULT': QColor(255, 255, 0)
            }[mode]
        self.OutputText.setTextColor(color)
        self.OutputText.insertPlainText(mode_str + msg + '\n')
        self.OutputText.moveCursor(self.OutputText.textCursor().End)

    # 列表停靠栏的关闭与开启
    def view_menu_triggered(self, action):
        if action == self.ImgList_Dock_action:
            if self.ImgList_Dock_action.isChecked():
                self.ImgList_Dock.show()
            else:
                self.ImgList_Dock.hide()
        if action == self.OutPut_Dock_action:
            if self.OutPut_Dock_action.isChecked():
                self.OutPut_Dock.show()
            else:
                self.OutPut_Dock.hide()
        if action == self.AI_Model_action:
            if self.AI_Model_action.isChecked():
                self.AI_Model_Dock.show();
            else:
                self.AI_Model_Dock.hide();
        if action == self.Algorithm_Dock_action:
            if self.Algorithm_Dock_action.isChecked():
                self.Algorithm_Dock.show()
            else:
                self.Algorithm_Dock.hide()

    # 解决停靠窗口手动关闭出现的Bug
    def handle_dock_widget_visibilityChanged(self, visible):
        sender = self.sender()
        if visible == False:
            if sender == self.ImgList_Dock:
                self.ImgList_Dock_action.setChecked(False)
            if sender == self.OutPut_Dock:
                self.OutPut_Dock_action.setChecked(False)
            if sender == self.AI_Model_Dock:
                self.AI_Model_action.setChecked(False)
            if sender == self.Algorithm_Dock:
                self.Algorithm_Dock_action.setChecked(False)

    # 选择需要加载图片的文件夹
    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹", os.getcwd())
        if folder_path:
            self.folder_path = folder_path
            self.loadImg_List(self.folder_path)

    # 加载指定文件夹下的图片文件
    def loadImg_List(self, folder_path):
        self.image_list_widget.clear()
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".jpg") or file_name.endswith(".png") or file_name.endswith(".tif"):
                list_item = QListWidgetItem(file_name)
                self.image_list_widget.addItem(list_item)
        if self.image_list_widget.count() > 0:
            self.image_list_widget.setCurrentRow(0)

    # 双击图片列表栏加载显示图片
    def on_image_list_double_clicked(self, item):
        file_name = item.text()
        self.show_original_image(file_name)
        self.save_button.setEnabled(False)
        self.show_result_button.setEnabled(False)
        self.threshold_slider.setDisabled(True)
        self.kernel_size_slider.setDisabled(True)
        self.OTSU_threshold_button.setEnabled(False)
        self.showModel_Button.setEnabled(False)
        self.radio_button_setEnabled(False)
        self.img = cv2.imread(self.img_path)
        self.garyImg = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)

    # 显示原始图片，传入图片路径
    def show_original_image(self, file_name):
        if file_name:
            self.img_name = file_name
            self.img_path = os.path.join(self.folder_path, file_name)
            pixmap = QPixmap()
            pixmap.load(self.img_path)
            pixmap = pixmap.scaled(self.original_image_label.width(), self.original_image_label.height(),
                                   Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.original_image_label.setPixmap(pixmap)
            self.show_processed_img(self.null_Img)
            self.tip1.setText(self.img_name)
            self.process_button.setEnabled(True)
            self.process_AI_button.setEnabled(True)
            self.show_result_button.setEnabled(True)
            self.showGaryImg_Button.setEnabled(True)

    # 显示原始的图片，传入图片数据
    def show_original_img(self, original_img):
        original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
        pixmap = QPixmap.fromImage(
            QImage(original_img.data, original_img.shape[1], original_img.shape[0], QImage.Format_RGB888))
        pixmap = pixmap.scaled(self.original_image_label.width(), self.original_image_label.height(),
                               Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.original_image_label.setPixmap(pixmap)

    # 显示处理后的图片
    def show_processed_img(self, processed_img):
        processed_img = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)
        pixmap = QPixmap.fromImage(
            QImage(processed_img.data, processed_img.shape[1], processed_img.shape[0], QImage.Format_RGB888))
        pixmap = pixmap.scaled(self.processed_image_label.width(), self.processed_image_label.height(),
                               aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        self.processed_image_label.setPixmap(pixmap)

    # 使用图像分割算法处理图像
    def Img_Process(self):
        self.resultImg = Process.Algorithm_Process(window, self.garyImg)
        self.show_processed_img(self.resultImg)
        self.save_button.setEnabled(True)
        self.show_result_button.setEnabled(True)
        self.threshold_slider.setDisabled(False)
        self.kernel_size_slider.setDisabled(False)
        self.OTSU_threshold_button.setEnabled(True)
        self.showModel_Button.setEnabled(False)
        self.radio_button_setEnabled(False)
        self.tip2.setText("阈值分割算法处理结果")

    # 刷新计算结果
    def update_image(self):
        value = int(self.kernel_size_slider.value())
        if value % 2 == 0:
            value += 1
            self.kernel_size_slider.setValue(value)
        self.kernel_size = value
        self.threshold = self.threshold_slider.value()
        self.threshold_label.setText('Threshold: {}'.format(self.threshold))
        self.kernel_size_label.setText('KernelSize: {}'.format(self.kernel_size))
        self.resultImg = Process.Algorithm_Process(window, self.garyImg, False)
        self.show_processed_img(self.resultImg)
        self.tip2.setText(f"高斯内核 ({self.kernel_size},{self.kernel_size}) : 阈值 {self.threshold}")

    # 大津法自动寻找最佳阈值
    def OTSU_threshold_find(self):
        self.resultImg = Process.Algorithm_Process(window, self.garyImg)
        self.show_processed_img(self.resultImg)
        self.threshold = (int)(self.OTUS_threshold)
        self.threshold_label.setText('Threshold: {}'.format(self.threshold))
        size = (int)(self.kernel_size_slider.value())
        self.tip2.setText(f"大津法自动阈值：{self.threshold} 高斯内核：({size},{size})")

    # 使用AI_Model处理图像
    def Img_AI_Process(self):
        # 模型处理显示结果
        self.OTSU_threshold_button.setEnabled(False)
        self.showModel_Button.setEnabled(True)
        self.radio_button_setEnabled(True)
        self.threshold_slider.setDisabled(True)
        self.kernel_size_slider.setDisabled(True)
        self.save_button.setEnabled(True)
        self.show_result_button.setEnabled(True)
        self.resultImg = Process.Model_Process(window, self.garyImg, self.select_Model)
        if self.error == 200:
            self.show_processed_img(self.resultImg)
            self.tip2.setText("模型：{} 处理结果".format(self.select_Model))
        else:
            self.show_processed_img(self.null_Img)
            self.OTSU_threshold_button.setEnabled(False)
            self.showModel_Button.setEnabled(True)
            self.radio_button_setEnabled(True)
            self.threshold_slider.setDisabled(True)
            self.kernel_size_slider.setDisabled(True)
            self.save_button.setEnabled(True)
            self.show_result_button.setEnabled(False)
            self.save_button.setEnabled(False)
            self.process_button.setEnabled(True)
            self.show_result_button.setEnabled(False)

    # 保存处理后的图片
    def Img_Save(self):
        # 设置默认的文件名和格式
        default_name =  'result_' + self.img_name
        suffix = 'JPEG (*.jpg;*.jpeg);;PNG (*.png);;All Files (*)'
        # 弹出文件对话框，让用户选择要保存的文件路径和名称
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", default_name, suffix)
        if file_path:  # 如果用户选择了文件路径，则保存图像
            cv2.imwrite(file_path, self.resultImg)
            self.INFO("保存成功: " + file_path)

    # 显示细胞统计结果统计图
    def show_result_button_action(self):
        Process.Show_CellsNumber_Table(window)

if __name__ == '__main__':
    app = QApplication([])
    # 创建一个QSplashScreen对象，并将其设置为应用程序的启动画面
    splash = QSplashScreen(QPixmap(project_Path + "\Res\SoCool.png"))
    splash.show()
    import Process
    splash.finish(None)
    # 创建应用界面，进入循环
    window = MainWindow()
    app.exec_()
