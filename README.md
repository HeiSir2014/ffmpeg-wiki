# ffmpeg-wiki
FFmpeg Command wiki

## HWAccel 硬件加速相关

[FFmpeg HWAccel](https://trac.ffmpeg.org/wiki/HWAccelIntro)

1. 枚举 ffmpeg 硬件加速能力
    ```bash
    ffmpeg -hwaccels
    ```
    >   Hardware acceleration methods:
        cuda
        dxva2
        qsv
        d3d11va
        opencl
        vulkan

    查看支持的所有编码器
    ```bash
    ffmpeg -encoders
    ```

    查看支持的所有解码器
    ```bash
    ffmpeg -decoders
    ```

2. 使用以上这些hw硬解视频，测试一个1分钟的MP4文件解码和编码。
    显卡：NVIDIA GTX1660ti
    CPU：Intel(R) Core(TM) i5-9400 CPU @ 2.90GHz
    系统：Win10

    ---
    <center>单纯解码测试</center>

    ```bash
    ffmpeg.exe -hwaccel dxva2 -i input.mp4 -f null -
    ```
    > dxva2 hwaccel spent = 5.09 s

    ```bash
    ffmpeg.exe -hwaccel d3d11va -i input.mp4 -f null -
    ```
    > d3d11va hwaccel spent = 5.62 s

    ```bash
    ffmpeg.exe -hwaccel cuda -i input.mp4 -f null -
    ```
    > cuda hwaccel spent = 4.35 s

    ```bash
    ffmpeg.exe -hwaccel cuvid -i input.mp4 -f null -
    ```
    > cuvid hwaccel spent = 3.50 s

    ```bash
    ffmpeg.exe -hwaccel qsv -i input.mp4 -f null -
    ```
    > qsv hwaccel spent = 2.29 s

    ```bash
    ffmpeg.exe -hwaccel opencl -i input.mp4 -f null -
    ```
    > opencl hwaccel spent = 2.55 s
    
    ```bash
    ffmpeg.exe -hwaccel vulkan -i input.mp4 -f null -
    ```
    > vulkan hwaccel spent = 3.09 s
    
    | HWAccell  | TimeSpent(s)  |
    |   -       |   -           |
    | dxva2     | 5.09          |
    | d3d11va   | 5.62          |
    | cuda      | 4.35          |
    | cuvid     | 3.50          |
    | qsv       | 2.29          |
    | opencl    | 2.55          |
    | vulkan    | 3.09          |

    ---
    <center>硬解 + 硬编测试</center>
    
    ```bash
    ffmpeg.exe -hwaccel dxva2 -i input.mp4 -f mp4 -c:v h264_nvenc -b:v 2000k -y NUL
    ```

    > dxva2 decoder | h264_nvenc encoder spent = 8.04 s

    ```bash
    ffmpeg.exe -hwaccel d3d11va -i input.mp4 -f mp4 -c:v h264_nvenc -b:v 2000k -y NUL
    ```

    > d3d11va decoder | h264_nvenc encoder spent = 8.66 s

    ```bash
    ffmpeg.exe -hwaccel cuda -i input.mp4 -f mp4 -c:v h264_nvenc -b:v 2000k -y NUL
    ```

    > cuda decoder | h264_nvenc encoder spent = 7.27 s

    ```bash
    ffmpeg.exe -c:v h264_cuvid -i input.mp4 -f mp4 -c:v h264_nvenc -b:v 2000k -y NUL
    ```

    > cuvid decoder | h264_nvenc encoder spent = 5.79 s

    ```bash
    ffmpeg.exe -hwaccel qsv -i input.mp4 -f mp4 -c:v h264_nvenc -b:v 2000k -y NUL
    ```

    > qsv decoder | h264_nvenc encoder spent = 5.78 s
    
    ```bash
    ffmpeg.exe -hwaccel opencl -i input.mp4 -f mp4 -c:v h264_nvenc -b:v 2000k -y NUL
    ```

    > opencl decoder | h264_nvenc encoder spent = 5.89 s
    
    ```bash
    ffmpeg.exe -hwaccel vulkan -i input.mp4 -f mp4 -c:v h264_nvenc -b:v 2000k -y NUL
    ```

    > vulkan decoder | h264_nvenc encoder spent = 6.36 s

    ```bash
    ffmpeg.exe -hwaccel qsv -i input.mp4 -f mp4 -c:v libx264 -b:v 2000k -y NUL
    ```

    > qsv decoder |    libx264 encoder spent = 40.62 s

    ```bash
    ffmpeg.exe -i input.mp4 -f mp4 -c:v libx264 -b:v 2000k -y NUL
    ```

    > h264 cpu |    libx264 encoder spent = 40.36 s

    | HWAccell  | encoder | TimeSpent(s)  |
    |   -       |   -           |   -           |
    | dxva2     |  h264_nvenc | 5.09          |
    | d3d11va   |  h264_nvenc | 5.62          |
    | cuda      |  h264_nvenc | 7.27          |
    | cuvid     |  h264_nvenc | 5.79          |
    | `qsv`       |  `h264_nvenc` | `5.78`          |
    | opencl    |  h264_nvenc | 5.89          |
    | vulkan    |  h264_nvenc | 6.36          |
    | qsv       |  libx264 | 40.62          |
    | h264 cpu  |  libx264 | 40.36          |

    > 硬解测试 Python脚本 [Python3]
    [ffmpeg-hw.py](./shell/ffmpeg-hw.py)


## 视频添加图片水印和背景音乐

添加图片水印主要使用的video filter的功能，参考：[FilteringGuide](https://trac.ffmpeg.org/wiki/FilteringGuide)

> Python脚本 [Python3]
[ffmpeg-hw.py](./shell/watermark.py)

