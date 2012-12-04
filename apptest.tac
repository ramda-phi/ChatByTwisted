import os
from twisted.application import service, internet
from twisted.web import static, server


def getWebService():
    fileServer = server.Site(static.File(os.getcwd()))
    return internet.TCPServer(8080, fileServer)


application = service.Application("Demo app")
service = getWebService()
service.setServiceParent(application)
