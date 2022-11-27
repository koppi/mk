import os
import subprocess

# print("koppi-cnc-axis-ui.py os.getcwd() %s" % (os.getcwd()))

root_window.tk.call(pane_bottom+".t.text","configure"
,"-foreground","white")

root_window.tk.call(pane_bottom+".t.text","configure"
,"-background","black")

root_window.bind("<Control-q>", "destroy .")
help2.append(("Control-Q", "Quit"))

subprocess.Popen(["./koppi-cnc-axis-startup.sh"])

######################################################################
# the following is experimental and does not work reliably
######################################################################

# home all axes at startup  ( not working at all )
#ensure_mode(linuxcnc.MODE_MANUAL)
#c.wait_complete()
#commands.home_all_joints()

