from subprocess import call

root_window.tk.call(pane_bottom+".t.text","configure"
,"-background","black")
<<<<<<< HEAD

=======
>>>>>>> db2527241f251c7c082fe5c6a38c069c59a166bd
root_window.tk.call(pane_bottom+".t.text","configure"
,"-foreground","white")

root_window.bind("<Control-q>", "destroy .")
help2.append(("Control-Q", "Quit"))

<<<<<<< HEAD
######################################################################
# the following is experimental and does not work reliably
######################################################################

# disable estop at startup  ( sometimes not working )
call(["halcmd", "setp", "halui.estop.reset", "1"])
call(["halcmd", "setp", "halui.estop.reset", "0"])

# enable machine at startup ( sometimes not working )
call(["halcmd", "setp", "halui.machine.on", "1"])

# home all axes at startup  ( not working at all )
=======
# disable estop at startup
call(["halcmd", "setp", "halui.estop.reset", "1"])
call(["halcmd", "setp", "halui.estop.reset", "0"])

# enable machine at startup
call(["halcmd", "setp", "halui.machine.on", "1"])

# home all axes at startup ( not working )
>>>>>>> db2527241f251c7c082fe5c6a38c069c59a166bd
#ensure_mode(linuxcnc.MODE_MANUAL)
#c.wait_complete()
#commands.home_all_axes()
