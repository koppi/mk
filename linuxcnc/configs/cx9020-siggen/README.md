### Machinekit on Beckhoff CX9020 siggen HAL component test

See [Video]()

To run the test execute:
```bash
realtime start
halcmd -f koppi-cnc.hal
```

Play with the HAL pid and siggen component parameters:
```bash
halcmd setp siggen.0.amplitude 2
halcmd setp siggen.0.frequency 2
halcmd setp y-pid.maxoutput 100
...
```

More details at https://github.com/koppi/mk/blob/master/Machinekit-Beckhoff-CX9020.md
