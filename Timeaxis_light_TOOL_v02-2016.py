#coding=utf-8
# timeaxis_light_Tool v0.1
# Arnold  render tool for maya 2016
# author :deliang  #E-mail :524707056@qq.com



import sys,os,re
import maya.cmds as cmd
import maya.mel as mm
import pymel.core as pm
import mtoa.aovs as aovs
from PySide import QtCore, QtGui


globIsoFlag=[]

WINDOW_NAME = 'Tool'
def maya_main_window():
    import maya.OpenMayaUI as apiUI
    from shiboken import wrapInstance
    main_win_ptr = apiUI.MQtUtil.mainWindow()
    return wrapInstance(long(main_win_ptr), QtGui.QWidget)
    
class Dialog(QtGui.QDialog):

    def __init__(self, parent=None, show=True):
        super(Dialog, self).__init__(parent=parent)
        self.mainLayout = QtGui.QGridLayout(self)
        
        self.CopyTransformBox()
        self.IsoBox()
        self.maskGroup()
        self.workSpace()
        self.getOriginObjGroup()
        self.setAOVGroup()
        self.openSkyFile()
        self.openFileBox()
        self.MotionVectorGro()
        self.creatLayerGro()
        self.creatShadowGro()
        self.optMayaGrp()
        self.renderwindowgru()
        
        self.mainLayout.addWidget(self.CopyTransformGBox,0,0,1,2)
        self.mainLayout.addWidget(self.IsoGBox,1,0,1,2)
        
        
        self.mainLayout.addWidget(self.workSpaceGroup,2,0,1,1)
        self.mainLayout.addWidget(self.aovGoup,2,1,1,1)
        
        
        self.mainLayout.addWidget(self.layerGroup,3,0,1,2)
        self.mainLayout.addWidget(self.maskGroup,4,0,1,2)
        
        self.mainLayout.addWidget(self.MotionVectorGroup,5,0,1,2)
        self.mainLayout.addWidget(self.shdowlayerGroup,6,0,1,2)
        self.mainLayout.addWidget(self.matchShaderGrp,7,0,1,2)
        
        self.mainLayout.addWidget(self.openskyPath,8,0,1,1)
        self.mainLayout.addWidget(self.openFPath,8,1,1,1)

        self.mainLayout.addWidget(self.optGroup,9,0,1,1)
        self.mainLayout.addWidget(self.displayRenderWinGro,9,1,1,1)
        

        self.setLayout(self.mainLayout)



        if show:
            self.show()

####################################################################################
#####################        copy transform         ################################
####################################################################################
       
    def CopyTransformBox(self):

        self.CopyTransformGBox= QtGui.QGroupBox("COPY  TRANSFORM")
        self.allTr = QtGui.QPushButton('ALL')
        self.Tr_translate = QtGui.QPushButton('Translate')
        self.Tr_rotate = QtGui.QPushButton('Rotate')
        
        CopyTransformLayout = QtGui.QGridLayout()
        CopyTransformLayout.addWidget(self.allTr,2,0,1,1)
        CopyTransformLayout.addWidget(self.Tr_translate,2,1,1,1)
        CopyTransformLayout.addWidget(self.Tr_rotate,2,2,1,1)
        self.CopyTransformGBox.setLayout(CopyTransformLayout)
        
        self.connect(self.allTr, QtCore.SIGNAL('clicked()' ), self.copyall )
        self.connect(self.Tr_translate, QtCore.SIGNAL('clicked()' ), self.copytraslate )
        self.connect(self.Tr_rotate, QtCore.SIGNAL('clicked()' ), self.Rotate )
    def copyall(self):   
        print 1
        dlight = cmd.ls(sl=True,tr=True)
        for i in range(1,len(dlight)):
            cmd.copyAttr(dlight[0],dlight[i],values=True,attribute=['translate','rotate'])    
    def copytraslate(self):   
        dlight = cmd.ls(sl=True,tr=True)
        for i in range(1,len(dlight)):
            cmd.copyAttr(dlight[0],dlight[i],values=True,attribute=['translate'])      
    def Rotate(self):   
        dlight = cmd.ls(sl=True,tr=True)
        for i in range(1,len(dlight)):
            cmd.copyAttr(dlight[0],dlight[i],values=True,attribute=['rotate'])           
####################################################################################
#####################        Isolate Light  Tool       #############################
####################################################################################
    def IsoBox(self):
        
        self.IsoGBox= QtGui.QGroupBox("Isolate Light  Tool")
        
        self.isolate = QtGui.QPushButton('Isolate Selection')
        self.lookthrought = QtGui.QPushButton('Look Throught')
        self.clean = QtGui.QPushButton('clean')
        
        IsoLayout = QtGui.QGridLayout()
        IsoLayout.addWidget(self.isolate,2,0,1,1)
        IsoLayout.addWidget(self.lookthrought,2,1,1,1)
        IsoLayout.addWidget(self.clean,2,2,1,1)
        self.IsoGBox.setLayout(IsoLayout)
        
        self.connect(self.isolate, QtCore.SIGNAL('clicked()' ), self.isoLightSel )
        self.connect(self.lookthrought, QtCore.SIGNAL('clicked()' ), self.lookThu )
        self.connect(self.clean, QtCore.SIGNAL('clicked()' ), self.lookThuClean ) 
    
    def isoLightSel(self, *args ):
        global globIsoFlag
        allLights = getAllLights()
        lightSel = getSelectedLights()
        resultSel = []
        for each in allLights:
            if not each in lightSel:
                resultSel.append(each)
        if not globIsoFlag:
            self.isolate.setStyleSheet("QPushButton:hover{color:red}")
            print 'Modo Isolate Light = ON'
            for each in resultSel:
                cmd.setAttr(each+'.v',0)
            globIsoFlag = 1
        else:
            pass
            self.isolate.setStyleSheet("QPushButton:hover{color:0.38,0.38,0.38}")
            print 'Modo Isolate Light = OFF'
            for each in allLights:
                cmd.setAttr(each+'.v',1)
            globIsoFlag = 0
            
    def lookThu(self, *args ):
        global previousCamera
        panel = pm.playblast(activeEditor=True)
        panel_name = str(panel).split('|')[-1]
        objs = pm.ls(sl=True)
        if objs:
            previousCamera = pm.windows.modelPanel(panel_name, query=True, camera=True)
            cmd = 'lookThroughModelPanelClipped %s %s 1 100000000' % (objs[0], panel_name)
            mm.eval(cmd)
            
    def lookThuClean(self, *args  ):
        global previousCamera
        panel = pm.playblast(activeEditor=True)
        panel_name = str(panel).split('|')[-1]
        if previousCamera:
            pm.windows.modelPanel(panel_name, e=1, camera=previousCamera)
    
        self.clean_camera_under_cam()
    
    def clean_camera_under_cam(self):
        ltypes = ['ambientLight','directionalLight','pointLight','spotLight','areaLight','volumeLight','aiAreaLight','aiSkyDomeLight','aiPhotometricLight']
        cam_list = list()
        for ltype in ltypes:
            for cam in pm.ls(type=ltype):
                t = cam.listRelatives(p=1)[0]
                ccs = [c for c in t.listRelatives(c=1) if pm.objectType(c) == 'camera']
                if ccs:
                    cam_list.extend(ccs)
        for cam in cam_list:
            try:
                pm.delete(cam)
            except:
                pass  
####################################################################################
#####################        open SKY           #############################
####################################################################################   
    def openSkyFile(self):
        
        self.openskyPath= QtGui.QGroupBox("OPEN sky")
        
        self.openskybnt = QtGui.QPushButton('SKY PATH')
        
        skyLayout = QtGui.QGridLayout()
        skyLayout.addWidget(self.openskybnt,2,0,1,1)

        self.openskyPath.setLayout(skyLayout)
        
        self.connect(self.openskybnt, QtCore.SIGNAL('clicked()'),self.openSkyPath)
    def openSkyPath(self):
        os.startfile(str("\\\\192.168.1.161\desktop2\SKY"))



####################################################################################
#####################        open pic path             #############################
####################################################################################               
                
    def openFileBox(self):
        
        self.openFPath= QtGui.QGroupBox("OPEN FILE")
        
        self.openFileBox = QtGui.QPushButton('OPEN FILE PATH')
        
        openLayout = QtGui.QGridLayout()
        openLayout.addWidget(self.openFileBox,2,0,1,1)

        self.openFPath.setLayout(openLayout)
        
        self.connect(self.openFileBox, QtCore.SIGNAL('clicked()' ), self.openPath)
    def openPath(self):  
        
        if os.path.exists(str(cmd.workspace( fn=True)+'/images')): 
            os.startfile(str(cmd.workspace( fn=True)+'/images'))
        else:
            os.startfile(str(cmd.workspace( fn=True)))

####################################################################################
#####################        mat match         #############################
####################################################################################               
                
    def getOriginObjGroup(self):
        
        self.matchShaderGrp= QtGui.QGroupBox("")
        
        self.QLineEdit = QtGui.QLineEdit('')
        
        self.originbtn = QtGui.QPushButton('Select')
        self.setShaderbtn = QtGui.QPushButton('DO...')
        
        macthShaderLayout = QtGui.QGridLayout()
        macthShaderLayout.addWidget(self.QLineEdit,0,0,1,1)
        macthShaderLayout.addWidget(self.originbtn,0,1,1,1)
        macthShaderLayout.addWidget(self.setShaderbtn,0,2,1,1)

        self.matchShaderGrp.setLayout(macthShaderLayout)
        
        self.connect(self.originbtn, QtCore.SIGNAL('clicked()'),self.getObjFn)
        self.connect(self.setShaderbtn, QtCore.SIGNAL('clicked()'),self.setShader)

    def getObjFn(self):
        self.originObj = pm.ls(sl=1,dag=1,type='mesh')
        self.QLineEdit.clear()
        self.QLineEdit.setText(self.originObj[0].name())
        
    def setShader(self):
        
        self.objectiveObj = pm.ls(sl=1,dag=1,type='mesh')   
        sg=self.originObj[0].outputs()
        for s in sg:
            newface=[]
            orShader = pm.ls(pm.listConnections(s),materials=1)[0].name()
            print orShader
            if isinstance( s, pm.nodetypes.ShadingEngine):
                if s.name()=='initialShadingGroup':
                    pass
                else:
                    
                    try:
                        origin_face = pm.sets(s,q=True)
                        for i in self.objectiveObj:
                            for of in origin_face:
                                face =of.name().split(".")[1]
                                newname = str(i.name())+"."+str(face)
                                newface.append( newname)
                    except:
                        pass
            else:
                pass
            #print s
            #print  newface
            cmd.select(newface,r=1,noExpand=1)
            cmd.hyperShade( assign= orShader)
        print "shader ok"
####################################################################################
#####################        make aov                  #############################
####################################################################################          
     
    def setAOVGroup(self):
        self.aovGoup= QtGui.QGroupBox("aov")
        
        self.aov = QtGui.QPushButton('AOV')
        
        aovLayout = QtGui.QGridLayout()
        aovLayout.addWidget(self.aov,2,0,1,1)

        self.aovGoup.setLayout(aovLayout)
     
        self.connect(self.aov, QtCore.SIGNAL('clicked()'),self.makeAOV)
    def makeAOV(self):  
        cmd.setAttr( "defaultArnoldDriver.mergeAOVs" ,1)

        timeaxis_aov_Nonmal = aovs.AOVInterface().addAOV('Normal', aovType='rgba')
        timeaxis_aov_N_samplerInfo= cmd.createNode ('samplerInfo',name='timeaxis_aov_N_samplerInfo')
        timeaxis_aov_N_surfaceShader= cmd.createNode ('surfaceShader',name='timeaxis_aov_N_surfaceShader')
        cmd.connectAttr(timeaxis_aov_N_samplerInfo+'.normalCamera',timeaxis_aov_N_surfaceShader+'.outColor')
        cmd.connectAttr(timeaxis_aov_N_surfaceShader+'.outColor',"aiAOV_Normal.defaultValue")
        
        timeaxis_aov_OCC = aovs.AOVInterface().addAOV('OCC', aovType='rgba')
        timeaxis_aov_occ_aiAO= cmd.createNode ('aiAmbientOcclusion',name='timeaxis_aov_occ_aiAO')
        cmd.connectAttr(timeaxis_aov_occ_aiAO+'.outColor','aiAOV_OCC.defaultValue')
        
        timeaxis_aov_rim = aovs.AOVInterface().addAOV('Rim', aovType='rgba')
        timeaxis_aov_rim_samplerInfo= cmd.createNode ('samplerInfo',name='timeaxis_aov_rim_samplerInfo')
        timeaxis_aov_rim_ramp= cmd.createNode ('ramp',name='timeaxis_aov_rim_ramp')
        cmd.setAttr(timeaxis_aov_rim_ramp+".colorEntryList[1].color" ,1,1,1)
        cmd.setAttr(timeaxis_aov_rim_ramp+".colorEntryList[0].color" ,0,0,0)
        cmd.setAttr(timeaxis_aov_rim_ramp+".colorEntryList[0].position" ,0.68)
        timeaxis_aov_rim_aistandard= cmd.createNode ('aiStandard',name='timeaxis_aov_rim_aistandard')
        cmd.connectAttr(timeaxis_aov_rim_samplerInfo+'.facingRatio',timeaxis_aov_rim_ramp+'.uvCoord.vCoord')
        cmd.connectAttr(timeaxis_aov_rim_ramp+'.outColor',timeaxis_aov_rim_aistandard+'.color')
        cmd.connectAttr(timeaxis_aov_rim_aistandard+'.outColor',"aiAOV_Rim.defaultValue")
        
        timeaxis_aov_Z_Depth= aovs.AOVInterface().addAOV('Z_Depth', aovType='rgba')
        timeaxis_aov_z_samplerInfo= cmd.createNode ('samplerInfo',name='timeaxis_aov_z_samplerInfo')
        timeaxis_aov_Z_multiplyDivide= cmd.createNode ('multiplyDivide',name='timeaxis_aov_Z_multiplyDivide')
        cmd.setAttr(timeaxis_aov_Z_multiplyDivide+ ".input2X", -1.1)
        timeaxis_aov_Z_setRange= cmd.createNode ('setRange',name='timeaxis_aov_Z_setRange')
        cmd.setAttr(timeaxis_aov_Z_setRange+".minX",1)
        cmd.setAttr(timeaxis_aov_Z_setRange+".oldMinX",0.1)
        cmd.setAttr(timeaxis_aov_Z_setRange+".oldMaxX",1500)
        timeaxis_aov_Z_aiUtility= cmd.createNode ('aiUtility',name='timeaxis_aov_Z_aiUtility')
        cmd.setAttr( timeaxis_aov_Z_aiUtility+'.shadeMode', 2)
        cmd.connectAttr(timeaxis_aov_z_samplerInfo+'.pointCamera.pointCameraZ',timeaxis_aov_Z_multiplyDivide+'.input1.input1X')
        cmd.connectAttr(timeaxis_aov_Z_multiplyDivide+'.input1.input1X',timeaxis_aov_Z_setRange+'.value.valueX')
        cmd.connectAttr(timeaxis_aov_Z_setRange+'.outValueX',timeaxis_aov_Z_aiUtility+'.color.colorR')
        cmd.connectAttr(timeaxis_aov_Z_setRange+'.outValueX',timeaxis_aov_Z_aiUtility+'.color.colorG')
        cmd.connectAttr(timeaxis_aov_Z_setRange+'.outValueX',timeaxis_aov_Z_aiUtility+'.color.colorB')
        cmd.connectAttr(timeaxis_aov_Z_aiUtility+'.outColor',"aiAOV_Z_Depth.defaultValue")
        aovs.AOVInterface().addAOV('beauty', aovType='rgba')
        aovs.AOVInterface().addAOV('direct_diffuse', aovType='rgb')
        aovs.AOVInterface().addAOV('direct_specular', aovType='rgb')
        aovs.AOVInterface().addAOV('direct_sss', aovType='rgb')
        aovs.AOVInterface().addAOV('direct_transmission', aovType='rgb')
        aovs.AOVInterface().addAOV('refraction', aovType='rgb')
        aovs.AOVInterface().addAOV('refraction_opacity', aovType='rgb')
        aovs.AOVInterface().addAOV('shadow_matte', aovType='rgb')
        aovs.AOVInterface().addAOV('sss', aovType='rgb')
        
####################################################################################
#####################        mask                    #############################
####################################################################################   


    def maskGroup(self):
        
        self.maskGroup= QtGui.QGroupBox("")
        
        self.maskSpbtn = QtGui.QPushButton('Mask L')
        self.maskRedbtn = QtGui.QPushButton('Red')
        self.maskRedbtn.setStyleSheet("background-color: rgb(255, 0, 0)")
        
        self.maskGreenbtn = QtGui.QPushButton('Green')
        self.maskGreenbtn.setStyleSheet("background-color: rgb(0, 255, 0)")
        
        self.maskBluebtn = QtGui.QPushButton('Blue')
        self.maskBluebtn.setStyleSheet("background-color: rgb(0, 0, 255)")
        
        self.maskBlackbtn = QtGui.QPushButton('Black')
        self.maskBlackbtn.setStyleSheet("background-color: rgb(0, 0, 0)")
        
        maskbtnLayout = QtGui.QGridLayout()
        maskbtnLayout.addWidget(self.maskSpbtn,0,0,1,1)
        maskbtnLayout.addWidget(self.maskRedbtn,0,1,1,1)
        maskbtnLayout.addWidget(self.maskGreenbtn,0,2,1,1)
        maskbtnLayout.addWidget(self.maskBluebtn,0,3,1,1)
        maskbtnLayout.addWidget(self.maskBlackbtn,0,4,1,1)
        

        self.maskGroup.setLayout(maskbtnLayout)
        
        self.connect(self.maskSpbtn, QtCore.SIGNAL('clicked()'), self.makeMaskeLayerFn)
        self.connect(self.maskRedbtn, QtCore.SIGNAL('clicked()'), self.mRedFn)
        self.connect(self.maskGreenbtn, QtCore.SIGNAL('clicked()'), self.mGreenFn)
        self.connect(self.maskBluebtn, QtCore.SIGNAL('clicked()'), self.mBlueFn)
        self.connect(self.maskBlackbtn, QtCore.SIGNAL('clicked()'), self.mBlackFn)
    def makeMaskeLayerFn(self):  
    
        cmd.createRenderLayer (name="Mask",mc=True,nr=True)
        cmd.editRenderLayerAdjustment ("defaultArnoldRenderOptions.AASamples")
        cmd.setAttr ("defaultArnoldRenderOptions.AASamples" ,2)
        cmd.editRenderLayerAdjustment ("defaultArnoldRenderOptions.GIDiffuseSamples")
        cmd.setAttr ("defaultArnoldRenderOptions.GIDiffuseSamples" ,2)

        cmd.setAttr ("defaultArnoldRenderOptions.range_type" ,1)
        cmd.editRenderLayerAdjustment( "defaultArnoldRenderOptions.aovMode")
        cmd.setAttr ("defaultArnoldRenderOptions.aovMode" ,0)
        
    def mRedFn(self): 
        obj=[]
        obj = cmd.ls(sl=1,dag=1,s=1) 
        if "Red_mask_SG_tm" in cmd.ls(set=1):
            cmd.hyperShade( assign= "Red_mask_SG_tm" )
        else:
            Red_mask_tm= cmd.shadingNode ('surfaceShader',name='Red_mask_tm_shder',asShader=1)
            cmd.setAttr(Red_mask_tm+".outColor" , 1, 0, 0, type="double3")
            cmd.setAttr(Red_mask_tm+".outMatteOpacity" , 0, 0, 0, type="double3")
        
            cmd.hyperShade( assign= Red_mask_tm )
            Red_mask_SG_tm = cmd.sets(renderable=1,empty=1,name='Red_mask_SG_tm')
            cmd.connectAttr(Red_mask_tm+'.outColor',Red_mask_SG_tm+'.surfaceShader',f=1)
            cmd.sets(obj ,e=1,forceElement=Red_mask_SG_tm)

    def mGreenFn(self): 
        obj=[]
        obj = cmd.ls(sl=1,dag=1,s=1) 
        #self.obj = cmd.ls(sl=1,dag=1,s=1) 
        if "Green_mask_SG_tm" in cmd.ls(set=1):
            cmd.hyperShade( assign= "Green_mask_SG_tm" )
        else:
            Green_mask_tm= cmd.shadingNode ('surfaceShader',name='Green_mask_tm_shder',asShader=1)
            cmd.setAttr(Green_mask_tm+".outColor" , 0, 1, 0, type="double3")
            cmd.setAttr(Green_mask_tm+".outMatteOpacity" , 0, 0, 0, type="double3")
        
            cmd.hyperShade( assign= Green_mask_tm )
            Green_mask_SG_tm = cmd.sets(renderable=1,empty=1,name='Green_mask_SG_tm')
            cmd.connectAttr(Green_mask_tm+'.outColor',Green_mask_SG_tm+'.surfaceShader',f=1)
            cmd.sets(obj ,e=1,forceElement=Green_mask_SG_tm)

    def mBlueFn(self):  
        obj=[]
        obj = cmd.ls(sl=1,dag=1,s=1) 
        if "Blue_mask_SG_tm" in cmd.ls(set=1):
            cmd.hyperShade( assign= "Blue_mask_SG_tm" )
        else:
            Blue_mask_tm= cmd.shadingNode ('surfaceShader',name='Blue_mask_tm_shder',asShader=1)
            cmd.setAttr(Blue_mask_tm+".outColor" , 0, 0, 1, type="double3")
            cmd.setAttr(Blue_mask_tm+".outMatteOpacity" , 0, 0, 0, type="double3")
        
            cmd.hyperShade( assign= Blue_mask_tm )
            Blue_mask_SG_tm = cmd.sets(renderable=1,empty=1,name='Blue_mask_SG_tm')
            cmd.connectAttr(Blue_mask_tm+'.outColor',Blue_mask_SG_tm+'.surfaceShader',f=1)
            cmd.sets(obj ,e=1,forceElement=Blue_mask_SG_tm)
            
            
    def mBlackFn(self):  
        obj=[]
        obj = cmd.ls(sl=1,dag=1,s=1) 
        if "Black_mask_SG_tm" in cmd.ls(set=1):
            cmd.hyperShade( assign= "Black_mask_SG_tm" )
        else:
            Black_mask_tm= cmd.shadingNode ('surfaceShader',name='Black_mask_tm_shder',asShader=1)
            cmd.setAttr(Black_mask_tm+".outColor" , 0, 0, 0, type="double3")
        
            cmd.hyperShade( assign= Black_mask_tm )
            Black_mask_SG_tm = cmd.sets(renderable=1,empty=1,name='Black_mask_SG_tm')
            cmd.connectAttr(Black_mask_tm+'.outColor',Black_mask_SG_tm+'.surfaceShader',f=1)
            cmd.sets(obj ,e=1,forceElement=Black_mask_SG_tm)
####################################################################################
#####################            optimized         #############################
####################################################################################    

    def optMayaGrp(self):
        self.optGroup= QtGui.QGroupBox("")
        
        self.optbtn = QtGui.QPushButton('Clear Maya')
        self.nameSpcabtn = QtGui.QPushButton('Name Space')
        
        optLayout = QtGui.QGridLayout()
        optLayout.addWidget(self.optbtn,0,0,1,1)
        optLayout.addWidget(self.nameSpcabtn,0,1,1,1)

        self.optGroup.setLayout(optLayout)
        
        self.connect(self.optbtn, QtCore.SIGNAL('clicked()'), self.doOptFn)
        self.connect(self.nameSpcabtn, QtCore.SIGNAL('clicked()'), self.nameSpcaeFn)
        
    def doOptFn(self):
        #pm.mel.source('cleanUpScene')

        #pm.mel.scOpt_performOneCleanup({
        #'setsOption',
        #'nurbsSrfOption',
        #'partitionOption',
        #'animationCurveOption',
        #'deformerOption',
        #'unusedSkinInfsOption',
        #'brushOption',
        #'shaderOption',
        #'unknownNodes',
        #'shadingNetworksOption'
        #}
        #)
        #unknown = pm.ls(type="unknown")
        #unknown = pm.filter(lambda node: not node.isReferenced(), unknown)
        #for node in unknown:
            #if not pm.objExists(node):
                #continue
                #pm.delete(node)
                
        pm.delete(pm.ls( type="unknown"))
        pm.mel.eval("MLdeleteUnused;")
        print "Optimize "
    def nameSpcaeFn(self):
        allNodes = pm.ls()  
        
        for node in allNodes:
               
            buffer= node.name() 
            try:
                newName = buffer.split(':')[-1]  
                pm.rename (node,newName)  
            except:
                pass

####################################################################################
#####################        set workspace             #############################
####################################################################################              
    def workSpace(self):
        
        self.workSpaceGroup= QtGui.QGroupBox("Work Space Group")
        
        self.workSpbtn = QtGui.QPushButton('Arnold Work Space')
        
        spbtnLayout = QtGui.QGridLayout()
        spbtnLayout.addWidget(self.workSpbtn,2,1,1,1)

        self.workSpaceGroup.setLayout(spbtnLayout)
        
        self.connect(self.workSpbtn, QtCore.SIGNAL('clicked()'), self.setArWorkSp)
    def setArWorkSp(self): 
        if not cmd.pluginInfo('mtoa',l=1,q=1):
            cmd.loadPlugin('mtoa')
            print 'arnold 宸茬粡鍔犺浇'

        if cmd.getAttr('defaultRenderGlobals.currentRenderer') !='arnold':
            
            cmd.setAttr('defaultRenderGlobals.currentRenderer',l=False)
            cmd.setAttr('defaultRenderGlobals.currentRenderer','arnold',type = 'string')
            self.ArSet()
        else:
            self.ArSet()
    def ArSet(self):
        try:
            self.options = pm.PyNode('defaultArnoldRenderOptions')
        except :
            self.options = pm.createNode('aiOptions', name='defaultArnoldRenderOptions', skipSelect=True, shared=True)
        try:
    
            self.filterNode = pm.PyNode('defaultArnoldFilter')
    
        except:
    
            self.filterNode = pm.createNode('aiAOVFilter', name='defaultArnoldFilter', skipSelect=True, shared=True)
        try:
            self.driverNode = pm.PyNode('defaultArnoldDriver')
        except:
            self.driverNode = pm.createNode('aiAOVDriver', name='defaultArnoldDriver', skipSelect=True, shared=True)
        try:
    
            self.resolution = pm.PyNode('defaultResolution')
        except :
            self.resolution = pm.createNode('resolution', name = 'defaultResolution', skipSelect=True, shared=True)
            
        cmd.setAttr ('defaultRenderGlobals.imageFilePrefix',"<Scene>/<RenderLayer>/<RenderLayer>",type="string")
        pm.mel.setMayaSoftwareFrameExt(7,0)
        cmd.colorManagementPrefs(e=True,cmEnabled=False)
        cmd.setAttr ("defaultRenderGlobals.extensionPadding" ,4)
        cmd.setAttr ("defaultArnoldRenderOptions.AASamples" ,2)
        cmd.setAttr ("defaultArnoldRenderOptions.GIDiffuseSamples", 2)
        cmd.setAttr ("defaultArnoldRenderOptions.GIGlossySamples", 1)
        cmd.setAttr ("defaultArnoldRenderOptions.GIRefractionSamples" ,1)
        cmd.setAttr ("defaultArnoldRenderOptions.GISssSamples" ,2)
        cmd.setAttr ("defaultArnoldRenderOptions.GIVolumeSamples",1)
        cmd.setAttr ("defaultArnoldRenderOptions.display_gamma",2.2)
        cmd.setAttr ("defaultArnoldRenderOptions.use_existing_tiled_textures" ,1)
        cmd.setAttr ("defaultArnoldRenderOptions.bucketSize" ,32)
        cmd.setAttr ("defaultArnoldRenderOptions.bucketScanning" ,4)
        cmd.setAttr ("defaultArnoldRenderOptions.abortOnError" ,0)
        cmd.setAttr ("defaultArnoldRenderOptions.log_max_warnings", 100)
        cmd.setAttr ("defaultArnoldRenderOptions.log_to_console", 0)
        cmd.setAttr ("defaultArnoldDriver.mergeAOVs", 1)
        cmd.setAttr ("defaultArnoldRenderOptions.range_type", 0)
        cmd.setAttr ("defaultArnoldRenderOptions.motion_blur_enable" ,0)
        cmd.setAttr ("defaultArnoldRenderOptions.GIRefractionDepth" ,1)
        cmd.setAttr ("defaultArnoldRenderOptions.GIReflectionDepth" ,1)
        cmd.setAttr ("defaultArnoldRenderOptions.GITotalDepth" ,10)
        cmd.setAttr ("defaultArnoldRenderOptions.log_to_console", 0)
        cmd.setAttr ("defaultArnoldRenderOptions.abortOnError", 0)
        
####################################################################################
#####################        set MotionVectorGro             #############################
####################################################################################     
    def MotionVectorGro(self):
        
        self.MotionVectorGroup= QtGui.QGroupBox("Motion Vector Group")
        
        self.MotionVectorbtn = QtGui.QPushButton('MV Layer')
        self.setMotionVectorMatbtn = QtGui.QPushButton('MV Shader')
        
        MotionVectorbtnLayout = QtGui.QGridLayout()
        
        MotionVectorbtnLayout.addWidget(self.MotionVectorbtn,2,0,1,1)
        MotionVectorbtnLayout.addWidget(self.setMotionVectorMatbtn,2,1,1,1)

        self.MotionVectorGroup.setLayout(MotionVectorbtnLayout)
        
        self.connect(self.MotionVectorbtn, QtCore.SIGNAL('clicked()'), self.creatMVshaderlayer)
        self.connect(self.setMotionVectorMatbtn, QtCore.SIGNAL('clicked()'), self.setMVshader)

    def creatMVshaderlayer(self):
        self.sl_mobj= cmd.ls(sl=True,dag=True,s=True)
        cmd.createRenderLayer (name="Motion_Vector",mc=True,nr=True)
        cmd.editRenderLayerAdjustment ("defaultArnoldRenderOptions.AASamples")
        cmd.setAttr ("defaultArnoldRenderOptions.AASamples" ,2)
        cmd.editRenderLayerAdjustment ("defaultArnoldRenderOptions.GIDiffuseSamples")
        cmd.setAttr ("defaultArnoldRenderOptions.GIDiffuseSamples" ,2)
        cmd.editRenderLayerAdjustment ("defaultArnoldRenderOptions.GIGlossySamples")
        cmd.setAttr ("defaultArnoldRenderOptions.GIDiffuseSamples" ,1)
        cmd.editRenderLayerAdjustment ("defaultArnoldRenderOptions.motion_blur_enable")
        cmd.setAttr ("defaultArnoldRenderOptions.motion_blur_enable" ,1)
        cmd.setAttr ("defaultArnoldRenderOptions.range_type" ,1)
        cmd.editRenderLayerAdjustment( "defaultArnoldRenderOptions.aovMode")
        cmd.setAttr ("defaultArnoldRenderOptions.aovMode" ,0)
        

    def setMVshader(self):
        timeaxis_aov_MV_aiMotionVector= cmd.createNode ('aiMotionVector',name='timeaxis_aov_MV_aiMotionVector')
        self.timeaxis_aov_MV_aiUitility= cmd.createNode ('aiUtility',name='timeaxis_aov_MV_aiUitility')
        cmd.setAttr (self.timeaxis_aov_MV_aiUitility+".shadeMode" ,2)
        cmd.setAttr (timeaxis_aov_MV_aiMotionVector+".maxDisplace" ,0.5)
        cmd.connectAttr(timeaxis_aov_MV_aiMotionVector+'.outColor',self.timeaxis_aov_MV_aiUitility+'.color')
        
        cmd.select(self.sl_mobj)
        cmd.hyperShade( assign=self.timeaxis_aov_MV_aiUitility )#缁欑墿浣撴潗璐
        newMVSg = cmd.sets(renderable=1,empty=1,name='mvSG')
        #newMVSg= cmd.createNode ('shadingEngine',name='timeaxis_aov_MV_aiUitilitySG')
        #cmd.connectAttr(disNode+'.out',newSg+'.displacementShader',f=1) # 缁欏畠缃崲鏉愯川銆
        cmd.connectAttr(self.timeaxis_aov_MV_aiUitility+'.outColor',newMVSg+'.surfaceShader',f=1)
        cmd.sets(self.sl_mobj,e=1,forceElement=newMVSg)

####################################################################################
#####################        creat layer               #############################
####################################################################################   
    def creatLayerGro(self):
        
        self.layerGroup= QtGui.QGroupBox("Creat Layer")
        
        self.envLayerbtn = QtGui.QPushButton('ENV Layer')
        self.chaLayerbtn = QtGui.QPushButton('Cha Layer')
        
        layerbtnLayout = QtGui.QGridLayout()
        
        layerbtnLayout.addWidget(self.envLayerbtn,2,0,1,1)
        layerbtnLayout.addWidget(self.chaLayerbtn,2,1,1,1)

        self.layerGroup.setLayout(layerbtnLayout)
        
        self.connect(self.envLayerbtn, QtCore.SIGNAL('clicked()'), self.creatENV)
        self.connect(self.chaLayerbtn, QtCore.SIGNAL('clicked()'), self.creatCha)
        
        
    def creatENV(self):
        cmd.createRenderLayer (name="env_10_key_10",mc=True,nr=True)
        cmd.createRenderLayer (name="env_10_fill_10",mc=True,nr=True)
        
    def creatCha(self):
        cmd.createRenderLayer (name="Cha_10_key_10",mc=True,nr=True)
        cmd.createRenderLayer (name="Cha_10_fill_10",mc=True,nr=True)
####################################################################################
#####################        creat  shadow               #############################
####################################################################################  
    def creatShadowGro(self):
        
        self.shdowlayerGroup= QtGui.QGroupBox("Creat Shadow Layer")
        
        self.shadowLayerbtn = QtGui.QPushButton('Shadow Layer')
        self.shadowShaderbtn = QtGui.QPushButton('Shadow Shader')
        
        shadowlayerbtnLayout = QtGui.QGridLayout()
        
        shadowlayerbtnLayout.addWidget(self.shadowLayerbtn,2,0,1,1)
        shadowlayerbtnLayout.addWidget(self.shadowShaderbtn,2,1,1,1)

        self.shdowlayerGroup.setLayout(shadowlayerbtnLayout)
        
        self.connect(self.shadowLayerbtn, QtCore.SIGNAL('clicked()'), self.creatShdowLayer)
        self.connect(self.shadowShaderbtn, QtCore.SIGNAL('clicked()'), self.makeShdowShader)
        
    def creatShdowLayer(self):
        cmd.createRenderLayer (name="Env_Shdow",mc=True,nr=True)
        cmd.editRenderLayerAdjustment ("defaultArnoldRenderOptions.AASamples")
        cmd.setAttr ("defaultArnoldRenderOptions.AASamples" ,2)
        cmd.editRenderLayerAdjustment ("defaultArnoldRenderOptions.GIDiffuseSamples")
        cmd.setAttr ("defaultArnoldRenderOptions.GIDiffuseSamples" ,2)
        cmd.editRenderLayerAdjustment ("defaultArnoldRenderOptions.GIGlossySamples")
        cmd.setAttr ("defaultArnoldRenderOptions.GIDiffuseSamples" ,1)
        cmd.setAttr ("defaultArnoldRenderOptions.range_type" ,1)
        #cmd.editRenderLayerAdjustment( "defaultArnoldRenderOptions.aovMode")
        #cmd.setAttr ("defaultArnoldRenderOptions.aovMode" ,0)
        sceneAOVs = aovs.AOVInterface().getAOVNodes(names=True)
        for i in sceneAOVs:
        
            if i[0]!='OCC':
                cmd.editRenderLayerAdjustment( i[1]+".enabled")
                cmd.setAttr (i[1]+".enabled" ,0)
                
            else: 
                pass


        
    def makeShdowShader(self):
        shdow_obj = cmd.ls(sl=True)
        timeaxis_shadow= cmd.createNode ('aiShadowCatcher',name='timeaxis_shadow')
        cmd.select(shdow_obj)
        cmd.hyperShade( assign=timeaxis_shadow )#缁欑墿浣撴潗璐
        newsdSg = cmd.sets(renderable=1,empty=1,name='sdSG')
        cmd.connectAttr(timeaxis_shadow+'.outColor',newsdSg+'.surfaceShader',f=1)
        cmd.sets(shdow_obj,e=1,forceElement=newsdSg)



####################################################################################
#####################        render window             #############################
####################################################################################  
    def renderwindowgru(self):
        
        self.displayRenderWinGro= QtGui.QGroupBox("")
        
        self.disWinbtn = QtGui.QPushButton('Show Render Window')
        
        displayWinLayout = QtGui.QGridLayout()
        
        displayWinLayout.addWidget(self.disWinbtn,2,0,1,1)

        self.displayRenderWinGro.setLayout(displayWinLayout)
        
        self.connect(self.disWinbtn, QtCore.SIGNAL('clicked()'), self.remakeRenderUi)


    def remakeRenderUi(self):
        if cmds.window("unifiedRenderGlobalsWindow",exists=True):
            cmds.deleteUI("unifiedRenderGlobalsWindow")
        mel.eval("unifiedRenderGlobalsWindow;")  
        #pm.mel.deleteUI('unifiedRenderGlobalsWindow')
        #pm.mel.buidNewSceneUI()
        #pm.mel.RenderGlobalsWindow()
def getAllLights():
    allLights=[]
    if cmd.getAttr("defaultRenderGlobals.currentRenderer")=='arnold':
        light_node = ['ambientLight','directionalLight','pointLight','spotLight','areaLight','volumeLight','aiAreaLight','aiSkyDomeLight','aiPhotometricLight']
        for node in light_node:
            for ev_light in cmd.ls(type=node):
                allLights.append(ev_light)

    elif cmd.getAttr("defaultRenderGlobals.currentRenderer")=='redshift':
        light_node = ['ambientLight','directionalLight','pointLight','spotLight','areaLight','volumeLight','RedshiftPhysicalLight','RedshiftDomeLight']
        for node in light_node:
            for ev_light in cmd.ls(type=node):
                allLights.append(ev_light)
    return allLights 
    #light_node = ['ambientLight','directionalLight','pointLight','spotLight','areaLight','volumeLight','aiAreaLight','aiSkyDomeLight','aiPhotometricLight','RedshiftPhysicalLight','RedshiftDomeLight']
 

def getSelectedLights(*args ):
    if cmd.getAttr("defaultRenderGlobals.currentRenderer")=='arnold':
        selectedLights =cmd.ls(sl=1, type=['ambientLight','directionalLight','pointLight','spotLight','areaLight','volumeLight','aiAreaLight','aiSkyDomeLight','aiPhotometricLight'], dag =1)
    elif cmd.getAttr("defaultRenderGlobals.currentRenderer")=='redshift':
        selectedLights =cmd.ls(sl=1, type=['ambientLight','directionalLight','pointLight','spotLight','areaLight','volumeLight','RedshiftPhysicalLight','RedshiftDomeLight'], dag =1)
    return selectedLights    
def maya_ui():
    dialog = Dialog(parent=maya_main_window())   
if __name__ == '__main__':
    maya_ui()


