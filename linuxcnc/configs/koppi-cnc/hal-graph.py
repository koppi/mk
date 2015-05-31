#!/usr/bin/env python2
#
# Interactive HAL Graph
#
# Copyright 2015 Jakob Flierl
#
# based on https://github.com/MachineryScience/Rockhopper/blob/master/MakeHALGraph.py
#
# this version differs to the above version in the following points:
#
# * it auto-refreshes the HAL data every five seconds
#
# * opens an interactive window (using a slightly modified version of xdot.py)
#
# * uses the pydot lib instead of the pygraphviz lib
#   (pygraphviz export seems to export dot files in a non-deterministic manner)

import os
import sys
import time
import math
import linuxcnc
import hal
import subprocess
import pydot

import gtk
import gtk.gdk

import xdot

import warnings

class HALAnalyzer( object ):
    def __init__(self ):
        self.Graph = pydot.Dot(graph_type='digraph', name="Hal graph",
                               rankdir='LR', splines='spline',
                               overlap='false', start='regular',
                               forcelabels='true')
                
    def parse_comps( self ):
        p = subprocess.Popen(['halcmd', '-s', 'show', 'comp'],
                             stderr=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=(1024*64))
        
        raw = p.communicate()[0].split( '\n' )
        components = [ filter( lambda a: a != '', [x.strip() for x in line(' ')] ) for line in raw ]
        
        self.component_dict = {}
        
        for c in components:
            if len(c) == 4:
                c.append( c[3] )
                c[3] = ''
            if ( c[2].find( 'halcmd' ) != 0 ):
                #self.Graph.add_node( c[2] )
                self.component_dict[ c[2] ] = c
           
    def parse_pins( self ):
        p = subprocess.Popen(['halcmd', '-s', 'show', 'pin'],
                             stderr=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             bufsize=(1024*64))
        
        raw = p.communicate()[0].split( '\n' )
        pins = [ filter( lambda a: a != '', [x.strip() for x in line.split(' ')] ) for line in raw ]
        self.pin_group_dict = {}
        self.sig_dict = {}
        for p in pins:
            if len(p) > 5:
                # if there is a signal listed on this pin, make sure
                # that signal is in our signal dictionary
                if ( p[6] in self.sig_dict ):
                    self.sig_dict[ p[6] ].append( p )
                else:
                    self.sig_dict[ p[6] ] = [ p ]
                    self.Graph.add_node(pydot.Node(p[6],
                                                   label=p[6] + " (" + p[3] + ")",
                                                   shape='box',
                                                   style='dotted',
                                                   outputMode='nodesfirst'))

                pstr = p[4].split('.')
                pin_group_name = pstr[0]
                try:
                    if (len(pstr) > 2) and (int(pstr[1] > -1)):
                        pin_group_name = pstr[0] + '.' + pstr[1]
                except Exception, err:
                    pass
 
                if pin_group_name in self.pin_group_dict:
                    self.pin_group_dict[ pin_group_name ].append( p )
                else:
                    self.pin_group_dict[ pin_group_name ] = [ p ]

        # Add all the pins into their sub-graphs
        for pin_g_name, pin_g_val_array in self.pin_group_dict.iteritems():
            subg = pydot.Cluster('cluster_' + pin_g_name.replace(".","_").replace("-", "_"),
                                 label=pin_g_name, style='rounded' )
            
            #print 'GROUP: ', pin_g_name
            for pin_g_val in pin_g_val_array:
                #print '      ', pin_g_val[4]
                subg.add_node(pydot.Node(pin_g_val[4], label=pin_g_val[4],
                                         shape='box', style='filled', color='lightgrey' ))
            self.Graph.add_subgraph(subg)

        # Add all the edges to and from signals
        for sig_name, pin_g_val_array in self.sig_dict.iteritems():
            for pin_g_val in pin_g_val_array:
                if (pin_g_val[5] == '==>'):
                    self.Graph.add_edge(pydot.Edge( pin_g_val[4], sig_name, color='#0000E0' ))
                else:
                    self.Graph.add_edge(pydot.Edge( sig_name, pin_g_val[4] ))

    def write_svg( self, filename ):
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore",category=DeprecationWarning)
                output = self.Graph.create_svg(prog='dot' )
                f = open(filename, "w")
                f.write(output)
                f.close()
        except Exception, err:
            print err

    def to_string( self ):
        return self.Graph.to_string()

class HALGraphWindow(xdot.DotWindow):

    def __init__(self):
        xdot.DotWindow.__init__(self)
        self.base_title = "HAL Graph"
        self.set_filter("dot") # 'dot', 'neato', 'twopi', 'circo', 'fdp'
        self.widget.connect('clicked', self.on_url_clicked)
        self.analyzer = None
        self.reload()
        self.widget.zoom_to_fit()

    def reload(self):
        self.analyzer = HALAnalyzer()
        self.analyzer.parse_pins()
        self.set_dotcode(self.analyzer.to_string())
        self.textentry_changed(self.widget, self.textentry)

        self.queue_draw()

    def on_reload(self, action):
        self.reload()

    def on_url_clicked(self, widget, url, event):
        dialog = gtk.MessageDialog(
                parent = self, 
                buttons = gtk.BUTTONS_OK,
                message_format="%s clicked" % url)
        dialog.connect('response', lambda dialog, response: dialog.destroy())
        dialog.run()
        return True

    def timer(self):
        self.reload()
        return True

def main():
    if len(sys.argv) == 1:
        w = HALGraphWindow()
        w.connect('destroy', gtk.main_quit)
        gtk.timeout_add(5000, w.timer)
        gtk.main()
    elif len(sys.argv) == 2:
        a = HALAnalyzer()
        a.parse_pins()
        a.write_svg(sys.argv[1])
    else:
        print "usage: hal-graph.py (hal-graph.svg)"

if __name__ == '__main__':
    main()
