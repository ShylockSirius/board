# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import os.path
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import board.WhiteBoard.Whitezheng as zheng
import board.classification as classification
import board.WhiteBoard.WhitepixelDetection as whitepixelDetection
import board.BlackBoard.BlackpixelDetection as blackpixelDetection
from board.Camera.CameraCalled import *
from board.Camera.CameraFunction import *
from board.Camera.MvImport.MvCameraControl_class import *
from board.UI import Ui_MainWindow
import time
import cv2
from board.rect_location_back import *
from board.rect_location_front import *
from board.imgCompare import *
from board.junhenghua import *

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.fpi = False
        self.bpi = False
        self.cap = False
        self.fname = ""
        self.bname = ""
        self.xuan = 0
        self.indexclick = False
        self.revoke.hide()

    def clearUI(self):
        if self.fname != "" and self.bname != "":
            self.frontpic.clear()
            self.frontpic.setGeometry(QtCore.QRect(20, 70, self.width-170, (self.height-200-10)/2))
            self.frontpic.setStyleSheet("background-color:grey;")
            self.backpic.clear()
            self.backpic.setGeometry(QtCore.QRect(20, 80+(self.height-200-10)/2, self.width-170, (self.height-200-10)/2))
            self.backpic.setStyleSheet("background-color:grey;")
            self.result.clear()
            self.result.setGeometry(QtCore.QRect(self.width-140, 70, 120, self.height-200))
            self.result.setStyleSheet("background-color:grey;")

    @pyqtSlot()
    def indexpic(self):
        if self.indexclick == False:
            self.cla()
            if self.fname != "" or self.bname != "":
                self.index.setToolTip("保存")
                self.indexclick = True
                self.revoke.show()
                if self.fname != "":
                    markfrontpic(self.fname)
                    self.fname = ""
                if self.bname != "":
                    markbackpic(self.bname)
                    self.bname = ""
                self.clearUI()
        else:
            self.index.setToolTip("检测定位")
            self.indexclick = False
            a = QMessageBox.question(self, '保存', '是否要保存?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)  # "退出"代表的是弹出框的标题,"你确认退出.."表示弹出框的内容
            if a == QMessageBox.Yes:
                lu = os.path.abspath(__file__)
                lu, _ = os.path.split(lu)
                if self.xuan == 0:
                    if self.fname != "":
                        saveremarkfrontpic(lu + "/board/WhiteBoard/newimages/aaa.csv")
                    if self.bname != "":
                        saveremarkbackpic(lu + "/board/WhiteBoard/new1.csv")
                elif self.xuan == 1:
                    if self.bname != "":
                        saveremarkbackpic(lu + "/board/BlackBoard/location_black.csv")
            self.revoke.hide()

    @pyqtSlot()
    def revokeindex(self):
        a = QMessageBox.question(self, '撤销', '撤销不可恢复，你确定要撤销吗?', QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.No)  # "退出"代表的是弹出框的标题,"你确认退出.."表示弹出框的内容
        if a == QMessageBox.Yes:
            if self.fname != "":
                revokefrontpic()
            if self.bname != "":
                revokebackpic()

    @pyqtSlot()
    def print_value(self):
        if self.cb.currentIndex() == None or self.cb.currentIndex() == 0:
            self.xuan = 0
        elif self.cb.currentIndex() == 1:
            self.xuan = 1

    @pyqtSlot()
    def con(self):
        _translate = QtCore.QCoreApplication.translate
        if self.cap:
            self.contipic.setToolTip("开启连续拍照")
            self.camera_timer.stop()
            self.cap = False
            closecam(self.cam)
        else:
            self.lu = QFileDialog.getExistingDirectory(self, '选择存储位置', os.getcwd())
            if self.lu == "":
                return
            if self.xuan == 0:
                self.junlu = self.lu + "/whitejun"
                self.lu += "/whiteoriginal"
            elif self.xuan == 1:
                self.junlu = self.lu + "/blackjun"
                self.lu += "/blackoriginal"
            if os.path.exists(self.lu) == False:
                os.mkdir(self.lu)
            if os.path.exists(self.junlu) == False:
                os.mkdir(self.junlu)
            self.contipic.setToolTip("关闭连续拍照")
            self.opencam.setToolTip("开启手动拍照")
            self.cam = start_continue()
            self.cap = True
            self.interval = 0
            self.camera_timer = QtCore.QTimer()
            self.camera_timer.timeout.connect(self.continuspic)
            self.camera_timer.start(40)  # 每40毫秒读取一次
            self.continuspic()

    @pyqtSlot()
    def openphoto(self):
        _translate = QtCore.QCoreApplication.translate
        if self.cap:
            self.opencam.setToolTip("开启手动拍照")
            self.camera_timer.stop()
            self.cap = False
            closecam(self.cam)
        else:
            self.lu = QFileDialog.getExistingDirectory(self, '选择存储位置', os.getcwd())
            if self.lu == "":
                return
            if self.xuan == 0:
                self.junlu = self.lu + "/whitejun"
                self.lu += "/whiteoriginal"
            elif self.xuan == 1:
                self.junlu = self.lu + "/blackjun"
                self.lu += "/blackoriginal"
            if os.path.exists(self.lu) == False:
                os.mkdir(self.lu)
            if os.path.exists(self.junlu) == False:
                os.mkdir(self.junlu)
            self.opencam.setToolTip("关闭手动拍照")
            self.contipic.setToolTip("开启连续拍照")
            self.cam = start_photo()
            self.cap = True
            self.interval = 0
            self.camera_timer = QtCore.QTimer()
            self.camera_timer.timeout.connect(self.photoonce)
            self.camera_timer.start(40)  # 每40毫秒读取一次
            self.photoonce()

    def continuspic(self):
        # 主动取流方式抓取图像
        now_time = time.strftime('%Y_%m_%d-%H_%M_%S-', time.localtime())
        savepath = self.lu + "/" + now_time + str(self.interval) + ".jpg"
        self.junpath = self.junlu + "/" + now_time + str(self.interval) + ".jpg"
        access_get_image_change(self.cam, savepath, active_way="getImagebuffer")
        self.interval += 1
        if self.interval == 25:
            self.interval = 0
            if os.path.exists(savepath):
                junhenghua(savepath, self.junpath)
                savepath = self.junpath
                self.clearUI()
                self.classif(savepath)
                self.showresult()
        else:
            if os.path.exists(savepath):
                #print(savepath)
                os.remove(savepath)

    def photoonce(self):
        if self.interval > 0:
            self.interval += 1
        # 主动取流方式抓取图像
        now_time = time.strftime('%Y_%m_%d-%H_%M_%S', time.localtime())
        savepath = self.lu + "/" + now_time + ".jpg"
        self.junpath = self.junlu + "/" + now_time + ".jpg"
        access_get_image_change(self.cam, savepath, active_way="getImagebuffer")
        if os.path.exists(savepath):
            if self.interval == 0:
                self.interval = 1
                junhenghua(savepath, self.junpath)
                savepath = self.junpath
                self.clearUI()
                self.classif(savepath)
                self.showresult()
            elif self.interval == 3:
                self.interval = 0
            else:
                os.remove(savepath)

    def sfpic(self):
        _translate = QtCore.QCoreApplication.translate
        if self.cap:
            self.opencam.setText(_translate("MainWindow", "关闭摄像头"))
            self.camera_timer.stop()
            self.capture.release()
            self.frontpic.clear()
            self.frontpic.setGeometry(QtCore.QRect(20, 70, self.width-170, (self.height-200-10)/2))
            self.frontpic.setStyleSheet("background-color:grey;")
            self.cap = False
        else:
            self.opencam.setText(_translate("MainWindow", "关闭摄像头"))
            self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.cap += 1
            currentFrame = self.capture.get(cv2.CAP_PROP_POS_FRAMES)
            currentTime = self.capture.get(cv2.CAP_PROP_POS_MSEC)
            self.fps = int(currentFrame / (currentTime / 1000)) * 1
            self.interval = 0
            self.camera_timer = QtCore.QTimer()
            self.camera_timer.timeout.connect(self.show_image)
            self.camera_timer.start(40)  # 每40毫秒读取一次
            self.show_image()

    def show_image(self, lu):
        image = cv2.imread(lu)
        fimg = image
        ksize = fimg.shape
        w = ksize[1]  # 宽度
        h = ksize[0]  # 高度
        scale = min((self.width - 170) / w, ((self.height-200-10)/2) / h)
        Width = int(w * scale)
        Height = int(h * scale)  # 缩放宽高尺寸
        fimg = cv2.resize(fimg, (Width, Height))
        fimg = cv2.cvtColor(fimg, cv2.COLOR_BGR2RGB)
        fimg = QImage(fimg.data, Width, Height, Width * 3, QtGui.QImage.Format_RGB888)
        size = QSize(Width, Height)
        pixImg = QPixmap.fromImage(
            fimg.scaled(size, Qt.IgnoreAspectRatio))  # 修改图片实例大小并从QImage实例中生成QPixmap实例以备放入QLabel控件中
        self.frontpic.setGeometry(QtCore.QRect(20 + (self.width - 170) / 2 - Width / 2, 70 + (self.height-200-10)/2/2-Height/2,
                                               Width, Height))
        self.frontpic.setPixmap(pixImg)

    def fpic(self):
        #self.fname, _ = QFileDialog.getOpenFileName(self, '选择图片', 'f:/pythontest/board/newimages', 'Image files(*.jpg *.gif *.png *.jpeg *.bmp)')
        if self.fname != "":
            fimg = QImage(self.fname)
            self.fscale = min((self.width-170)/fimg.size().width(), ((self.height-200-10)/2)/fimg.size().height())
            self.fmgnWidth = int(fimg.size().width() * self.fscale)
            self.fmgnHeight = int(fimg.size().height() * self.fscale)  # 缩放宽高尺寸
            size = QSize(self.fmgnWidth, self.fmgnHeight)
            pixImg = QPixmap.fromImage(
                fimg.scaled(size, Qt.IgnoreAspectRatio))  # 修改图片实例大小并从QImage实例中生成QPixmap实例以备放入QLabel控件中
            self.frontpic.setGeometry(int(20+(self.width-170)/2-self.fmgnWidth/2), int(70+(self.height-200-10)/4-self.fmgnHeight/2),
                                      self.fmgnWidth, self.fmgnHeight)
            self.frontpic.setPixmap(pixImg)
            self.fpi = True

    def bpic(self):
        #self.bname, _ = QFileDialog.getOpenFileName(self, '选择图片', 'C:/Users/HP/Desktop', 'Image files(*.jpg *.gif *.png *.jpeg *.bmp)')
        if self.bname != "":
            bimg = QImage(self.bname)
            scale = min((self.width-170) / bimg.size().width(), ((self.height-200-10)/2) / bimg.size().height())
            self.bmgnWidth = int(bimg.size().width() * scale)
            self.bmgnHeight = int(bimg.size().height() * scale)  # 缩放宽高尺寸
            size = QSize(self.bmgnWidth, self.bmgnHeight)
            pixImg = QPixmap.fromImage(
                bimg.scaled(size, Qt.IgnoreAspectRatio))  # 修改图片实例大小并从QImage实例中生成QPixmap实例以备放入QLabel控件中
            self.backpic.setGeometry(int(20+(self.width-170)/2-self.bmgnWidth/2), int(80+(self.height-200-10)/2+(self.height-200-10)/4-self.bmgnHeight/2), self.bmgnWidth, self.bmgnHeight)
            self.backpic.setPixmap(pixImg)
            self.bpi = True

    def classif(self, name):
        if name != "":
            luu, lun = os.path.splitext(name)
            luu = luu + "_jun" + lun
            junhenghua(name, luu)
            name = luu
            #if classification.classi(name):
            if classifica(name):
                self.bname = name
                self.bpic()
            else:
                self.fname = name
                self.fpic()

    @pyqtSlot()
    def cla(self):
        name, _ = QFileDialog.getOpenFileName(self, '选择图片', 'C:/Users/HP/Desktop',
                                                    'Image files(*.jpg *.gif *.png *.jpeg *.bmp)')
        if name != "":
            self.clearUI()
        self.classif(name)

    def deletefolder(self, img):
        import os
        savepath, _ = os.path.split(img)
        os.remove(img)
        os.rmdir(savepath)

    @pyqtSlot()
    def showresult(self):
        _translate = QtCore.QCoreApplication.translate
        if self.fpi:
            #if self.xuan == 0:
            img, falg = zheng.fpicture(self.fname)
            if img == "":
                return
            fimg = QImage(img)
            size = QSize(self.fmgnWidth, self.fmgnHeight)
            pixImg = QPixmap.fromImage(
                fimg.scaled(size, Qt.IgnoreAspectRatio))  # 修改图片实例大小并从QImage实例中生成QPixmap实例以备放入QLabel控件中
            self.frontpic.setGeometry(int(20 + (self.width - 170) / 2 - self.fmgnWidth / 2), int(70+(self.height-200-10)/4-self.fmgnHeight/2),
                                      self.fmgnWidth, self.fmgnHeight)
            self.frontpic.setPixmap(pixImg)
            if falg:
                self.result.setText(_translate("MainWindow", "OK"))
                self.result.setStyleSheet("background-color:green;color:white;")
            else:
                self.result.setText(_translate("MainWindow", "NG"))
                self.result.setStyleSheet("background-color:red;color:white;")
            self.fpi = False
            #self.deletefolder(img)
        if self.bpi:
            print(self.xuan)
            if self.xuan == 0:
                img, falg = whitepixelDetection.whitebpicture(self.bname)
            elif self.xuan == 1:
                img, falg = blackpixelDetection.blackbpicture(self.bname)
                print(img)
            if img == "":
                return
            bimg = QImage(img)
            size = QSize(self.bmgnWidth, self.bmgnHeight)
            pixImg = QPixmap.fromImage(
                bimg.scaled(size, Qt.IgnoreAspectRatio))  # 修改图片实例大小并从QImage实例中生成QPixmap实例以备放入QLabel控件中
            self.backpic.setGeometry(int(20+(self.width-170)/2-self.bmgnWidth/2), int(80+(self.height-200-10)/2+(self.height-200-10)/4-self.bmgnHeight/2), self.bmgnWidth, self.bmgnHeight)
            self.backpic.setPixmap(pixImg)
            if falg:
                self.result.setText(_translate("MainWindow", "OK"))
                self.result.setStyleSheet("background-color:green;color:white;")
            else:
                self.result.setText(_translate("MainWindow", "NG"))
                self.result.setStyleSheet("background-color:red;color:white;")
            self.bpi = False
            #self.deletefolder(img)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    iniCamera()
    #initemp()
    sys.exit(app.exec_())