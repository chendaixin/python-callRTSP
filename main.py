
import sys
import os
import time

THIRD_LIB_PATH = os.getcwd() + '\\third_libs'
if THIRD_LIB_PATH not in sys.path:
    sys.path.append(THIRD_LIB_PATH)
import vlc
from multiprocessing import Process

import logging


# 创建一个日志器logger
class logFrame:

    def getlogger(self):
        self.logger = logging.getLogger("logger")
        # 判断是否有处理器，避免重复执行
        if not self.logger.handlers:
            # 日志输出的默认级别为warning及以上级别，设置输出info级别
            self.logger.setLevel(logging.DEBUG)

            # 创建一个处理器handler  StreamHandler()控制台实现日志输出
            sh = logging.StreamHandler()
            # 创建一个格式器formatter  （日志内容：当前时间，文件，日志级别，日志描述信息）
            formatter = logging.Formatter(fmt="当前时间是%(asctime)s,文件是%(filename)s,行号是%(lineno)d，日志级别是%(levelname)s，"
                                              "描述信息是%(message)s", datefmt="%Y/%m/%d %H:%M:%S")
            # 关联控制台日志器—处理器—格式器
            self.logger.addHandler(sh)
            sh.setFormatter(formatter)
            # 设置处理器输出级别
            sh.setLevel(logging.DEBUG)

            '''
            # 创建一个文件处理器，文件写入日志
            fh = logging.FileHandler(
                filename="./{}_log.txt".format(time.strftime("%Y_%m_%d %H_%M_%S", time.localtime())), encoding="utf8")
            # 创建一个文件格式器f_formatter
            f_formatter = logging.Formatter(fmt="当前时间是%(asctime)s,文件是%(filename)s,行号是%(lineno)d，日志级别是%(levelname)s，"
                                                "描述信息是%(message)s", datefmt="%Y/%m/%d %H:%M:%S")
            # 关联文件日志器-处理器-格式器
            self.logger.addHandler(fh)
            fh.setFormatter(f_formatter)
            # 设置处理器输出级别
            fh.setLevel(logging.DEBUG)
            '''
        return self.logger


def get_loger():
    log = logFrame()
    return log.getlogger()


logger = get_loger()


class Player:
    '''
        args:设置 options
    '''
    def __init__(self, *args):
        if args:
            instance = vlc.Instance(*args)
            self.media = instance.media_player_new()
        else:
            self.media = vlc.MediaPlayer()

    # 设置待播放的url地址或本地文件路径，每次调用都会重新加载资源
    def set_uri(self, uri):
        self.media.set_mrl(uri)

    # 播放 成功返回0，失败返回-1
    def play(self, path=None):
        if path:
            self.set_uri(path)
            return self.media.play()
        else:
            return self.media.play()

    # 暂停
    def pause(self):
        self.media.pause()

    # 恢复
    def resume(self):
        self.media.set_pause(0)

    # 停止
    def stop(self):
        self.media.stop()

    # 释放资源
    def release(self):
        return self.media.release()

    # 是否正在播放
    def is_playing(self):
        return self.media.is_playing()

    # 已播放时间，返回毫秒值
    def get_time(self):
        return self.media.get_time()

    # 拖动指定的毫秒值处播放。成功返回0，失败返回-1 (需要注意，只有当前多媒体格式或流媒体协议支持才会生效)
    def set_time(self, ms):
        return self.media.get_time()

    # 音视频总长度，返回毫秒值
    def get_length(self):
        return self.media.get_length()

    # 获取当前音量（0~100）
    def get_volume(self):
        return self.media.audio_get_volume()

    # 设置音量（0~100）
    def set_volume(self, volume):
        return self.media.audio_set_volume(volume)

    # 返回当前状态：正在播放；暂停中；其他
    def get_state(self):
        state = self.media.get_state()
        if state == vlc.State.Playing:
            return 1
        elif state == vlc.State.Paused:
            return 0
        else:
            return -1

    # 当前播放进度情况。返回0.0~1.0之间的浮点数
    def get_position(self):
        return self.media.get_position()

    # 拖动当前进度，传入0.0~1.0之间的浮点数(需要注意，只有当前多媒体格式或流媒体协议支持才会生效)
    def set_position(self, float_val):
        return self.media.set_position(float_val)

    # 获取当前文件播放速率
    def get_rate(self):
        return self.media.get_rate()

    # 设置播放速率（如：1.2，表示加速1.2倍播放）
    def set_rate(self, rate):
        return self.media.set_rate(rate)

    # 设置宽高比率（如"16:9","4:3"）
    def set_ratio(self, ratio):
        self.media.video_set_scale(0)  # 必须设置为0，否则无法修改屏幕宽高
        self.media.video_set_aspect_ratio(ratio)

    # 注册监听器
    def add_callback(self, event_type, callback):
        self.media.event_manager().event_attach(event_type, callback)

    # 移除监听器
    def remove_callback(self, event_type, callback):
        self.media.event_manager().event_detach(event_type, callback)


def my_call_back(event):
    print("call:", player.get_time())
    return


def process_work(name):

    logger.info('%s, begin', name)
    player = Player()
    #player.add_callback(vlc.EventType.MediaPlayerTimeChanged, my_call_back)
    # 在线播放流媒体视频
    player.play("rtsp://192.168.31.18:8554/mystream")

    time.sleep(60)

    player.stop()
    logger.info('%s, over', name)
    return


if __name__ == '__main__':
    process_list = list()
    for i in range(100):
        arg_str = 'Process[%s]' % (i,)
        p = Process(target=process_work, args=(arg_str,) )
        process_list.append(p)

    for p in process_list:
         p.start()

    for p in process_list:
         p.join()

# if __name__ == '__main__':
#     print('PyCharm')
#     player = Player()
#     player.add_callback(vlc.EventType.MediaPlayerTimeChanged, my_call_back)
#     # 在线播放流媒体视频
#     player.play("rtsp://192.168.0.84:8554/mystream")
#
#     # 播放本地mp3
#     # player.play("D:/abc.mp3")
#
#     # 防止当前进程退出
#     while True:
#         pass




