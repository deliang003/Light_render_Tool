#coding=utf-8
import sys
import os
import re
import time
#from PySide import QtCore, QtWidgets
from PySide2 import QtWidgets,QtCore
import maya.cmds as cmd
import maya.mel as mm
import pymel.core as pm
import mtoa.aovs as aovs
globIsoFlag=[]

WINDOW_NAME = 'Tool'
def maya_main_window():
    import maya.OpenMayaUI as apiUI
    from shiboken2 import wrapInstance
    main_win_ptr = apiUI.MQtUtil.mainWindow()
    return wrapInstance(long(main_win_ptr), QtWidgets.QDialog)
    
class Dialog(QtWidgets.QDialog):

    def __init__(self, parent=None, show=True):
        super(Dialog, self).__init__(parent=parent)
        self.mainLayout = QtWidgets.QGridLayout(self)
        
        self.CopyTransformBox()
        self.IsoBox()
        self.workSpace()
        self.setAOVGroup()
        
        self.openFileBox()
        
        self.mainLayout.addWidget(self.CopyTransformGBox,0,0,1,2)
        self.mainLayout.addWidget(self.IsoGBox,1,0,1,2)
        self.mainLayout.addWidget(self.workSpaceGroup,2,0,1,1)
        self.mainLayout.addWidget(self.aovGoup,2,1,1,1)
        
        self.mainLayout.addWidget(self.openFPath,3,0,1,1)

        self.setLayout(self.mainLayout)



        if show:
            self.show()

####################################################################################
#####################        copy transform         ################################
####################################################################################


       
    def CopyTransformBox(self):

        self.CopyTransformGBox= QtWidgets.QGroupBox("COPY  TRANSFORM")
        self.allTr = QtWidgets.QPushButton('ALL')
        self.Tr_translate = QtWidgets.QPushButton('Translate')
        self.Tr_rotate = QtWidgets.QPushButton('Rotate')
        
        CopyTransformLayout = QtWidgets.QGridLayout()
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
        
        self.IsoGBox= QtWidgets.QGroupBox("Isolate Light  Tool")
        
        self.isolate = QtWidgets.QPushButton('Isolate Selection')
        self.lookthrought = QtWidgets.QPushButton('Look Throught')
        self.clean = QtWidgets.QPushButton('clean')
        
        IsoLayout = QtWidgets.QGridLayout()
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
#####################        set workspace             #############################
####################################################################################              

                
    def workSpace(self):
        
        self.workSpaceGroup = QtWidgets.QGroupBox("Work Space Group")
        self.workSpbtn = QtWidgets.QPushButton('Aronld Work Space')
        spbtnLayout = QtWidgets.QGridLayout()
        spbtnLayout.addWidget(self.workSpbtn,0,0,1,1)
        
        self.workSpaceGroup.setLayout(spbtnLayout)
        
        
        
        self.connect(self.workSpbtn, QtCore.SIGNAL('clicked()' ), self.setArWorkSp)
    def setArWorkSp(self): 
        if not cmd.pluginInfo('mtoa',l=True,q=True):
            cmd.loadPlugin('mtoa')
        if cmd.getAttr('defaultRenderGlobals.currentRenderer') !='arnold':
            cmds.setAttr('defaultRenderGlobals.currentRenderer',l=False)
            cmds.setAttr('defaultRenderGlobals.currentRenderer','arnold',type = 'string')
            print"Arnold Render Is Load"
            self.ArSet()
        else:
            self.ArSet()
    def ArSet(self):
        drg = pm.PyNode('defaultRenderGlobals')
        cmd.setAttr ('defaultRenderGlobals.imageFilePrefix',"<Scene>/<RenderLayer>/<RenderLayer>",type="string")
        
        #drg.imageFilePrefix.set('exr')
        pm.mel.setMayaSoftwareFrameExt(7,0)
        cmd.setAttr ("defaultRenderGlobals.extensionPadding",3)
        cmd.setAttr ("defaultRenderGlobals.extensionPadding" ,4)
        cmd.setAttr ("defaultArnoldRenderOptions.AASamples", 2)
        cmd.setAttr ("defaultArnoldRenderOptions.GIDiffuseSamples", 3)
        cmd.setAttr ("defaultArnoldRenderOptions.GIDiffuseSamples" ,2)
        cmd.setAttr ("defaultArnoldRenderOptions.GIGlossySamples" ,3)
        cmd.setAttr ("defaultArnoldRenderOptions.GIGlossySamples", 2)
        cmd.setAttr ("defaultArnoldRenderOptions.GIRefractionSamples" ,3)
        cmd.setAttr ("defaultArnoldRenderOptions.GIRefractionSamples" ,2)
        cmd.setAttr ("defaultArnoldRenderOptions.GISssSamples" ,3)
        cmd.setAttr ("defaultArnoldRenderOptions.GISssSamples" ,2)
        cmd.setAttr ("defaultArnoldRenderOptions.GIVolumeSamples" ,3)
        cmd.setAttr ("defaultArnoldRenderOptions.GIVolumeSamples",2)
        cmd.setAttr ("defaultArnoldRenderOptions.display_gamma",2.2)
        cmd.setAttr ("defaultArnoldRenderOptions.use_existing_tiled_textures" ,1)
        cmd.setAttr ("defaultArnoldRenderOptions.bucketSize" ,32)
        cmd.setAttr ("defaultArnoldRenderOptions.bucketScanning" ,4)
        cmd.setAttr ("defaultArnoldRenderOptions.abortOnError" ,0)
        cmd.setAttr ("defaultArnoldRenderOptions.log_max_warnings", 100)
        cmd.setAttr ("defaultArnoldRenderOptions.log_to_console", 0)
        cmd.setAttr ("defaultArnoldDriver.mergeAOVs", 1)
        cmd.setAttr ("defaultArnoldRenderOptions.motion_blur_enable", 1)
        cmd.setAttr ("defaultArnoldRenderOptions.range_type", 0)
        cmd.setAttr ("defaultArnoldRenderOptions.motion_blur_enable" ,0)
        cmd.setAttr ("defaultArnoldRenderOptions.GIRefractionDepth" ,1)
        cmd.setAttr ("defaultArnoldRenderOptions.GIReflectionDepth" ,1)
        cmd.setAttr ("defaultArnoldRenderOptions.GITotalDepth" ,10)
        
####################################################################################
#####################        make aov                  #############################
####################################################################################          
     
    def setAOVGroup(self):
        self.aovGoup= QtWidgets.QGroupBox("aov")
        
        self.aov = QtWidgets.QPushButton('AOV')
        
        aovLayout = QtWidgets.QGridLayout()
        aovLayout.addWidget(self.aov,2,0,1,1)

        self.aovGoup.setLayout(aovLayout)
     
        self.connect(self.aov, QtCore.SIGNAL('clicked()'),self.makeAOV)
    def makeAOV(self):  
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

####################################################################################
#####################        open pic path             #############################
####################################################################################               
                
    def openFileBox(self):
        
        self.openFPath= QtWidgets.QGroupBox("OPEN FILE")
        
        self.openFileBox = QtWidgets.QPushButton('OPEN FILE PATH')
        
        openLayout = QtWidgets.QGridLayout()
        openLayout.addWidget(self.openFileBox,2,0,1,1)

        self.openFPath.setLayout(openLayout)
        
        self.connect(self.openFileBox, QtCore.SIGNAL('clicked()' ), self.openPath)
    def openPath(self):  
        
        if os.path.exists(str(cmd.workspace( fn=True)+'/images')): 
            os.startfile(str(cmd.workspace( fn=True)+'/images'))
        else:
            os.startfile(str(cmd.workspace( fn=True)))
  

          

        
           
        
def getAllLights():
    allLights=[]
    if cmds.getAttr("defaultRenderGlobals.currentRenderer")=='arnold':
        light_node = ['ambientLight','directionalLight','pointLight','spotLight','areaLight','volumeLight','aiAreaLight','aiSkyDomeLight','aiPhotometricLight']
        for node in light_node:
            for ev_light in cmd.ls(type=node):
                allLights.append(ev_light)

    elif cmds.getAttr("defaultRenderGlobals.currentRenderer")=='redshift':
        light_node = ['ambientLight','directionalLight','pointLight','spotLight','areaLight','volumeLight','RedshiftPhysicalLight','RedshiftDomeLight']
        for node in light_node:
            for ev_light in cmd.ls(type=node):
                allLights.append(ev_light)
    return allLights 
    #light_node = ['ambientLight','directionalLight','pointLight','spotLight','areaLight','volumeLight','aiAreaLight','aiSkyDomeLight','aiPhotometricLight','RedshiftPhysicalLight','RedshiftDomeLight']
 

def getSelectedLights(*args ):
    if cmds.getAttr("defaultRenderGlobals.currentRenderer")=='arnold':
        selectedLights =cmd.ls(sl=1, type=['ambientLight','directionalLight','pointLight','spotLight','areaLight','volumeLight','aiAreaLight','aiSkyDomeLight','aiPhotometricLight'], dag =1)
    elif cmds.getAttr("defaultRenderGlobals.currentRenderer")=='redshift':
        selectedLights =cmd.ls(sl=1, type=['ambientLight','directionalLight','pointLight','spotLight','areaLight','volumeLight','RedshiftPhysicalLight','RedshiftDomeLight'], dag =1)
    return selectedLights    
def maya_ui():
    dialog = Dialog(parent=maya_main_window())   
if __name__ == '__main__':
    maya_ui()


