"""
For tests install:
 - rtsp-simple-server (https://github.com/aler9/rtsp-simple-server)
 - ffmpeg (https://ffmpeg.org)

and add it to PATH
"""

import pytest
from stream_saver_g4 import StreamSaver
from subprocess import Popen
import time
import os
import glob


def _removeTempFiles() -> None:
    """
    Remove temp files
    :rtype: None
    :return: None
    """

    removeFiles = glob.iglob('tests/output/*.ts')

    for _file in removeFiles:
        os.remove(_file)


def test_defaults():
    stream = StreamSaver()

    assert stream.streamURL == ''
    assert stream.outputTemplate == 'output_%Y-%m-%d_%H-%M-%S.ts'
    assert stream.segmentTime == '01:00:00'


def test_setVars_1():
    stream = StreamSaver('rtsp://localhost:12345', '%H-%M-%S.ts', '00:10:00')

    assert stream.streamURL == 'rtsp://localhost:12345'
    assert stream.outputTemplate == '%H-%M-%S.ts'
    assert stream.segmentTime == '00:10:00'


def test_setVars_2():
    stream = StreamSaver(outputTemplate='out.ts',
                         segmentTime='12:34:56',
                         streamURL='rtsp://user:pass@localhost:4321')

    assert stream.streamURL == 'rtsp://user:pass@localhost:4321'
    assert stream.outputTemplate == 'out.ts'
    assert stream.segmentTime == '12:34:56'


def test_print(capsys):
    stream = StreamSaver(streamURL='rtsp://user:pass@localhost:4321',
                         outputTemplate='%H-%M-%S.ts',
                         segmentTime='12:34:56'
                         )
    print(stream)

    captured = capsys.readouterr()
    assert captured.out == 'rtsp://user:pass@localhost:4321 => %H-%M-%S.ts (12:34:56)\n'


def test_save():
    _removeTempFiles()

    rtspSrv = Popen(['rtsp-simple-server', 'tests/rtsp-simple-server.yml'])

    time.sleep(5)

    ffmpegStream = Popen(['ffmpeg', '-re', '-stream_loop', '-1', '-i', 'tests/test.mp4', '-c', 'copy', '-f', 'rtsp',
                          'rtsp://localhost:8554/mystream'])

    time.sleep(5)

    stream = StreamSaver(streamURL='rtsp://localhost:8554/mystream',
                         outputTemplate='tests/output/out_%H-%M-%S.ts',
                         segmentTime='00:00:05'
                         )
    stream.run()

    time.sleep(20)

    stream.stop()
    ffmpegStream.terminate()
    rtspSrv.terminate()

    # _removeTempFiles()