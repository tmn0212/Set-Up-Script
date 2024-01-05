import os, os.path
import doPi4_I2CGPIO_ICE40  as DO
#import daqPi4B_Basys3 as DO

import cherrypy

#def leds_refresh():

#        MyMEA.detect_leds_continous()


MyDO=DO.ICE40_I2CGPIO_DO()

#t=threading.Thread(target=leds_refresh)
#t.daemon=True
#t.start()
#MyMEA.detect_leds_continous()

class DE2Power(object):

    #MEA.detect_leds_continous(centroids)
    @cherrypy.expose
    def index(self):
        return 'ok' #open('index.html')


@cherrypy.expose
class DE2PowerWebAPI(object):
    #@cherrypy.tools.accept(media='text/plain')
    #def GET_ID(self,boardNumber='0'):
    #    return MyMEA.usb

    @cherrypy.tools.accept(media='text/plain')
    def GET(self,boardNumber='0'):
        return 'ok'
        #print('cam leds=',MyCAM.leds)
        #return str(MyCAM.leds[0])
    #    leds=[str(x) for x in MyMEA.leds]
    #    return ''.join(leds) # array to str

    def POST(self,switches='x'*20,boardNumber='0'): # 10SW+4KEY
        #print('web api post switches=',switches)
        try:
            MyDO.writeSwitches(switches)
            print("web apt post switchs=",switches)
        except:
            pass
        return ''.join([str(do) for do in MyDO.DO])
        #print('web api dataStr=',dataStr)
        #sw=switches[0:20]
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



if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/generator': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }


    }
    #MyWebAPI=DE2PowerWebAPI()
    #MyWebAPI.DAQ=MyDaq
    #cherrypy.engine.exit()

##    cherrypy.config.update({
##    'server.socket_host' : '127.0.0.1',
##    'server.socket_port' : 9000,
##    })
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    #cherrypy.config.update(
    #{'server.socket_host': '24.243.100.105'} )

    #cherrypy.config.update({'server.socket_host':'::'})
    cherrypy.config.update({'server.socket_port':7001})
    webapp = DE2Power()
    webapp.generator = DE2PowerWebAPI()

    cherrypy.quickstart(webapp, '/',conf)

##MyDaq=daq.niUSB6501()
##MyDaq.listDaqDevices()
####
##while (True):
##    MyDaq.writeDO_POWR(True)
##    input("check power on")
##    MyDaq.writeDO_POWR(False)
##    input("check power off")
##

