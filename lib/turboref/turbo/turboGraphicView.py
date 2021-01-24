from PyQt5 import QtCore, QtWidgets, QtGui
from turbo.turboGraphicItem import TurboImageItem, TurboTextItem
import sys, math

def scaleModifier():
    if sys.platform == "darwin":
        return QtCore.Qt.AltModifier
    return QtCore.Qt.ControlModifier

class ContextMenus:
    
    def __init__(self, graphicView):
        self.graphicView = graphicView

    def hoverOverItemContextMenu(self, contextMenuEvent, menu):
        item = self.graphicView.scene().selectedItems()[0]
        if isinstance(item, TurboTextItem):
            edit = menu.addAction("edit_",  self.testContextMenuAction)



    def selectedItemsContextMenu(self, contextMenuEvent, menu):
        menu.addSection("selection")
        delete = menu.addAction("delete_",  self.testContextMenuAction)
        group = menu.addAction("group_",  self.testContextMenuAction)

    def generalContextMenu(self, contextMenuEvent):
        menu = QtWidgets.QMenu(self.graphicView)
        moreSubMenusThanOne = False
        if len(self.graphicView.scene().selectedItems()) == 1:
            self.hoverOverItemContextMenu(contextMenuEvent, menu)
            moreSubMenusThanOne = True

        if len(self.graphicView.scene().selectedItems()) >= 1:
            self.selectedItemsContextMenu(contextMenuEvent, menu)
            moreSubMenusThanOne = True

        if moreSubMenusThanOne:
            menu.addSeparator()
        
        self.standardContextMenu(contextMenuEvent, menu)

        action = menu.exec_(self.graphicView.mapToGlobal(contextMenuEvent.pos()))

    def standardContextMenu(self, contextMenuEvent, menu):
        selectAll = menu.addAction("select all",  self.selectAllContextMenuAction)
        testAction = menu.addAction("debug",  self.testContextMenuAction)
        quitAction = menu.addAction("Quit", self.quitContextMenuAction)
        
    def selectAllContextMenuAction(self):
        for item in self.graphicView.scene().items():
            item.setSelected(True)

    def testContextMenuAction(self):
        print("test")

    def quitContextMenuAction(self):
        QtWidgets.qApp.quit()

class TurboGraphicView(QtWidgets.QGraphicsView):

    scaleChanged = QtCore.pyqtSignal(int)
    rectChanged = QtCore.pyqtSignal(QtCore.QRect)

    def __init__(self, scene, **kwargs):
        super().__init__(scene, **kwargs)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30.5, 30.5, 30.5))) # background color
        
        self.setMouseTracking(True)
        self.grabGesture(QtCore.Qt.PinchGesture)
        self._drawingOffset = QtCore.QPoint()
        self._scale = 1.0
        self._inverseScale = 0.1
        self.windowIsMoving = False # attr needed for dragging window
        self.windowRecievingDragAction = False # attr needed for dragging window
        self.m_nMouseClick_X_Coordinate, self.m_nMouseClick_Y_Coordinate = (0, 0)
        self.rubberBand = QtWidgets.QRubberBand(
            QtWidgets.QRubberBand.Rectangle, self)
        self.origin = QtCore.QPoint()
        self.changeRubberBand = False
        self.allowRubberBand = True

        self.rectChanged.connect(self.selectionRectChanged)   



    # -------------------------------------------
    # slots/signals
    # -------------------------------------------

    def timeForContextMenuIsOut(self):
        if self.windowRecievingDragAction:
            self.windowIsMoving = True

    # -------------------------------------------
    # events
    # -------------------------------------------

    def mousePressEvent(self, event):
        
        if event.button() == QtCore.Qt.MidButton:
            self.allowRubberBand = False
            self.setDragMode(self.ScrollHandDrag)
            self.original_event = event
            handmade_event = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonPress,QtCore.QPointF(event.pos()),QtCore.Qt.LeftButton,event.buttons(),QtCore.Qt.KeyboardModifiers())
            self.mousePressEvent(handmade_event)

        
        elif event.button() == QtCore.Qt.LeftButton and not self.scene().isCursorHovering and self.allowRubberBand:
            self.origin = event.pos()
            self.rubberBand.setGeometry(QtCore.QRect(self.origin, QtCore.QSize()))
            self.rectChanged.emit(self.rubberBand.geometry())      
               
            self.rubberBand.show()
            self.changeRubberBand = True
            return
            # QtWidgets.QGraphicsView.mousePressEvent(self, event)
        elif event.button() == QtCore.Qt.RightButton:
            # move Window
            self.m_nMouseClick_X_Coordinate = event.x()
            self.m_nMouseClick_Y_Coordinate = event.y()
            self.windowRecievingDragAction = True
            QtCore.QTimer.singleShot(150,self.timeForContextMenuIsOut)

        super(TurboGraphicView, self).mousePressEvent(event)
    def selectionRectChanged(self, geometry):
        selectionPath = QtGui.QPainterPath()
        selectionRect = self.mapToScene(geometry)
        selectionPath.addPolygon(selectionRect)
        self.scene().setSelectionArea( selectionPath )
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.changeRubberBand = False
            self.rubberBand.hide()
            QtWidgets.QGraphicsView.mouseReleaseEvent(self,event)

        if event.button() == QtCore.Qt.MidButton:
            self.setDragMode(self.NoDrag)
            handmade_event = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonRelease,QtCore.QPointF(event.pos()),QtCore.Qt.LeftButton,event.buttons(),QtCore.Qt.KeyboardModifiers())
            self.mouseReleaseEvent(handmade_event)
        elif event.button() == QtCore.Qt.RightButton:
            
            # shows the right click context menu
            # only if the window is not being dragged
            if self.windowIsMoving:
                self.windowIsMoving = False
                self.windowRecievingDragAction = False
            else:
                self.buildRightClickMenu(event)
        self.allowRubberBand = True

        super(TurboGraphicView, self).mouseReleaseEvent(event)
        
    def mouseMoveEvent(self, event):
        if self.changeRubberBand:
            self.rubberBand.setGeometry(QtCore.QRect(self.origin, event.pos()).normalized())
            self.rectChanged.emit(self.rubberBand.geometry())
            QtWidgets.QGraphicsView.mouseMoveEvent(self,event)

        if self.windowIsMoving:
            self.window().move(event.globalX() - self.m_nMouseClick_X_Coordinate, event.globalY()-self.m_nMouseClick_Y_Coordinate)

        super(TurboGraphicView, self).mouseMoveEvent(event)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Alt:
            # pan action
            self.setInteractive(False)
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
    
    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Alt:
            # pan action
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self.setInteractive(True)

    # -------------------------------------------
    # right click menu
    # -------------------------------------------
    
    def buildRightClickMenu(self, contextMenuEvent):
        self.windowRecievingDragAction = False
        contextMenuSystem = ContextMenus(self)
        if False:
            pass
        else:
            contextMenuSystem.generalContextMenu(contextMenuEvent)

        
    # -------------------------------------------
    # public methods
    # -------------------------------------------

    def getScale(self):
        return self._scale

    def resetScale(self):
        zoomFactor = self._inverseScale
        self.scale(zoomFactor, zoomFactor)
        self.setScale(zoomFactor * self._scale)

    def setScale(self, scale):
        self._scale = scale
        if self._scale <= 0:
            self._scale = 0.01
        self._inverseScale = 1.0 / self._scale
        self.scaleChanged.emit(scale)
        self.update()


    def wheelEvent(self, event):
        
        # Zoom Factor
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor

        # Set Anchors
        self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
        self.setResizeAnchor(QtWidgets.QGraphicsView.NoAnchor)

        # Save the scene pos
        oldPos = self.mapToScene(event.pos())

        # Zoom
        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor
        # self.setScale(self._scale*zoomFactor)
        
        self.scale(zoomFactor, zoomFactor)
        self.setScale(zoomFactor * self._scale)

        # Get the new position
        newPos = self.mapToScene(event.pos())

        # Move scene to old position
        # delta = newPos - oldPos
        delta = newPos - oldPos
        self.translate(delta.x(), delta.y())

        # self._scale *= zoomFactor

"""
filtering move event for main window
https://stackoverflow.com/questions/35570802/moving-dragging-a-framelesswindow-qt
"""
#     bool myApp::eventFilter(QObject *obj, QEvent *event)
# {
#   if (obj == ui->pushButton && event->type()==QMouseEvent::MouseButtonPress){
#     QMouseEvent *mouseEvent = static_cast<QMouseEvent*>(event);
# //    m_nMouseClick_X_Coordinate = mouseEvent->x() + 100;
# //    m_nMouseClick_Y_Coordinate = mouseEvent->y() + 90;
#     absPosX = ui->pushButton->mapToParent(QPoint(0,0)).x();
#     absPosY = ui->pushButton->mapToParent(QPoint(0,0)).y();
#     m_nMouseClick_X_Coordinate = mouseEvent->x() + absPosX;
#     m_nMouseClick_Y_Coordinate = mouseEvent->y() + absPosY;
#     return true;
#   }
#   return false;
# }

