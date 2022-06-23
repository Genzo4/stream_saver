import pytest
from stream_saver_g4 import StreamSaver


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


