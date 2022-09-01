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
import glob
import ffmpeg
from utilspy_g4 import templated_remove_files


def _remove_temp_files() -> None:
    """
    Remove temp files
    :rtype: None
    :return: None
    """

    templated_remove_files('tests/output/*.ts')


def test_defaults():
    stream = StreamSaver()

    assert stream.stream_URL == ''
    assert stream.output_template == 'output_%Y-%m-%d_%H-%M-%S.ts'
    assert stream.segment_time == '01:00:00'


def test_set_vars_1():
    stream = StreamSaver('rtsp://localhost:12345', '%H-%M-%S.ts', '00:10:00')

    assert stream.stream_URL == 'rtsp://localhost:12345'
    assert stream.output_template == '%H-%M-%S.ts'
    assert stream.segment_time == '00:10:00'


def test_set_vars_2():
    stream = StreamSaver(output_template='out.ts',
                         segment_time='12:34:56',
                         stream_URL='rtsp://user:pass@localhost:4321')

    assert stream.stream_URL == 'rtsp://user:pass@localhost:4321'
    assert stream.output_template == 'out.ts'
    assert stream.segment_time == '12:34:56'


def test_print(capsys):
    stream = StreamSaver(stream_URL='rtsp://user:pass@localhost:4321',
                         output_template='%H-%M-%S.ts',
                         segment_time='12:34:56'
                         )
    print(stream)

    captured = capsys.readouterr()
    assert captured.out == 'rtsp://user:pass@localhost:4321 => %H-%M-%S.ts (12:34:56)\n'


def test_save():
    _remove_temp_files()

    rtsp_srv = Popen(['rtsp-simple-server', 'tests/rtsp-simple-server.yml'])

    time.sleep(5)

    ffmpeg_stream = Popen(['ffmpeg', '-re', '-stream_loop', '-1', '-i', 'tests/test.mp4', '-c', 'copy', '-f', 'rtsp',
                           'rtsp://localhost:8554/mystream'])

    time.sleep(5)

    stream = StreamSaver(stream_URL='rtsp://localhost:8554/mystream',
                         output_template='tests/output/out_%H-%M-%S.ts',
                         segment_time='00:00:05'
                         )
    stream.run()

    time.sleep(20)

    stream.stop()
    ffmpeg_stream.terminate()
    rtsp_srv.terminate()

    ts_files = glob.iglob('tests/output/*.ts')

    i = 0
    for file in ts_files:
        if i <= 3:
            info = ffmpeg.probe(file)
            for video_stream in info['streams']:
                if video_stream['index'] == 0:
                    assert video_stream['codec_name'] == 'h264'
                    break
        i += 1

    assert i >= 4

    _remove_temp_files()
