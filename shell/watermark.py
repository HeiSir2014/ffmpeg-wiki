import subprocess
import os
import sys
import json

if __name__ == '__main__':

    ## make slient.pcm
    # with open("slient.pcm",mode="wb") as f:
    #     for i in range(48000):
    #         f.write(b'\0\0\0\0')
    # exit()

    srcDir = sys.argv[len(sys.argv) - 1]
    # srcDir = 'video\\'
    srcDir = (os.path.dirname(srcDir) if srcDir.endswith('\\') else srcDir)
    if not (os.path.exists(srcDir) and os.path.isdir(srcDir)):
        print("{} 目录不存在，或者不是一个目录".format(srcDir))
        exit(0)

    dstDir = srcDir + '-watermark'
    not os.path.exists(dstDir) and os.mkdir(dstDir)
    files = os.listdir(srcDir)

    num = -1
    while (num <= 0 or num >= 10):
        print('''----\t批 量 添 加 水 印\t----
----\t检测到 {} 个文件\t----
* 请在当前目录放置图片水印文件：watermark.png
* 如果需要加背景音乐，请放置音乐文件：bkg.mp3

* 请输入以下水印放置位置得序号
---- 静态 ----
[1] 左上角
[2] 右上角
[3] 右下角
[4] 左下角
---- 运动 ----
[5] 左上 -> 右上
[6] 左上 -> 右下
[7] 左下 -> 右下
[8] 左下 -> 右上
---- 控制 ----
按 Q / q 键退出。

'''.format(len(files)))
        num = int(input('序号：'), 10)
        print(num)
        if num == 'q' or num == 'Q':
            exit()

    vfStr = None
    if num == 1:
        vfStr = "movie=watermark.png[logo];[in][logo]overlay=x='10':y='10'"
    elif num == 2:
        vfStr = "movie=watermark.png[logo];[in][logo]overlay=x='W-w-10':y='10'"
    elif num == 3:
        vfStr = "movie=watermark.png[logo];[in][logo]overlay=x='W-w-10':y='H-h-10'"
    elif num == 4:
        vfStr = "movie=watermark.png[logo];[in][logo]overlay=x='10':y='H-h-10'"
    elif num == 5:
        vfStr = "movie=watermark.png[logo];[in][logo]overlay=x='mod(t*W/30,W)':y='10'"
    elif num == 6:
        vfStr = "movie=watermark.png[logo];[in][logo]overlay=x='mod(t*W/30,W)':y='mod(t*H/30,H)'"
    elif num == 7:
        vfStr = "movie=watermark.png[logo];[in][logo]overlay=x='mod(t*W/30,W)':y=H-h-10"
    elif num == 8:
        vfStr = "movie=watermark.png[logo];[in][logo]overlay=x='mod(t*W/30,W)':y='H-mod(t*H/30,H)'"

    if vfStr is None:
        exit()

    #  跑马灯效果 隔30秒显示30秒
    vfStr += ":enable='lt(mod(t,60),30)'"
    _cwd, filename = os.path.split(
        os.path.abspath(os.path.realpath(sys.argv[0])))
    os.chdir(_cwd)
    if os.path.exists('bkg.mp3') or os.path.exists('bkg.wav') or os.path.exists('bkg.m4a'):
        bkg = 'bkg.mp3' if os.path.exists('bkg.mp3') else (
            'bkg.wav' if os.path.exists('bkg.wav') else 'bkg.m4a')
        
        out = 'bkg_out.wav'
        if not os.path.exists(out):
            start = int(input("\n背景音乐起始时间(秒)："))
            space = int(input("\n背景音乐播放完毕停顿时间(秒)："))
            num = int(input("\n背景音乐播放次数："))
            inputWav = 'bkg_input.wav'
            with open("list.txt", "w") as fo:
                for i in range(start):
                    fo.write('file \'slient.wav\'\n')
                for i in range(num):
                    fo.write('file \'{}\'\n'.format(inputWav))
                    for i in range(space): 
                        fo.write('file \'slient.wav\'\n')
                fo.close()
            # 转换不同格式的背景音乐 统一Wav 短整数 | 48k | 双声道格式
            subprocess.run(["ffmpeg.exe", "-i",
                           bkg,"-f","wav","-acodec", "pcm_s16le","-ar","48000","-ac","2", "-y", inputWav], cwd=_cwd)
            subprocess.run(["ffmpeg.exe", "-f", "concat", "-i",
                           "list.txt", "-y", out], cwd=_cwd)
            os.remove("list.txt")
            os.remove("bkg_input.wav")

    for file in files:
        bit_rate = 2048
        with open("probe.log", mode="w+", encoding='utf-8') as probe:
            subprocess.run(["ffprobe.exe", "-show_format", "-print_format", "json","{}\\{}".format(srcDir, file)], cwd=_cwd, stdout= probe)
            probe.close()
        with open("probe.log", mode="r", encoding='utf-8') as probe:
            _data= json.load(probe,)
            bit_rate = int(int(_data['format']['bit_rate']) / 1000) + 100
            probe.close()
            os.path.exists("probe.log") and os.remove("probe.log")

        print(" * '{}\\{}' bitrate is {}k\n".format(srcDir, file, bit_rate))

        if os.path.exists('bkg.mp3') or os.path.exists('bkg.wav') or os.path.exists('bkg.m4a'):
            bkg= 'bkg.mp3' if os.path.exists('bkg.mp3') else ('bkg.wav' if os.path.exists('bkg.wav') else 'bkg.m4a')
            out = 'bkg_out.wav'
            # '-shortest',
            subprocess.run(["ffmpeg.exe", "-hwaccel", "dxva2", "-i", "{}\\{}".format(srcDir, file), "-i", out, 
             "-vf", vfStr, '-filter_complex', '[0:a][1:a]amix', '-c:v', 'h264_qsv', '-b:v', '{}k'.format(bit_rate), "-y", "{}\\{}".format(dstDir, file)], cwd=_cwd)
        else:
            subprocess.run(["ffmpeg.exe", "-hwaccel", "dxva2", "-i", "{}\\{}".format(srcDir, file), "-vf", vfStr, '-c:v',
                           'h264_qsv', '-c:a', 'copy', '-b:v', '{}k'.format(bit_rate), "-y", "{}\\{}".format(dstDir, file)], cwd=_cwd)
