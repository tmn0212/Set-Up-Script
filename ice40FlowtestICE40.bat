#!/bin/sh
rm hardware.bin
rm hardware.asc

yosys -p "read_verilog  -noblackbox testICE40.v ; synth_ice40  -top testICE40 -json hardware.json" 

nextpnr-ice40 --hx8k --package ct256 --ignore-loops --json hardware.json --asc hardware.asc --pcf ice40New.pcf

icepack testICE40New.bin
