import openai
import threading
import time
import io
from pydub import AudioSegment
from pydub.playback import play
import ui_ci



openai_api_key = ""
openai_api_base_url = ""
chat_model = ""
openai_voice_model = ""
init_prompt = ""

def set_():
    global client
    client = openai.OpenAI(api_key=openai_api_key,base_url=openai_api_base_url)

audio_cache_list = []

def extract_segment(a):
    punctuations = ['!', '?', '.', '。', ',', '，', '！', '？', ':', '：']

    end_pos = []
    for i in range(len(a)):
        for po in punctuations:
            if po == a[i]:
                end_pos.append(i+1)

    n = len(end_pos)
    # 冒泡排序
    for i in range(n):
        
        # 标记某一轮是否发生了交换
        swapped = False
        
        # 最后 i 个元素已经排好序,无需再比较
        for j in range(0, n-i-1):
            
            # 如果当前元素大于下一个元素,交换它们
            if end_pos[j] > end_pos[j+1]:
                end_pos[j], end_pos[j+1] = end_pos[j+1], end_pos[j]
                swapped = True
        
        # 如果某一轮没有发生交换,说明数组已经有序,直接退出
        if not swapped:
            break

    # print(end_pos)

    end = None
    segment = []
    for pos in end_pos:
        # print(pos)
        segment.append(a[:pos][end:])
        end = pos

    a = a[end:]

    return segment,a




def play_cache():
    global audio_cache_list
    global stop__    #暂停用                 # 该函数只读stop__[last index]，
    global i         #播放完成后暂停用
    global l         #记录播放位置
    while True:
        try:
            if audio_cache_list[l][3] == True:
                # ui    audio_cache_list[0][1]
                ui_ci.job.append(f"""global jv_zi
global jv_zi_timer
"""+f'jv_zi = """{audio_cache_list[l][1]}"""'+"""
jv_zi_timer = QTimer()
jv_zi_timer.timeout.connect(jv_zi_timer_)
jv_zi_timer.start(200)""")
                play(audio_cache_list[l][0])
                ui_ci.job.append(f"""global jv_zi_timer
jv_zi_timer.stop()
custom_widget[0].text_browser.setText(custom_widget[0].text_browser.toPlainText() + jv_zi) """)
                
                l += 1
                if l >= i:
                    ui_ci.text_start__yun_xv = True
                    audio_cache_list = []
                    ui_ci.job.append("button_stop_talking.setVisible(False)")
 

                # del audio_cache_list[0]
                time.sleep(0.5) # 换气sleep
        except IndexError:
            time.sleep(0.1) # 巡查sleep

        try:
            if stop__[len(stop__) - 1] == True:
                ui_ci.text_start__yun_xv = True
                audio_cache_list = []
        except IndexError:
            pass


def vice(input_s,nub,index):
    global openai_voice_model
    global audio_cache_list 
    global stop__   # 该函数读number[index]，

    # print("input_s",input_s)
    # s = input_s

    if stop__[index] == False:
        # Call the OpenAI API to convert text to speech
        response = client.audio.speech.create(
            model="tts-1",
            voice=openai_voice_model,
            input=input_s
        )

        # 将字节流转换为 BytesIO 对象
        audio_bytes = io.BytesIO(response.content)

        # 使用 AudioSegment.from_file() 从字节流中加载音频数据
        new_audio = AudioSegment.from_file(audio_bytes, format="mp3")

    if stop__[index] == False:
        audio_cache_list[nub][0] = new_audio
        audio_cache_list[nub][3] = True

    # while True:
    #     if nub == l:
    #         # audio_cache_list.append([new_audio,s])
            
    #         l += 1
    #         break

    #     time.sleep(0.5)

l = 0
stop__ = []

def msg(input_,mod):
    global chat_model
    global l
    global i
    global audio_cache_list
    global init_prompt
    ui_ci.text_start__yun_xv = False
    if mod == "文本":
        ui_ci.job.append(f'custom_widget_create("""{input_}""","user.png")')
        time.sleep(0.1)

    his = chat_history()
    ui_ci.job.append("custom_widget_create('','gpt.png')")

    response = client.chat.completions.create(
        model=chat_model,
        messages=[
            {"role": "system", "content": f"{init_prompt}"},
            {"role": "system", "content": f"\n{his}\nuser:{input_}\nyou:"}
        ],
        stream=True
    )

    tokens = ""
    i = 0
    l = 0
    audio_cache_list = []
    stop__.append(False)
    index_ = len(stop__) - 1

    for line in response:
        for choice in line.choices:
            delta = choice.delta
            if delta.content is not None:
                # print(delta.content, end='', flush=True)
                tokens += delta.content
                segment_list,tokens = extract_segment(tokens)
                for it in segment_list:
                    audio_cache_list.append(["new_audio",it,i,False])
                    threading.Thread(target=vice,args=(it,i,index_,), daemon=True).start()
                    i += 1


his = None
def chat_history():
    global his
    his = None
    # 传入job
    ui_ci.job.append(r"""his = ''
x0 = False
for it in custom_widget:
    if x0 == True:
        try:
            his = '\n' + it.text_his() + his
        except Exception:
            pass
    else:
        x0 = True

prompt.his = his""")

    while True:
        if his or his == "":
            # print(his)
            # print(his)
            break
        else:
            time.sleep(0.1)

    return his






threading.Thread(target=play_cache, daemon=True).start()