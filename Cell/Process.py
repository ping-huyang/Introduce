import cv2
import numpy as np
import matplotlib.pyplot as plt
from stardist.models import StarDist2D
import matplotlib
import traceback

# 指定使用Qt5作为可视化后端
matplotlib.use('Qt5Agg')

# 定义全局变量用来保存数据
cell_areas = []
cell_count = 0
labels = None
colored_labels = None


'''*************************************************************************************
* @note    : 显示灰度度和灰度直方图
* @note    : none 
* @note    : none 
* @note    : none
* @time     : 2023/05/30 08:43:11
*************************************************************************************'''

# 显示灰度直方图
def Show_Gary_Histogram(window,img):
    # 计算直方图
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    # 绘制直方图
    plt.plot(hist)
    # 显示图像和直方图
    plt.subplot(121), plt.imshow(img, cmap='gray'), plt.title(window.img_name)
    plt.subplot(122), plt.plot(hist)
    plt.xlim([0, 256])
    plt.show()
    window.INFO("灰度直方图显示成功！！！")
    plt.show(block=True)


'''*************************************************************************************
* @note    : 传入一个灰度图像，进行处理，将处理后的结果图像返回 
* @note    : none 
* @note    : none 
* @note    : none
* @time     : 2023/05/30 08:43:11
*************************************************************************************'''

# 打印统计结果表格
def Show_CellsNumber_Table(window):
    global cell_count
    global cell_areas
    for i, area in enumerate(cell_areas):
        window.INFO(f"细胞{i + 1} 面积: {area}", mode="RESULT")
    window.INFO(f"共计: {cell_count} 个细胞", mode="RESULT")
    plt.hist(cell_areas, bins=20)
    plt.xlabel("Cell Area")
    plt.ylabel("Frequency")
    plt.title("Cell Area Histogram")
    plt.annotate(f"Number of cells: {cell_count}", xy=(0.7, 0.9), xycoords='axes fraction', fontsize=12)
    plt.tight_layout()
    plt.show()
    plt.show(block=True)

'''*****************************************
* @note    : 图像分割算法处理
* @time     : 2023/05/30 08:43:11
*****************************************'''
# 具体的图像分割算法实现
def Algorithm_Process(window, image, OTUS = True):
    # window.INFO(">>>> Begain Process >>>>\r\n", mode="INFO")
    # 0. 参数变量设置
    global cell_count
    global cell_areas
    kernel_size = window.kernel_size
    # 1. 图像预处理
    blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    if OTUS:
        _, thresholded = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        window.OTUS_threshold = _
    else:
        _, thresholded = cv2.threshold(blurred, window.threshold, 255, cv2.THRESH_BINARY_INV)
    # 2. 使用阈值分割和轮廓检测进行细胞分割
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    image_contours = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(image_contours, contours, -1, (0, 255, 0), 2)
    # 3. 计算细胞个数和面积
    cell_count = len(contours)
    cell_areas = [cv2.contourArea(contour) for contour in contours]
    # 打印细胞面积和细胞结果
    window.INFO(f"细胞个数: {cell_count}", mode="INFO")
    # window.INFO(">>>>>  Finished!!! >>>>>\r\n", mode="INFO")
    return image_contours


'''*****************************************
* @note     : 调用模型处理
* @time     : 2023/05/30 08:43:11
*****************************************'''
# 图像归一化处理
def normalize_image(img):
    # 将图像归一化到 [0, 1] 范围
    normalized_img = (img - np.min(img)) / (np.max(img) - np.min(img))
    return normalized_img

# 2D_versatile_he模型加载处理
def Model_Process(window: object, img_input, model_name):
    # 变量和参数定义
    global cell_count
    global cell_areas
    global labels
    global colored_labels
    model_path = f"{window.project_path}\\{model_name}\\weights_best.h5"
    # 加载模型
    try:
        # model = StarDist2D.from_pretrained(model_name)
        window.INFO(model_name)
        model = StarDist2D(None, name=model_name)
        model.load_weights(model_path)
    except Exception as e:
        window.error = 404
        window.INFO(f"Failed to load model {model_name}: {e}")
        tb_str = traceback.format_exc()  # Get the traceback information as a string
        tb_lines = tb_str.splitlines()  # Split the string into individual lines
        window.INFO(tb_str)
        window.INFO(f"{model_name}:\n{tb_lines[-1]}")  # Print the last line of the traceback
        return img_input
    # 根据不同的模型进行不同的处理
    if model_name == '2D_versatile_he':
        # 对传入的图像预处理，使之符合模型要求
        if len(img_input.shape) == 2:
            img = np.repeat(img_input[..., np.newaxis], 3, axis=2)
        else:
            gray_image = cv2.cvtColor(img_input, cv2.COLOR_RGB2GRAY)
            img = np.repeat(gray_image[..., np.newaxis], 3, axis=2)
        img_normalized = normalize_image(img)
        # 使用模型进行细胞分割
        labels, _ = model.predict_instances(img_normalized)
    else:
        img_input = img_input.astype(np.float32)
        img_input /= 255.0
        labels, _ = model.predict_instances(img_input)
    # 统计细胞数量和面积
    cell_count = labels.max()
    cell_areas = [(labels == i).sum() for i in range(1, cell_count + 1)]
    # 将标签转换为彩色图像以便可视化
    colored_labels = plt.cm.nipy_spectral(labels / labels.max())
    # 将标签转换为彩色图像以便可视化
    result_img = cv2.applyColorMap((labels / labels.max() * 255).astype('uint8'), cv2.COLORMAP_PARULA)
    window.INFO(f"使用模型：<{model_name}> 分割的结果为细胞数：{cell_count} 个", mode="RESULT")
    window.error = 200
    return result_img


# 可视化显示模型分割出来的效果对比图
def Show_Model_Result(window):
    global cell_count
    global cell_areas
    global labels
    global colored_labels
    # 打印细胞数目和细胞面积信息
    for i, area in enumerate(cell_areas):
        window.INFO(f"细胞{i + 1} 面积: {area}", mode="RESULT")
    window.INFO(f"共计: {cell_count} 个细胞", mode="RESULT")
    # 绘制统计结果
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 3, 1)
    plt.imshow(window.garyImg, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')
    plt.subplot(1, 3, 2)
    plt.imshow(colored_labels)
    plt.title(window.select_Model + ' : Segmentation Result')
    plt.axis('off')
    plt.subplot(1, 3, 3)
    plt.hist(cell_areas, bins=20)
    plt.xlabel("Cell Area")
    plt.ylabel("Frequency")
    plt.title("Cell Area Histogram")
    plt.annotate(f"Number of cells: {cell_count}", xy=(0.7, 0.9), xycoords='axes fraction', fontsize=12)
    plt.tight_layout()
    plt.show()
    plt.show(block=True)

