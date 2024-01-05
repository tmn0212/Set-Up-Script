import cherrypy
import json
import os
import subprocess
import threading
import time

import measurePiGPIOICE40 as MEAPi
import measureDual_Ftdi4232_Pi4 as MEAFtdi
#import daqPi4B_Basys3 as DO

#def leds_refresh():

#        MyMEA.detect_leds_continous()


MyMEAPi=MEAPi.ICE40_Pi4_GPIO_DI()
MyMEAFtdi=MEAFtdi.Dual_Ftdi4232()

#MyDO=DO.Ftdi4232()

#t=threading.Thread(target=leds_refresh)
#t.daemon=True
#t.start()
MyMEAPi.detect_leds_continous()
MyMEAFtdi.detect_leds_continous()

class FPGABoard:
    no = 0
    def __init__(self, name='ice40'):
        self.name = name
        self.no = FPGABoard.no
        self.BOOT = '1'                 # SD boot by default
        self.user = 'na'		# board user controlling the board
        self.ready = '1'		# board status: idle
        self.starttime = 0		# current timer start time
        self.stoptime = 0		# current timer stop time
        self.timeout = 60		# 1m 5m for jtag boot mode

        self.jtagNotSD = True
        self.waitlist = []
        self.timer = threading.Timer(1, self.timeoutBoard)
        FPGABoard.no += 1

    def timeoutBoard(self):
        if len(self.waitlist) > 0:
            self.ready = '0'
            self.user = self.waitlist.pop(0)
            self.starttime = time.time() * 1000
            self.stoptime = self.starttime + self.timeout * 1000
            self.timer.cancel()
            self.timer = threading.Timer(self.timeout, self.timeoutBoard)	# 30 seconds timeout board assigned from waitlist
            self.timer.start()

        else:
            self.ready = '1'
            self.user = 'na'
            self.starttime = 0
            self.stoptime = 0

board = FPGABoard('ice40/0')

class DE2Power(object):

    #MEA.detect_leds_continous(centroids)
    @cherrypy.expose
    def index(self):
        return open('index.html')

    @cherrypy.expose
    def checkoutBoard(self, requester='na'):
        board.ready = '0' 
        board.user = requester
        board.starttime = time.time() * 1000
        board.stoptime = board.starttime + board.timeout * 1000
        board.timer.cancel()
        board.timer = threading.Timer(board.timeout, board.timeoutBoard)
        board.timer.start()

    @cherrypy.expose
    def returnBoard(self):
        if len(board.waitlist) > 0:
            board.ready = '0'
            board.user = board.waitlist.pop(0)
            board.starttime = time.time() * 1000
            board.stoptime = board.starttime + board.timeout * 1000
            board.timer.cancel()
            board.timer = threading.Timer(board.timeout, board.timeoutBoard)
            board.timer.start()
        else:
            board.ready = '1'
            board.user = 'na'
            board.starttime = 0
            board.stoptime = 0

    @cherrypy.expose
    def cancelWaitlistBoard(self, requester=''):
        if (requester in board.waitlist):
            board.waitlist.remove(requester)

    @cherrypy.expose
    def insertWaitlist(self, requester):
        if (not requester in board.waitlist and board.ready == '0'):
            board.waitlist.append(requester)

    @cherrypy.expose
    def getBoardWaitlist(self):
        return json.dumps({'boardWaitlist': board.waitlist})

@cherrypy.expose
class FPGABoardSystemWebAPI(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET(self,boardNumber='0'):
        return  'Hello from System'

    @cherrypy.tools.accept(media='text/plain')
    def POST(self,cmd,boardNumber='0'):
        print('cmd=',cmd)
        #print('cam leds=',MyCAM.leds)
        #return str(MyCAM.leds[0])
        if cmd=='reboot':
            cmd=['bash','/home/ecelabs/start.sh']
            with subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE) as p:
                (msg0,msg1)=p.communicate()
                print(msg0)
                print(msg1)

@cherrypy.expose
class DE2PowerWebAPI(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET_ID(self):
        return MyMEA.usb

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        #print('cam leds=',MyCAM.leds)
        #return str(MyCAM.leds[0])
        ledsPi = [str(x) for x in MyMEAPi.leds]
        ledsFtdi = [str(x) for x in MyMEAFtdi.leds]
        ledsStr = ''.join(ledsPi + ledsFtdi)

        return json.dumps({'ledsStr':ledsStr, 'user': board.user, 'ready': board.ready, 'waitlist': board.waitlist}) #, 'viewerlist': board.viewerlist})
        #return ''.join(ledsPi+ledsFtdi) # array to str

    #def POST(self,switches='x'*24, directionStr='', dataStr=''): # 10SW+4KEY
    #    print('web api post switches=',switches)
        #print('web api dataStr=',dataStr)
    #    sw=switches[0:24]
        #boardNumber=int(switches[24]) # local boardNumber 0-3
        #print('switches=',sw);
        #print('boardNumber=',boardNumber)
        #for n in range (1000):
        #    print('switches=',switches)
        
        #sw=switches
       
        #print('sw=',sw)
        #cherrypy.session['myswitches'] = MyDO.DO
       
        #if sw=='1':
        #        MyDO.writeSW1(0,1)
        #elif sw=='0':
        #       MyDO.writeSW1(0,0)
        #MyDIO.writeBoardSwitches(boardNumber,sw)# 24 bits output
      #  MyDO.writeSwitches(sw)
        #DO=MyDO.DO[int(boardNumber)]
        #return ''.join([str(do) for do in DO])

      #  if directionStr!='' or dataStr!='' : # update JB port
      #      if directionStr!='': # update JB port direction
      #          MyDO.configureJB(directionStr)
      #      if dataStr!='': # post JB input data 
      #          MyDO.writeJB(dataStr)

@cherrypy.expose
class BoardStatusWebAPI(object):
    @cherrypy.tools.json_out()

    def GET(self):
        boardStatus = {}
        boardStatus['available'] = board.ready == '1'
        boardStatus['controller'] = board.user
        boardStatus['boot'] = board.BOOT
        boardStatus['waitlist'] = board.waitlist
        boardStatus['timeout'] = str(board.timeout)
        boardStatus['starttime'] = str(board.starttime)
        boardStatus['stoptime'] = str(board.stoptime)
        boardStatus['jtagFlag'] = str(board.jtagNotSD)

        return json.dumps(boardStatus)


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/generator': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')]
        },
        '/boardStatus': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')]
        },
        '/system': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')]
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

##    cherrypy.config.update({
##    'server.socket_host' : '127.0.0.1',
##    'server.socket_port' : 9000,
##    })
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    #cherrypy.config.update(
    #{'server.socket_host': '24.243.100.105'} )

    #cherrypy.config.update({'server.socket_host':'::'})
    cherrypy.config.update({'server.socket_port':7000})
    #cherrypy.config.update({'log.screen': False})

    webapp = DE2Power()
    webapp.generator = DE2PowerWebAPI()
    webapp.system = FPGABoardSystemWebAPI()
    webapp.boardStatus = BoardStatusWebAPI()

    cherrypy.quickstart(webapp, '/',conf)

##MyDaq=daq.niUSB6501()
##MyDaq.listDaqDevices()

