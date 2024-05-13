from faster_whisper import WhisperModel
from io import BytesIO
import typing
import io
import collections
import wave
import time
import threading

import pyaudio
import webrtcvad
import logging
import ui_ci




whisper_locality_model = ""
whisper_device = ""
whisper_compute_type = ""


#解决bug问题
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"


logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(levelname)s - %(message)s')

# #实现标点符号的添加
# model1 = AutoModel(model="E:\ct-punc")
class Transcriber(object):
    def __init__(self,
                 prompt: str = '实时/低延迟语音转写服务"'
                 ) -> None:



        self.prompt = prompt

    def __enter__(self) -> 'Transcriber':
        global whisper_locality_model
        global whisper_device
        global whisper_compute_type
        self._model = WhisperModel(whisper_locality_model, device=whisper_device, compute_type=whisper_compute_type)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    def __call__(self, audio: bytes) -> typing.Generator[str, None, None]:
        segments, info = self._model.transcribe(BytesIO(audio),
                                               initial_prompt=self.prompt,vad_filter=True)
        # print(info.language)
        # if info.language != "zh" or info.language != "en":
        #     # return {"error": "语音错误"}
        #     print("语音错误")
        res_all = ""
        for segment in segments:
            t = segment.text

            # res1 = model1.generate(input=t)
            res_all = res_all + t
        if res_all.strip().replace('.', ''):
            yield res_all



class AudioRecorder(object):
    """ Audio recorder.
    Args:
        channels (int, 可选): 通道数，默认为1（单声道）。
        rate (int, 可选): 采样率，默认为16000 Hz。
        chunk (int, 可选): 缓冲区中的帧数，默认为256。
        frame_duration (int, 可选): 每帧的持续时间（单位：毫秒），默认为30。
    """

    def __init__(self,
                 channels: int = 1,
                 sample_rate: int = 16000,
                 chunk: int = 256,
                 frame_duration: int = 30) -> None:
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk = chunk
        self.frame_size = (sample_rate * frame_duration // 1000)
        self.__frames: typing.List[bytes] = []

    def __enter__(self) -> 'AudioRecorder':
        self.vad = webrtcvad.Vad()
        # 设置 VAD 的敏感度。参数是一个 0 到 3 之间的整数。0 表示对非语音最不敏感，3 最敏感。
        self.vad.set_mode(0)

        self.audio = pyaudio.PyAudio()
        self.sample_width = self.audio.get_sample_size(pyaudio.paInt16)
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=self.channels,
                                      rate=self.sample_rate,
                                      input=True,
                                      frames_per_buffer=self.chunk)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def __bytes__(self) -> bytes:
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.sample_width)
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.__frames))
            self.__frames.clear()
        return buf.getvalue()

    def __iter__(self):
        global start_ing
        """ Record audio until silence is detected.
        """
        MAXLEN = 30
        watcher = collections.deque(maxlen=MAXLEN)
        triggered, ratio = False, 0.5
        while True:
            frame = self.stream.read(self.frame_size)
            is_speech = self.vad.is_speech(frame, self.sample_rate)
            watcher.append(is_speech)
            self.__frames.append(frame)
            if not triggered:
                num_voiced = len([x for x in watcher if x])
                if num_voiced > ratio * watcher.maxlen and start_ing == True:
                    logging.info("start recording...")
                    triggered = True
                    watcher.clear()
                    self.__frames = self.__frames[-MAXLEN:]
            else:
                num_unvoiced = len([x for x in watcher if not x])
                if num_unvoiced > ratio * watcher.maxlen or start_ing == False:
                    logging.info("stop recording...")
                    triggered = False
                    yield bytes(self)



def gett(audio,transcriber,i):
    global tokenss_list
    for seg in transcriber(audio): # 可能没有切片
        tokenss_list[i][1] += seg
    tokenss_list[i][2] = True
    # print(seg)
    rs()

def main():
    global l
    global window
    try:
        with AudioRecorder(channels=1, sample_rate=16000) as recorder:
            # print("加载完成")
            with Transcriber() as transcriber:  #选择本地的large-v3
                print("加载完成")
                ui_ci.job.append("window.show()")
                for audio in recorder:
                    # print("audio")
                    tokenss_list.append([l,"",False])
                    threading.Thread(target=gett,args=(audio,transcriber,l,)).start()
                    l += 1
                    # for seg in transcriber(audio):
                    #     print(seg)


    except KeyboardInterrupt:
        print("KeyboardInterrupt: terminating...")
    except Exception as e:
        print(e)

start_ing = False


def rs():
    global tokenss_list
    tokens = ""
    for it in tokenss_list:
        tokens += " "
        tokens += it[1]
    # print("re::::::::",tokens)
    
    ############## 更新ui text  // f'custom_widget[0].text_browser.setText("""{tokens}""")'
    ui_ci.job.append(f'custom_widget[0].text_browser.setText("""{tokens}""")')
    return tokens

tokenss_list = []
l = 0
def start_ing__start():
    global tokenss_list
    global l
    global start_ing
    tokenss_list = []
    l = 0
    start_ing = True

    ########### 更新一个容器  //custom_widget_create("")
    ui_ci.job.append("custom_widget_create('','user.png')")

def start_ing__close():
    global start_ing
    start_ing = False

    ui_ci.text_start__yun_xv = False

    ############# 添加一个timer ，每100ms，如果tokenss_list[it][2] all为true，则tokens = rs(),关闭timer，运行msg(tokens) //

    ui_ci.job.append(f"""global staream_last_timer
staream_last_timer.start(100)""")


# while True:
    
#     if input("input ") == "1":
#         tokenss_list = []
#         l = 0
#         start_ing = True
        
#     else:
#         start_ing = False

#     print(start_ing)

