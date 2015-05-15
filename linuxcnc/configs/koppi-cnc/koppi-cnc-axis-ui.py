from subprocess import call

root_window.tk.call(pane_bottom+".t.text","configure"
,"-background","black")
root_window.tk.call(pane_bottom+".t.text","configure"
,"-foreground","white")

root_window.bind("<Control-q>", "destroy .")
help2.append(("Control-Q", "Quit"))

# disable estop at startup
call(["halcmd", "setp", "halui.estop.reset", "1"])
call(["halcmd", "setp", "halui.estop.reset", "0"])

# enable machine at startup
call(["halcmd", "setp", "halui.machine.on", "1"])

# home all axes at startup ( not working )
#ensure_mode(linuxcnc.MODE_MANUAL)
#c.wait_complete()
#commands.home_all_axes()
