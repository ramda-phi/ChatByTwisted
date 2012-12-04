from twisted.application import service
from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.web.template import Element, flattenString, XMLFile, renderer
from twisted.python.filepath import FilePath
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile


class ChatRoomElement(Element):
    loader = XMLFile(FilePath('chatroom.xml'))

    @renderer
    def content(self, request, tag):
        return tag("")


class ChatRoom(Resource):
    def __init__(self, roomName):
        Resource.__init__(self)
        self.roomName = roomName

    def render_GET(self, request):
        request.write("<!DOCTYPE html>\n")
        flattenString(request, RoomListElement()).addCallback(
                request.write)
        request.finish()
        return NOT_DONE_YET


class ChatRoot(Resource):
    def __init__(self):
        Resource.__init__(self)
        self.requestedRoom = []
        self.putChild('', ChatIndexPage(self.requestedRoom))

    def render(self, request):
        request.redirect(request.path + '/')
        return "render dunc"

    def getChild(self, path, request):
        if path not in self.requestedRoom:
            return ChatRoom(path)


class RoomListElement(Element):
    loader = XMLFile(FilePath('roomlist.xml'))

    @renderer
    def content(self, request, tag):
        return tag("")


class ChatIndexPage(Resource):
    def __init__(self, requestedRoomList):
        Resource.__init__(self)
        self.requestedRooms = requestedRoomList

    def render_GET(self, request):
        request.write("<!DOCTYPE html>\n")
        flattenString(request, RoomListElement()).addCallback(
                request.write)
        request.finish()
        return NOT_DONE_YET


class EntranceElement(Element):
    loader = XMLFile(FilePath('entrance.xml'))

    @renderer
    def content(self, request, tag):
        return tag("")


class Root(Resource):
    isLeaf = True

    def render_GET(self, request):
        request.write("<!DOCTYPE html>\n")
        flattenString(request, EntranceElement()).addCallback(
                request.write)
        request.finish()
        return NOT_DONE_YET


#application = service.Application("Chat Demo")
#logfile = DailyLogFile("chatdemo.log", "")
#application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
#service = appName()
#service.setServiceParent(application)

root = Resource()
root.putChild('', Root())
root.putChild('RoomList', ChatRoot())
site = Site(root)
reactor.listenTCP(8080, site)
reactor.run()
