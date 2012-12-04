import os
from twisted.application import service, internet
from twisted.web import static, server
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile


def getWebService():
    fileServer = server.Site(static.File(os.getcwd()))
    return internet.TCPServer(8080, fileServer)


application = service.Application("Demo app")
logfile = DailyLogFile("my.log", "/tmp")
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
service = getWebService()
service.setServiceParent(application)
