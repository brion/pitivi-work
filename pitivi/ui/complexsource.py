#!/usr/bin/python
# PiTiVi , Non-linear video editor
#
#       pitivi/ui/timeline.py
#
# Copyright (c) 2005, Edward Hervey <bilboed@bilboed.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import gtk
import gst
import cairo
import gc

from pitivi.timeline import TimelineSource, MEDIA_TYPE_VIDEO, MEDIA_TYPE_AUDIO
from complexinterface import ZoomableWidgetInterface

# TODO : We might need an abstract class for ComplexTimelineObjects....

class ComplexTimelineSource(gtk.Image, ZoomableWidgetInterface):
    __gsignals__ = {
        "size-request":"override",
        "size-allocate":"override",
        }

    modelclass = TimelineSource

    def __init__(self, source, layerInfo):
        gtk.Image.__init__(self)
        self.layerInfo = layerInfo
        self.source = source
        self.source.connect("start-duration-changed", self._start_duration_changed_cb)
        self.thumbnailsurface = cairo.ImageSurface.create_from_png(self.source.factory.thumbnail)
        self.pixmap = None

    def get_height(self):
        # TODO, maybe this should be zoomable too ?
        return 50

    ## gtk.Widget overrides

    def do_size_allocate(self, allocation):
        changed = not (list(allocation) == list(self.allocation))
        gtk.Image.do_size_allocate(self, allocation)
        if changed:
            self.doPixmap()

    def do_size_request(self, requisition):
        gst.debug("source, requisition:%s" % list(requisition))
        requisition.width=self.get_pixel_width()

    ## Drawing methods

    def doPixmap(self):
        if not self.flags() & gtk.REALIZED:
            return
        rect = self.get_allocation()
        gst.debug("Source draw %s" % list(rect))

        if self.pixmap:
            del self.pixmap
            #gc.collect()
        self.pixmap = gtk.gdk.Pixmap(self.window, rect.width, rect.height)
        context = self.pixmap.cairo_create()
        
        self.draw_background(context, rect)

        if self.source.media_type == MEDIA_TYPE_VIDEO:
            self.draw_thumbnail(context, rect)

        self.draw_decoration_border(context, rect)
        self.set_from_pixmap(self.pixmap, None)

    def draw_background(self, context, allocation):
        context.save()
        context.set_source_rgb(1.0, 0.9, 0.9)
        context.rectangle(0, 0, allocation.width, allocation.height)
        context.fill()
        context.stroke()
        context.restore()
        
    def draw_decoration_border(self, context, rect):
        context.set_source_rgb(1, 0, 0)
        context.rectangle(0, 0, rect.width, rect.height)
        context.stroke()
        

    def draw_thumbnail(self, context, alloc):
        context.save()
        # figure out the scaleratio
        surfwidth = self.thumbnailsurface.get_width()
        surfheight = self.thumbnailsurface.get_height()
        widthratio = float(alloc.width - 10) / float(surfwidth)
        heightratio = float(alloc.height - 10) / float(surfheight)
        ratio = min(widthratio, heightratio)

        context.scale(ratio, ratio)
        context.set_source_surface(self.thumbnailsurface,
                                   ((alloc.width / ratio) - surfwidth) / 2 ,
                                   5 / ratio)
        context.paint()

        context.restore()


    ## ZoomableWidgetInterface methods

    def get_duration(self):
        return self.source.duration

    def get_start_time(self):
        return self.source.start

    def _start_duration_changed_cb(self, source, start, duration):
        self.start_duration_changed()
