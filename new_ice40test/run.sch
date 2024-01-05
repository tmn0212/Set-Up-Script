#!/bin/bash
rm out*
yosys -p 'synth_ice40 -top top -blif out.blif; write_json out.json' top.v
nextpnr-ice40 --hx8k --package ct256 --pcf pin.pcf --asc out.asc --json out.json
icepack out.asc out.bin
iceprog out.bin