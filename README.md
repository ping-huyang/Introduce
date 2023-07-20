## <font color="yellow">简历个人作品详细介绍</font>
### <a name="目录"></a>目录

#### [完全模型组智能车竞赛](#第一部分)
#### [多种人机交互方式的电子小制作](#第二部分)
#### [倒立摆专业课程设计](#第三部分)

### <font color="yellow"><a name="第一部分"></a>一：完全模型组智能车竞赛</font>
#### [1.1 效果展示图](#1.1)

![img1](https://github.com/ping-huyang/Introduce/blob/main/img/Icar1.png)
#### [1.2 成绩](#1.2)
第十八届全国大学生智能车华南赛中获得一等奖
#### [1.3 硬件资源、软件平台](#1.3)
- Edgeboard Linux开发板（赛道图像处理）、RT1064最小系统板（智能车运动控制）、vscode、keil、NVC、匿名助手
#### [1.4 主要完成的内容](#1.4)
- 主要负责智能车的运动控制的实现与优化：电机舵机PID控制、陀螺仪角度控制。
- 与上位机串口通信协议的设计与实现。
- 部分赛道元素的控制：出入库、侧方位停车、陡坡等
- 各种调试、测试、选型：陀螺仪性能测试与选择、程序运行一些数据的波形显示，QT串口调试软件
- 屏幕、按键等等调试方面的功能实现
- 协助上位机软件同学完成赛道图像处理算法
#### [1.5 部分资源位置](#1.5)
- 下位机部分程序（/Icar/RT1064_Code）
- 自行开发的QT上位机（/Icar/QT_Code）

### <font color="yellow"><a name="第二部分"></a>二：多种人机交互方式的电子小制作</font>
#### [2.1 效果展示图](#2.1)

![img2](https://github.com/ping-huyang/Introduce/blob/main/img/PCB1.png)

![img3](https://github.com/ping-huyang/Introduce/blob/main/img/Home1.png)

#### [2.2 硬件资源、软件平台](#2.2)
- ESP32、STM32、各种传感器、腾讯云服务器、MQTT、蓝牙模块、语音模块
- 语言主要为C/C++
#### [2.3 主要完成的内容](#2.3)
- 0.96OLED基于u8g2完成的菜单栏设计
- 通过四个按键模拟传统的按键交互方式
- 通过特定的语音词汇与开发板进行交互和控制
- 通过手机蓝牙APP控制
- 通过MQTT远程控制
#### [2.4 部分资源位置](#2.3)
- ESP32开源程序（/Home/ESP32_Code）

### <font color="yellow"><a name="第三部分"></a>三：倒立摆专业课程设计</font>
#### [3.1 效果展示图](#3.1)
![img4](https://github.com/ping-huyang/Introduce/blob/main/img/Inverted1.png)

![img5](https://github.com/ping-huyang/Introduce/blob/main/img/Inverted2.png)

![img6](https://github.com/ping-huyang/Introduce/blob/main/img/Inverted3.png)
#### [3.2 硬件资源、软件平台](#3.2)
- 倒立摆套件（核心板STM32F103C8T6）、IMX6ULL MIN开发板（QT专用串口软件）
#### [3.3 主要完成的内容](#3.3)
- 创新点在于优化了人机交互的方式。开发了一个专用的上位机控制软件，使控制或调试都更加方便，增加使用体验。主要涉及的内容包括：QT软件开发、串口通信、位置环速度环PD控制、交叉编译等。
#### [3.4 部分资源位置](#3.3)
- STM32开源代码（/Inverted/STM32_Code）
- QT上位机软件（/Inverted/QT_Code）
