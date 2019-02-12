import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
# from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar

from PlotWindow import PlotBox

class ZoomWindow():
    def __init__(self, parent, simulation, colormap, zoom_value=0):
        self.parent = parent
        self.simulation = simulation
        self.colormap = colormap
        self.zoom_value = zoom_value

        
        self.builder = Gtk.Builder()
        self.builder.add_from_file("./interfaces/zoom.glade")
        self.window = self.builder.get_object("wndZoom")
        self.statBar = self.builder.get_object("statBar")
        self.btnApplyZoom = self.builder.get_object("btnApplyZoom")
        self.txtZoomValue = self.builder.get_object("txtZoomValue")
        self.boxPlot = self.builder.get_object("boxPlot")
        self.menuColorMap = self.builder.get_object("menuColorMap")


        self.window.set_transient_for(self.parent.window)


        self.btnApplyZoom.connect("clicked", self.on_apply_zoom)

        self.plot = PlotBox(self, self.simulation, self.colormap, self.statBar, txtZoomValue=self.txtZoomValue)
        self.boxPlot.pack_start(self.plot.boxPlot, True, True, 0)

        # Get a list of the colormaps in matplotlib.  Ignore the ones that end with
        # '_r' because these are simply reversed versions of ones that don't end
        # with '_r'
        maps = sorted(m for m in pyplot.cm.datad if not m.endswith("_r"))

        firstitem = Gtk.RadioMenuItem(self.colormap)
        firstitem.set_active(True)
        firstitem.connect('activate', self.on_color_bar_menu, self.colormap)
        self.menuColorMap.append(firstitem)
        for name in maps:
            if name != self.colormap:
                item = Gtk.RadioMenuItem.new_with_label([firstitem], name)
                item.set_active(False)
                item.connect('activate', self.on_color_bar_menu, name)
                self.menuColorMap.append(item)


        self.window.show_all()

        self.zoom = 100.0
        self.txtZoomValue.set_text(str(self.zoom))
        self.btnApplyZoom.emit("clicked")



    def on_apply_zoom(self, widget):
        self.zoom = float(self.txtZoomValue.get_text())
        print(self.zoom)
        zmin, zmax, ymin, ymax = self.plot.compute_zoom(self.zoom)
        self.plot.lblLabelInfo.set_text("Zoom = %s" % self.zoom)
        
        text = "Zoom = %s" % self.zoom
        if self.zoom <= 100:
            text = ""
        self.parent.plot.draw_rectangle(zmin, zmax, ymin, ymax, text)



    def on_color_bar_menu(self, widget, name):
        self.colormap = name
        self.plot.update_plot(name)