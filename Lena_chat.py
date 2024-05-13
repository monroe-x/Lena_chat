print("正在加载")
print("如果是初次加载 可能在下载模型")
from PyQt5.QtWidgets import QPushButton,QFrame,QScrollArea,QTextEdit,QTextBrowser, QVBoxLayout,QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap,QPainter, QPixmap,QFont, QColor,QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer,QRect,Qt
from PyQt5 import uic
import sys
import threading
import keyboard
import time
import ui_ci
import prompt
import staream



moren_prompt = "你扮演'you'，你叫莉娜,是一个活泼开朗的语音聊天乐趣机器人，你的回复简短（就像正常人聊天），你还会主动发起问题或使用emoji表达情感"






import json
import set

with open('set.json', 'r') as f:
    set_json = json.load(f)

if set_json["open_again"] == True:
    # print(set_json["open_again"])
    set.sockett()

    with open('set.json', 'r') as f:
        set_json = json.load(f)

## 设置
prompt.openai_api_key = set_json["openai_api_key"]
prompt.openai_api_base_url = set_json["openai_api_base_url"]
prompt.chat_model = set_json["chat_model"]
prompt.openai_voice_model = set_json["openai_voice_model"]
staream.whisper_locality_model = set_json["whisper_locality_model"]
whisper_device_compute = json.loads(set_json["whisper_device_compute"])
staream.whisper_device = whisper_device_compute['whisper_device']
staream.whisper_compute_type = whisper_device_compute['whisper_compute_type']
prompt.init_prompt = set_json["init_prompt"]
if prompt.init_prompt == "":
    prompt.init_prompt = moren_prompt

# print(prompt.init_prompt)

threading.Thread(target=staream.main,daemon=True).start()
prompt.set_()




app = QApplication(sys.argv)
window = uic.loadUi('user.ui')
icon = QIcon('icon.png')
window.setWindowIcon(icon)

# window.show()


pixmap_noron = QPixmap("noron.jpg")
# 背景图片
def on_paint_event(event, widget):
    qp = QPainter()
    qp.begin(widget)
    
    # 获取窗口和图片的原始尺寸
    window_width = widget.width()
    window_height = widget.height()
    img_width = pixmap_noron.width()
    img_height = pixmap_noron.height()

    # 计算新的高度以保持长宽比
    new_height = int(window_width * img_height / img_width)
    if new_height <= window_height:
        new_width = int(window_height * img_width / img_height)
        scaled_pixmap = pixmap_noron.scaled(new_width, window_height, Qt.KeepAspectRatio)
        scaled_pixmap = scaled_pixmap.copy(int((new_width - window_width )/2), 0, scaled_pixmap.width() - int((new_width - window_width )/2), scaled_pixmap.height())
        qp.drawPixmap(0, 0, scaled_pixmap)
        qp.end()
    else:
        scaled_pixmap = pixmap_noron.scaled(window_width, new_height, Qt.KeepAspectRatio)

        qp.drawPixmap(0, 0, scaled_pixmap)
        qp.end()


window.paintEvent = lambda event: on_paint_event(event, window)






class AutoResizingTextEdit(QTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置样式
        self.setStyleSheet("border-radius: 10px; background-color: rgba(255, 255, 255, 0.6);")

        # 完全关闭垂直和水平滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 设置初始最大高度为22
        self.setFixedHeight(22)  

        font = QFont("Microsoft YaHei", 13, QFont.DemiBold)
        self.setFont(font)
        self.setTextColor(QColor(50, 50, 50)) # 设置字体颜色为红色

        self.document().documentLayout().documentSizeChanged.connect(self.adjustHeight)

    def adjustHeight(self):
        doc_height = self.document().size().height()
        self.setFixedHeight(int(doc_height + 10))  # 10是一个额外的边距，可以根据需要调整

def on_key_pressed(event):
    global a
    if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:# 检查是否按下了回车键
        on_button_fasong_clicked()
    else:
        # 保持与之前相同的功能
        QTextEdit.keyPressEvent(text_edit, event)


# 创建一个QTextBrowser的子类来禁用鼠标滚动
class CustomTextBrowser(QTextBrowser):
    def __init__(self,parent=None):
        super().__init__(parent)
        # 设置滚动条策略为始终隐藏
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 使用样式表消除外框和其他样式
        self.setStyleSheet("border: none; background: transparent;color: rgb(85, 45, 82);")
        # 创建一个字体对象，参数分别为字体类型、大小、粗细
        font = QFont("Microsoft YaHei", 13, QFont.DemiBold)
        # 将字体应用到 TextBrowser 对象
        self.setFont(font)

    def wheelEvent(self, event):
        # 通过简单地忽略滚轮事件，我们可以禁用鼠标滚动
        pass

class CustomFrame(QFrame):
    def __init__(self,last_botton,text,touxiang):
        super().__init__()        
        self.last_botton = last_botton
        self.touxiang = touxiang
        # self.setStyleSheet("background-color: black;") # 调试用于染成白色，主容器

        self.label = QLabel(self)
        # 创建新的容器，父对象为自己
        self.new_container = QWidget(self)
        self.new_container.setStyleSheet("background-color: rgba(255, 255, 255, 0.6); border-radius: 10px;")
        # 设定头像
        self.label.setPixmap(QPixmap(touxiang) )

        # 创建CustomTextBrowser实例
        self.text_browser = CustomTextBrowser(self.new_container)
        self.text_browser.setText(text)
        self.text_browser.show()
        

        self.show_event()


        
        # 初始化第一个 QTimer 对象，用于 UI 刷新
        self.timer = QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.show_event)  # 连接到一个名为 'refresh_ui' 的方法
        self.timer.start()



    def show_event(self):      
        # 设置text_browser
        # 获取文本的高度
        document_height = self.text_browser.document().size().height()
        # 将文本高度转换为整数
        document_height = int(document_height)    

        # 设置自己 # 主位置  
        self.setGeometry(0, self.last_botton, container.width(), 20+document_height+30) # 设置位置和大小

        # 设置容器的高度与text_browser的高度相同
        self.new_container.setGeometry(20, 15, self.width() - 80, document_height+30)

        # 设置text_browser 位置大小
        self.text_browser.setGeometry(10, 10, self.new_container.width(), document_height)

        
        self.label.setGeometry(self.width() - image_width - 20, 15, image_width, image_height)

    # 已完成渲染
    def showEvent(self, event):
        super().showEvent(event)
        self.show_event()


    def text_his(self):
        if self.touxiang == "user.png":
            his = "user:" + self.text_browser.toPlainText()
        else:
            his = "you:" + self.text_browser.toPlainText()
        return his
        




# 定义一个函数来检测滑动条的位置,如果true则一直true，如果false则一直false
def check_scrollbar_position(value):
    global scroll11_move
    max_value = scroll11.verticalScrollBar().maximum()

    # 检查滚动条是否在最底部
    if value == max_value:
        scroll11_move = True
    else:
        scroll11_move = False

scroll11 = window.findChild(QScrollArea, 'scrollArea')
scroll11_move = True #默认配置
# 连接滚动条的valueChanged信号到check_scrollbar_position函数
scroll11.verticalScrollBar().valueChanged.connect(check_scrollbar_position)



def scroll111_max_move():
    # 设置滑动栏父级
    container.setMinimumSize(container.minimumSize().width(), custom_widget[0].geometry().bottom() + 20)
    if scroll11_move:
        # 将滚动条的值设置为最大值，从而将其滑动到底部
        scroll11.verticalScrollBar().setValue(scroll11.verticalScrollBar().maximum())

scroll111_max_move_timer = QTimer()
scroll111_max_move_timer.timeout.connect(scroll111_max_move)  # 连接到 'change_interval' 函数
scroll111_max_move_timer.start(10)















# 目标容器
container = window.findChild(QWidget, 'scrollAreaWidgetContents') 

# 设置图片
image_width = 30  # 图片宽度
image_height = 30  # 图片高度



custom_widget = []




custom_widget.insert(0, QWidget())
custom_widget[0].setGeometry(QRect(0, 0, 1, 1))
custom_widget[0].setParent(container)
custom_widget[0].show() # 使 widget 可见
QApplication.processEvents()




#################### 测试用的button
def on_button_clicked():
    global timer1
    last_botton =custom_widget[0].geometry().bottom()
    custom_widget.insert(0, CustomFrame(last_botton=last_botton,text="okkkkkkkkkkkkkkkkkk",touxiang='user.png'))
    custom_widget[0].setParent(container)
    custom_widget[0].show()

    # 初始化第二个 QTimer 对象，用于修改第一个计时器的间隔
    def change_interval1():  # 定义一个函数来改变第一个计时器的间隔
        last_botton = custom_widget[0].geometry().bottom()
        custom_widget.insert(0, CustomFrame(last_botton=last_botton,text="nhhsssssuaghu111111111111111111111",touxiang='gpt.png'))
        custom_widget[0].setParent(container)
        custom_widget[0].show()
        timer1.stop()  # 停止计时器

    timer1 = QTimer()
    timer1.timeout.connect(change_interval1)  # 连接到 'change_interval' 函数
    timer1.start(100)

# button = window.findChild(QPushButton, 'pushButton_4')  # 找到按钮
# # 将按钮的点击事件与上面定义的函数连接
# button.clicked.connect(on_button_clicked)











# 文本编辑器
text_edit = AutoResizingTextEdit()
text_edit_box = window.findChild(QVBoxLayout, 'verticalLayout_9') 
text_edit_box.addWidget(text_edit)
text_edit.keyPressEvent = on_key_pressed
text_edit.show() # 显示 QTextEdit 控件




















def custom_widget_create(text,touxiang):
    global timer1
    last_botton =custom_widget[0].geometry().bottom()
    custom_widget.insert(0, CustomFrame(last_botton=last_botton,text=text,touxiang=touxiang))
    custom_widget[0].setParent(container)
    custom_widget[0].show()
    # time.sleep(100)

def jv_zi_timer_():
    global jv_zi
    # 文字加载
    try:
        if 'a' <= jv_zi[0].lower() <= 'z':
            x = 5
        else:
            x = 1
        custom_widget[0].text_browser.setText(custom_widget[0].text_browser.toPlainText() + jv_zi[:x])

        jv_zi = jv_zi[x:]
    except Exception:
        pass


# custom_widget_create(text,)
# time.sleep(0.1)
# custom_widget_create("")


# vice ui
# global jv_zi
# jv_zi = "句子"
# jv_zi_timer = QTimer()
# jv_zi_timer.timeout.connect(jv_zi_timer_)
# jv_zi_timer.start(500) # 文字加载速度


# 句子播放完成
# jv_zi_timer.stop()
# custom_widget[0].text_browser.setText(custom_widget[0].text_browser.toPlainText() + jv_zi) 





def staream_last_timer_def():
    tokenss_list___all_is_true = True
    for it in staream.tokenss_list:
        if it[2] == False:
            tokenss_list___all_is_true = False

    if tokenss_list___all_is_true == True:
        text = staream.rs()
        global staream_last_timer
        staream_last_timer.stop()
        threading.Thread(target=prompt.msg,args=(text,"语音"), daemon=True).start()
        button_stop_talking.setVisible(True) ##显示停止按钮



staream_last_timer = QTimer()
staream_last_timer.timeout.connect(staream_last_timer_def)
# global staream_last_timer
# staream_last_timer.start(100)




# his = ''
# x0 = False
# for it in custom_widget:
#     if x0 == True:
#         try:
#             his = '\n' + it.text_his() + his
#         except Exception:
#             pass
#     else:
#         x0 = True

# prompt.his = his



######### 大调，只执行job
updata_end_time = time.time()
text_wb_i = 0
def update_1():
    if ui_ci.job != []:
        # print(ui_ci.job[0])
        exec(ui_ci.job[0])
        del ui_ci.job[0]
      


# 使用定时器
timer = QTimer()
timer.timeout.connect(update_1)
timer.start(100)  # 每100毫秒检查一次



# lambda示例
# jv_zi_timer.timeout.connect(lambda: jv_zi_timer_(jv_zi))














########### 语音切换按钮
button_yvyin_qiehuan = window.findChild(QPushButton, "pushButton")

button_fasong = window.findChild(QPushButton, "pushButton_5")

button_set = window.findChild(QPushButton, "pushButton_2")

def on_button_fasong_yvyin_clicked():
    if ui_ci.text_start__yun_xv:
        if not staream.start_ing:  # 开始录音
            staream.start_ing__start()
            button_fasong.setText("发送")
            button_yvyin_qiehuan.setHidden(True)
        else:                      # 结束录音
            staream.start_ing__close()
            button_fasong.setText("speek")
            button_yvyin_qiehuan.setHidden(False)

moshi = "文本模式"
def on_button_fasong_yvyin_qiehuan_clicked():
    global moshi
    if moshi == "文本模式": #文本转语音
        moshi = "语音模式"
        button_fasong.clicked.disconnect()
        button_fasong.clicked.connect(on_button_fasong_yvyin_clicked)
        button_fasong.setText("speek")
        text_edit.setHidden(True)
        button_yvyin_qiehuan.setText("切换文本模式")

        
    else:                 # 语音转文本
        moshi = "文本模式" 
        button_fasong.clicked.disconnect()
        button_fasong.clicked.connect(on_button_fasong_clicked)
        button_fasong.setText("发送")
        text_edit.setHidden(False)
        button_yvyin_qiehuan.setText("切换语音模式")
        



# 启动线程，传参text，清除当前的文本ui
def on_button_fasong_clicked():
    text = text_edit.toPlainText()  # 获取当前文本
    if text == "":
            print("文本为空")
    else:
        if ui_ci.text_start__yun_xv:
            # 启动线程，传参text，
            threading.Thread(target=prompt.msg,args=(text,"文本",), daemon=True).start()
            button_stop_talking.setVisible(True) ##显示停止按钮
            # 清除当前的文本ui
            text_edit.clear()               # 清空文本
            QApplication.processEvents()


def on_button_set_clicked():
    threading.Thread(target=set.sockett, daemon=True).start()

# 将功能与按钮的点击事件关联
button_fasong.clicked.connect(on_button_fasong_clicked)


button_yvyin_qiehuan.clicked.connect(on_button_fasong_yvyin_qiehuan_clicked)

button_set.clicked.connect(on_button_set_clicked)









button_stop_talking = window.findChild(QPushButton, 'pushButton_4')

button_stop_talking.setVisible(False) # 不显示停止按钮
def button_stop_talking_clicked():
    prompt.stop__[len(prompt.stop__) - 1] = True
    button_stop_talking.setVisible(False)


button_stop_talking.clicked.connect(button_stop_talking_clicked)





















####### 快捷键
class SignalHandler(QtCore.QObject):
    signal_on_button_fasong_clicked = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.signal_on_button_fasong_clicked.connect(on_button_fasong_clicked)

def signal_on_button_fasong():
    handler.signal_on_button_fasong_clicked.emit()

handler = SignalHandler()

keyboard.add_hotkey("u+i", signal_on_button_fasong)



sys.exit(app.exec_())






# def update_2():
#     pass


# # 使用定时器
# timer_ui = QTimer()
# timer_ui.timeout.connect(update_2)
# timer_ui.start(100)  # 每100毫秒检查一次