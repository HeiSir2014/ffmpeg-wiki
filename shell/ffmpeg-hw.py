import subprocess
import os
import sys
import time

if __name__ == '__main__':
    _cwd, filename = os.path.split(
        os.path.abspath(os.path.realpath(sys.argv[0])))
    os.chdir(_cwd)
    srcFile = "input.mp4"
    bit_rate = 2000
    with open("ffmpeg.stdout",mode="w") as out:
        # HWACCEL解码测试
        for hw in ["dxva2","d3d11va","cuda","cuvid","qsv","opencl","vulkan"]:
            _cmd = ["ffmpeg","-hwaccel", hw,"-i", srcFile,"-f","null","-"]
            _start = time.time()
            subprocess.run(_cmd, cwd=_cwd,stderr = out,stdout = out)
            _end = time.time()
            print( "{}".format(' '.join(_cmd)) )
            print("{:>10} hwaccel decoder spent = {:.2f} s".format(hw , _end - _start))

        for hw in ["dxva2","d3d11va","cuda", "cuvid","qsv","opencl","vulkan"]:
            #['nvenc','qsv','videotoolbox'] mac 平台
            for encoder in ['nvenc','libx264']:
                if encoder == 'libx264' and hw != 'qsv':
                    continue
                encoder = ("h264_" + encoder) if encoder != 'libx264' else encoder
                _cmd = ["ffmpeg","-hwaccel", hw ,"-i", srcFile,"-f","mp4", '-c:v', encoder, '-b:v', '{}k'.format(bit_rate), "-y","NUL"]
                if hw == 'cuda' and encoder == 'h264_nvenc':
                    # _cmd.insert(3,"-hwaccel_output_format")
                    # _cmd.insert(4,"cuda")
                    # _cmd.insert(1,"-hwaccel_device")
                    # _cmd.insert(2,"0")
                    pass
                elif hw == 'cuvid':
                    _cmd[1] = '-c:v'
                    _cmd[2] = 'h264_cuvid'
                _start = time.time()
                subprocess.run(_cmd, cwd=_cwd,stderr = out,stdout = out)
                _end = time.time()
                print( "{}".format(' '.join(_cmd)) )
                if _end - _start < 1.5:
                    print("{:>10} decoder | {:>10} encoder not supported".format(hw , encoder))
                    continue
                print("{:>10} decoder | {:>10} encoder spent = {:.2f} s".format(hw , encoder , _end - _start))
        
        # cpu 解码
        _cmd = ["ffmpeg","-i", srcFile,"-f","mp4", '-c:v', "libx264", '-b:v', '{}k'.format(bit_rate), "-y","NUL"]
        _start = time.time()
        subprocess.run(_cmd, cwd=_cwd,stderr = out,stdout = out)
        _end = time.time()
        print( "{}".format(' '.join(_cmd)) )
        print("{:>10} decoder | {:>10} encoder spent = {:.2f} s".format('h264 cpu' , "libx264" , _end - _start))

        exit()
