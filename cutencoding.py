#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) [2023] [Matthias Gasser], [matti@hosli.ch]
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
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
'''
https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d
'''

import inkex
inkex.NSS["1shaper"] = "http://www.shapertools.com/namespaces/shaper"


from tkinter import messagebox



class set_cut_encodings(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        pass
        
    def add_arguments(self, pars):
        pars.add_argument("--tab", type=str, default="page_cut_encoding")
        pars.add_argument("--set_cut_type", type=inkex.Boolean, default=False)
        pars.add_argument("--types", type=str, default="int")
        pars.add_argument("--set_stroke_width", type=inkex.Boolean, default=False)
        pars.add_argument("--stroke_width", type=str, default="0.01")
        pars.add_argument("--set_cut_depth", type=inkex.Boolean, default=False)
        pars.add_argument("--unit", type=str, default="1")
        pars.add_argument("--cut_depth_mm", type=str, default="1")
        pars.add_argument("--cut_depth_in", type=str, default="0.4")
        pass

    def effect(self):
        """
        
        """
        cut_types_stroke_colors = {"int":"#000000", "ext":"#000000", "online":"#969696","poc":"#969696","guide_f":"#0000ff","guide_s":"#0000ff"}
        cut_types_fill_colors = {"int":"none", "ext":"#000000", "online":"none","poc":"#969696","guide_f":"#0000ff","guide_s":"none"}
        units = {"1":"mm","2":"in"}
        if self.options.tab == "check_path":
            for elem in self.svg.selection.filter(inkex.PathElement):
                tagD = elem.get("d")
                #messagebox.showwarning("Warning", tagD)
                checked = self.check_path_closed(tagD,True)
                elem.set("d",checked["tag_d"])
                pass
            pass

        if self.options.tab == "page_cut_encoding":
            #
            for elem in self.svg.selection:
                cut_depth_possible = True
                if self.options.set_cut_type == True:
                    #
                    elem.style.set_color(cut_types_stroke_colors[self.options.types],'stroke')
                    elem.style.set_color(cut_types_fill_colors[self.options.types],'fill')
                    if (self.options.types).startswith("guide"):
                        cut_depth_possible = False
                        pass
                    pass
                if self.options.set_stroke_width == True:
                    strokeWidth = round(float(self.options.stroke_width),3)
                    elem.style['stroke-width'] = strokeWidth
                    pass
                if self.options.set_cut_depth == True:
                    if cut_depth_possible == True:
                        unit = units[self.options.unit]
                        depth = "0"
                        if self.options.unit == "1":
                            depth = round(float(self.options.cut_depth_mm),1)
                            pass
                        if self.options.unit == "2":
                            depth = round(float(self.options.cut_depth_in),3)
                            pass
                        elem.set("shaper:cutDepth", str(depth)+unit)
                        pass
                    else:
                        elem.pop('shaper:cutDepth')
                        messagebox.showwarning("Warning", "set cut depth encoding not set")
                        pass
                    pass
                pass
            pass
        #
        pass

    def check_path_closed(self,svg_tag_d, fix_it):
        #
        ret = {"tag_d":svg_tag_d,"end_Z": True}
        tag_d_fixed = svg_tag_d
        #
        startM = False
        tag_d_counter = 0
        #endeZ = False
        m2z_error = []
        for c in svg_tag_d:
            if c=="m" or c=="M":
                if startM == True:
                    # darf nicht true sein denn da fehlt ein ende Z
                    # hier könnte ein fix eingebaut werden
                    m2z_error.append(tag_d_counter)
                    pass
                else:
                    startM = True
                    pass
                pass
            else:
                pass
            if c=="z" or c=="Z":
                if startM == True:
                    #endeZ = True
                    startM = False
                    pass
                else:
                    #
                    pass
                pass
            else:
                pass
            tag_d_counter += 1
            # next c
            pass
        #kontrolle auf ende Z
        if startM == True:
            # start ist immer noch true-- somit kein Ende Z
            m2z_error.append(tag_d_counter)
            pass
        else:
            pass
        messagebox.showinfo("inof","erros on " + str(m2z_error))
        #
        if fix_it == True:
            if len(m2z_error) > 0:
                m2z_error.sort(reverse=True) # umkehren von hinten beginnen
                for i in m2z_error:
                    tag_d_fixed = tag_d_fixed[:i] + " z " + tag_d_fixed[i:]
                    pass
                ret["tag_d"] = tag_d_fixed
                pass
            else:
                pass
            pass
        else:
            pass
        messagebox.showinfo("inof","fixed " + str(tag_d_fixed))
        return ret
        pass

if __name__ == '__main__':
    set_cut_encodings().run()
    pass
