from subprocess import call

root_window.tk.call(pane_bottom+".t.text","configure"
,"-foreground","white")

root_window.tk.call(pane_bottom+".t.text","configure"
,"-background","black")

root_window.bind("<Control-q>", "destroy .")
help2.append(("Control-Q", "Quit"))

######################################################################
# the following is experimental and does not work reliably
######################################################################

# reset estop at startup    ( sometimes not working )
call(["halcmd", "setp", "halui.estop.reset", "1"])
call(["halcmd", "setp", "halui.estop.reset", "0"])

# enable machine at startup ( sometimes not working )
call(["halcmd", "setp", "halui.machine.on", "1"])

# home all axes at startup  ( not working at all )
#ensure_mode(linuxcnc.MODE_MANUAL)
#c.wait_complete()
#commands.home_all_axes()

# window fullscreen
# root_window.tk.call ("wm", "attributes", ".", "-fullscreen", "True")
# window maximized
root_window.tk.call ("wm", "attributes", ".", "-zoomed", "True")
# windows always top
#root_window.tk.call ("wm", "attributes", ".", "-topmost", "True")

# enable Z axis compensation at startup (not working at all)
#call(["axis-remote" ,"-m", "M64 P0"])
