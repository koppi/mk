#!/usr/bin/env python

import sys
import time
import linuxcnc
import psycopg2
import hal
import logging
import getpass

# psql -c "create table log(id SERIAL PRIMARY KEY, time timestamp, task_mode int, file varchar(1024), line int, x_min float, x_max float, x_avg float, y_min float, y_max float, y_avg float, z_min float, z_max float, z_avg float);"
# psql -c "CREATE INDEX log_idx_time ON log (id, time, time DESC);"

work_thread = 5.0 # work_thread means how often pins will be updated (sec)

logging.basicConfig(stream=sys.stderr, level=logging.ERROR)
#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class Logger :
        def __init__(self) :
                logging.info("init")
                self.linuxcnc = linuxcnc
                self.stat     = self.linuxcnc.stat()
                self.con = None
                self.cur = None
                self.log_insert = "INSERT INTO log (time, task_mode, file, line, x_min, x_max, x_avg, y_min, y_max, y_avg, z_min, z_max, z_avg) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

                try:
                        self.con = psycopg2.connect(database=getpass.getuser(), user=getpass.getuser())
                        self.cur = self.con.cursor()
                        self.cur.execute('SELECT version()')
                        ver = self.cur.fetchone()
                        logging.debug(ver)
                except psycopg2.DatabaseError, e:
                        logging.error('%s' % e)
                        sys.exit(1)

                self.h = hal.component("data_logger")
                logging.info("ok")

        def run(self) :
                self.h.newpin("beat", hal.HAL_BIT, hal.HAL_OUT)
                self.h.newpin("error", hal.HAL_BIT, hal.HAL_OUT)
                self.h.newpin("enable", hal.HAL_BIT, hal.HAL_IN)

                self.h.newpin("line", hal.HAL_S32, hal.HAL_IN)

                self.h.newpin("i11", hal.HAL_FLOAT, hal.HAL_IN)
                self.h.newpin("i12", hal.HAL_FLOAT, hal.HAL_IN)
                self.h.newpin("i13", hal.HAL_FLOAT, hal.HAL_IN)

                self.h.newpin("i21", hal.HAL_FLOAT, hal.HAL_IN)
                self.h.newpin("i22", hal.HAL_FLOAT, hal.HAL_IN)
                self.h.newpin("i23", hal.HAL_FLOAT, hal.HAL_IN)

                self.h.newpin("i31", hal.HAL_FLOAT, hal.HAL_IN)
                self.h.newpin("i32", hal.HAL_FLOAT, hal.HAL_IN)
                self.h.newpin("i33", hal.HAL_FLOAT, hal.HAL_IN)
                self.h.ready()

                try:
                        while 1:
                                try:
                                        time.sleep(work_thread)
                                        self.h['beat'] = not self.h['beat']
                                        self.stat.poll()
                                        #for x in dir(self.stat):
                                        #        if not x.startswith('_'):
                                        #                print x, getattr(self.stat,x)

                                        t  = psycopg2.TimestampFromTicks(time.time())

                                        tm = getattr(self.stat, "task_mode")
                                        f  = getattr(self.stat, "file")
                                        l = self.h["line"]

                                        x_min = self.h["i11"]
                                        x_max = self.h["i12"]
                                        x_avg = self.h["i13"]
                                        y_min = self.h["i21"]
                                        y_max = self.h["i22"]
                                        y_avg = self.h["i23"]
                                        z_min = self.h["i31"]
                                        z_max = self.h["i32"]
                                        z_avg = self.h["i33"]

                                        self.cur.execute(self.log_insert, (t, tm, f, l,
                                                                           x_min, x_max, x_avg,
                                                                           y_min, y_max, y_avg,
                                                                           z_min, z_max, z_avg))
                                        self.con.commit()
                                except KeyboardInterrupt :
                                        self.con.close()
                                        raise SystemExit
                                except Exception,e:
                                        print str(e)
                                        self.h["error"] = False
                                else :
                                        self.h["error"] = True
                except KeyboardInterrupt:
                        self.con.close()
                        raise SystemExit

l = Logger()
l.run()
