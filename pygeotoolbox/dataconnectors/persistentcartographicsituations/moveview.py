from PyQt4.QtGui import *
from PyQt4.QtCore import *

def doPrint(minX, minY, maxX, maxY, fileName):
	print "Saving map..."

	print "\tCreating output image"
	img = QImage(QSize(600, 600), QImage.Format_ARGB32_Premultiplied)
	color = QColor(255, 255, 255)
	img.fill(color.rgb())

	print "\tCreating painter"
	p = QPainter()
	p.begin(img)
	p.setRenderHint(QPainter.Antialiasing)

	print "\tCreating renderer"
	render = QgsMapRenderer()

	if False:
		lst = [iface.activeLayer()]
	else:
		layers = qgis.utils.iface.legendInterface().layers()
		layers = QgsMapLayerRegistry.instance().mapLayers()
    #lst = []
    #for layer in layers:
        #lst.append(layer)
        #print "Layer:", layer.name

	print "\tSetting layer set"
	print "\t", QgsMapLayerRegistry.instance().mapLayers().keys()
	render.setLayerSet(QgsMapLayerRegistry.instance().mapLayers().keys())

	print "\tSetting extent"
	if False:
		rect = QgsRectangle(render.fullExtent())
	else:
		rect = QgsRectangle(minX, minY, maxX, maxY)
	#rect.scale(1.1)
	render.setExtent(rect)
	print "\tExtent:", rect.asWktCoordinates()

	print "\tSetting output size"
	render.setOutputSize(img.size(), img.logicalDpiX())

	# do the rendering
	render.render(p)

	p.end()

	print "\tSaving image"
	img.save("c:/temp/" + fileName + ".png","png")
	print "Done."

print "Move view"
#import PIL
#import printtobitmap

extent = iface.mapCanvas().extent()

for step in range(1):
    extent.set(extent.xMinimum()+ 100.0, extent.yMinimum() + 100.0, extent.xMaximum() + 100.0, extent.yMaximum() + 100.0)
    #iface.mapCanvas().setExtent(extent)
    #iface.mapCanvas().refresh ()
    print iface.mapCanvas().extent().toString()
    doPrint(extent.xMinimum(), extent.yMinimum(), extent.xMaximum(), extent.yMaximum(), "saved_" + str(step))
