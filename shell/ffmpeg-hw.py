#!/usr/bin/python
# -*- coding: UTF-8 -*-

import subprocess
import os
import sys
import time

if __name__ == '__main__':
    _cwd, filename = os.path.split(
        os.path.abspath(os.path.realpath(sys.argv[0])))
    os.chdir(_cwd)

    ffmpeg_shell = "ffmpeg" if os.sys.platform == "win32" else "./ffmpeg"
    null_file = "NUL" if os.sys.platform == "win32" else "/dev/null"

    srcFile = "input.mp4"
    bit_rate = 2000
    with open("ffmpeg.stdout",mode="w") as out:
        # HWACCEL解码测试
        _fastest_decoder = ''
        _fastest_decoder_time = float('inf')

        _available_decoders = []
        _available_encoders = []

        for hw in ["dxva2","d3d11va","cuda","cuvid","qsv","opencl","vulkan","videotoolbox"]:
            _cmd = [ffmpeg_shell,"-hwaccel", hw,"-i", srcFile,"-f","null", null_file]
            if hw == "qsv":
                _cmd.insert(3,"-c:v")
                _cmd.insert(4,"h264_qsv")
            if hw == "cuvid":
                _cmd.insert(3,"-c:v")
                _cmd.insert(4,"h264_cuvid")
        
            _start = time.time()
            ret = subprocess.run(_cmd, cwd=_cwd,stderr = out,stdout = out)
            _end = time.time()
            _t = _end - _start
            print( "{}".format(' '.join(_cmd)))
            if ret.returncode != 0:
                print("\033[0;31m{:>10} hwaccel decoder not supported \033[0m".format(hw))
                continue
            if _t < _fastest_decoder_time:
                _fastest_decoder = hw
                _fastest_decoder_time = _t

            _available_decoders.append(hw)
            print("{:>10} hwaccel decoder spent = \033[1;32m {:.2f} s \033[0m".format(hw , _t))

        print("\n--------")
        print("fastest hwaccel decoder is \033[0;32m {} \033[0m , spent = {:.2f} s \033[0m".format(_fastest_decoder , _fastest_decoder_time))
        print("--------")

        # 检测可用的编码器
        for _encoder in ["h264_nvenc","h264_qsv","h264_amf","h264_videotoolbox"]:
            _cmd = [ffmpeg_shell,"-i", srcFile,"-f","mp4","-c:v", _encoder ,"-y", null_file]
            ret = subprocess.run(_cmd, cwd=_cwd,stderr = out,stdout = out,timeout=2000)
            if ret.returncode == 0:
                _available_encoders.append(_encoder)
        
        print("available_decoders is \033[0;32m {} \033[0m".format( " | ".join(_available_decoders) ))
        print("available_encoders is \033[0;32m {} \033[0m".format( " | ".join(_available_encoders) ))

        for hw in _available_decoders:
            for encoder in _available_encoders:
                _cmd = [ffmpeg_shell,"-hwaccel", hw ,"-i", srcFile,"-f","mp4", '-c:v', encoder, '-b:v', '{}k'.format(bit_rate), "-y", null_file]
                if hw == 'cuda' and encoder == 'h264_nvenc':
                    # _cmd.insert(3,"-hwaccel_output_format")
                    # _cmd.insert(4,"cuda")
                    # _cmd.insert(1,"-hwaccel_device")
                    # _cmd.insert(2,"0")
                    pass
                elif hw == 'cuvid':
                    _cmd[1] = '-c:v'
                    _cmd[2] = 'h264_cuvid'
                elif hw == 'qsv':
                    _cmd[1] = '-c:v'
                    _cmd[2] = 'h264_qsv'
                
                _start = time.time()
                ret = subprocess.run(_cmd, cwd=_cwd,stderr = out,stdout = out)
                _end = time.time()
                print( "{}".format(' '.join(_cmd)) )
                if ret.returncode != 0:
                    print("{:>10} decoder | {:>10} encoder not supported".format(hw , encoder))
                    continue
                
                print("{:>10} decoder | {:>10} encoder spent = {:.2f} s".format(hw , encoder , _end - _start))
        
        # cpu 解码和编码
        print( "-------- CPU encoder|decoder Start --------" )
        _cmd = [ffmpeg_shell,"-i", srcFile,"-f","mp4", '-c:v', "libx264", '-b:v', '{}k'.format(bit_rate), "-y", null_file]
        _start = time.time()
        subprocess.run(_cmd, cwd=_cwd,stderr = out,stdout = out)
        _end = time.time()
        print( "{}".format(' '.join(_cmd)) )
        print("{:>10} decoder | {:>10} encoder spent = {:.2f} s".format('h264 cpu' , "libx264" , _end - _start))
        print( "-------- CPU encoder|decoder END --------" )

        exit()