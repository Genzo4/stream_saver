class StreamSaver:

    def __init__(self,
                 streamURL: str = '',
                 outputTemplate: str = 'output_%Y-%m-%d_%H-%M-%S.ts',
                 segmentTime: str = '01:00:00'):
        """
        :param streamURL: Stream URL
        :param outputTemplate: Output template
        """

        self.streamURL = streamURL
        self.outputTemplate = outputTemplate
        self.segmentTime = segmentTime

    @property
    def streamURL(self):
        return self.__streamURL

    @streamURL.setter
    def streamURL(self, streamURL: str):
        self.__streamURL = streamURL

    @property
    def outputTemplate(self):
        return self.__outputTemplate

    @outputTemplate.setter
    def streamURL(self, outputTemplate: str):
        self.__outputTemplate = outputTemplate

    @property
    def segmentTime(self):
        return self.__segmentTime

    @segmentTime.setter
    def segmentTime(self, segmentTime: str):
        self.__segmentTime = segmentTime

    def __str__(self):
        """Overrides the default implementation"""
        return '%s => %s (%d)' % (self.streamURL, self.outputTemplate, self.segmentTime)

