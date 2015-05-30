import subprocess


root_window.tk.call(pane_bottom+".t.text","configure"
,"-foreground","white")

root_window.tk.call(pane_bottom+".t.text","configure"
,"-background","black")

root_window.bind("<Control-q>", "destroy .")
help2.append(("Control-Q", "Quit"))

######################################################################
# the following is experimental and does not work reliably
######################################################################

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

subprocess.Popen(["koppi-cnc-axis-startup.sh"])
