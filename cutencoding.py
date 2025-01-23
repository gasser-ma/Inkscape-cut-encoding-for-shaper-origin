#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) [2023] [Matthias Gasser], [matti@hosli.ch]
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

import inkex

#from inkex import paths
from inkex import utils


class set_cut_encodings(inkex.Effect):
    elem_type = ["circle", "ellipse", "line", "path", "polygon", "polyline", "rect"]
    cut_types_stroke_colors = {"int":"#000000", "ext":"#000000", "online":"#969696","poc":"none","guide_f":"none","guide_s":"#0000ff","guide_a":"none"}
    cut_types_fill_colors = {"int":"#ffffff", "ext":"#000000", "online":"none","poc":"#969696","guide_f":"#0000ff","guide_s":"none","guide_a":"#FF0000"}
    #units = {"1":"mm","2":"in"}
    
    def __init__(self):
        inkex.Effect.__init__(self)
        pass
        
    def add_arguments(self, pars):
        pars.add_argument("--tab", type=str, default="page_cut_encoding")
        pars.add_argument("--set_cut_type", type=inkex.Boolean, default=False)
        pars.add_argument("--types", type=str, default="int")
        pars.add_argument("--check_path_close", type=inkex.Boolean, default=True)
        pars.add_argument("--try_path_close", type=inkex.Boolean, default=False)
        pars.add_argument("--set_stroke_width", type=inkex.Boolean, default=False)
        pars.add_argument("--stroke_width", type=str, default="0.01")
        
        pars.add_argument("--cut_depth", type=str, default="1")
        pars.add_argument("--cut_depth_mm", type=str, default="1")

        pars.add_argument("--cut_Offset", type=str, default="1")
        pars.add_argument("--cut_Offset_mm", type=str, default="0")

        pars.add_argument("--tool_Dia", type=str, default="1")
        pars.add_argument("--tool_Dia_mm", type=str, default="8")

        pars.add_argument("--unit", type=str, default="mm")
        pass

    def effect(self):
        self.iterator(self.svg.selection)
        pass

    def iterator(self, e):
        # if e is group --> cals itself
        for elem in e:
            #
            if str(elem) in self.elem_type:
                #
                if self.options.set_cut_type == True:
                    self.setCutType(elem)
                    pass
                #
                if self.options.check_path_close == True and str(elem)=="path":
                    self.checkPathClose(elem)
                    pass
                #
                if self.options.set_stroke_width == True:
                    self.setStrokeWidth(elem)
                    pass
                #
                if self.options.cut_depth == "1":
                    pass
                elif self.options.cut_depth == "2":
                    self.setCutDepth(elem)
                    pass
                elif self.options.cut_depth == "3":
                    for a in elem.attrib:
                        if "cutDepth" in a:
                            #utils.errormsg(a)
                            elem.pop(a)
                            pass
                        pass
                    #utils.errormsg(elem.attrib)
                    pass
                #
                if self.options.cut_Offset == "1":
                    pass
                elif self.options.cut_Offset == "2":
                    self.setCutOffset(elem)
                    pass
                elif self.options.cut_Offset == "3":
                    for a in elem.attrib:
                        if "cutOffset" in a:
                            elem.pop(a)
                            pass
                        pass
                    pass
                #
                if self.options.tool_Dia == "1":
                    pass
                elif self.options.tool_Dia == "2":
                    self.setToolDia(elem)
                    pass
                elif self.options.tool_Dia == "3":
                    for a in elem.attrib:
                        if "toolDia" in a:
                            elem.pop(a)
                            pass
                        pass
                    pass
                #
                pass
            elif str(elem) == "g":
                self.iterator(elem)
                pass
            else:
                #is not in list
                utils.errormsg("selected element not changed")
                utils.errormsg("Element ID is: " + str(elem.get('id')) + "")
                utils.errormsg("Element is  " + str(elem.typename) + "")
                utils.errormsg("Please use one of:")
                utils.errormsg(str(self.elem_type))
                pass
        #next elem
        pass

    def setToolDia(self, elem):
        #
        unit = "mm"
        dia = "0"
        dia = round(float(self.options.tool_Dia_mm),1)
        url = "http://www.shapertools.com/namespaces/"
        elem.set(url + "shaper:toolDia", str(dia)+unit)
        pass

    def setCutOffset(self, elem):
        #
        unit = "mm"
        offset = "0"
        offset = round(float(self.options.cut_Offset_mm),1)
        url = "http://www.shapertools.com/namespaces/"
        elem.set(url + "shaper:cutOffset", str(offset)+unit)
        pass

    def setCutDepth(self, elem):
        #
        unit = "mm"
        depth = "0"
        depth = round(float(self.options.cut_depth_mm),1)
        url = "http://www.shapertools.com/namespaces/"
        elem.set(url + "shaper:cutDepth", str(depth)+unit)
        pass

    def setStrokeWidth(self, elem):
        strokeWidth = round(float(self.options.stroke_width),3)
        elem.style['stroke-width'] = strokeWidth
        pass

    def checkPathClose(self, elem):
        svg_tag_d = elem.get("d")
        svg_new_d = ""
        has_m = False
        has_z = True
        i=0
        for d in svg_tag_d:
            #
            if d.upper() =="M":
                has_m = True
                if has_z == True:
                    has_z = False
                    pass
                else:
                    utils.errormsg("no Z at " + str(i))
                    svg_new_d = svg_new_d + "Z "
                    pass
                pass
            else:
                pass
            if d.upper() == "Z":
                has_z = True
                if has_m==True:
                    has_m=False
                    pass
                else:
                    pass
                pass
            else:
                #
                pass
            pass
            svg_new_d = svg_new_d + d
            i=i+1
        pass
        if svg_tag_d[-1].upper()=="Z":
            pass
        else:
            svg_new_d = svg_new_d + " Z"
            pass
        if self.options.try_path_close == True:
            elem.path = svg_new_d
            pass
        pass

    def setCutType(self, elem):
        elem.style.set_color(self.cut_types_stroke_colors[self.options.types],'stroke')
        elem.style.set_color(self.cut_types_fill_colors[self.options.types],'fill')
        # end def 
        pass
    #
    # end class
    pass


        

    
if __name__ == '__main__':
    set_cut_encodings().run()
    pass
