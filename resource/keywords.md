# Keywords

<!--toc:start-->

- [Keywords](#keywords)
  - [software engineering](#software-engineering)
  - [Math](#math)
  - [ICS](#ics)
    - [sensor protocol](#sensor-protocol)
    - [Clock/Reset](#clockreset)
  - [board design](#board-design)
  - [tool/software](#toolsoftware)
  - [Website](#website) - [For fun](#for-fun) - [Hardware](#hardware)
  <!--toc:end-->

## software engineering

- treesitter query config
- Canonical LR parser
- penpot: design in codes
- Grokking system design
- ddia: Designing Data-intensive Applications

## Math

- stochastic process

## ICS

### sensor protocol

- DPI: parallel signals
- SDI: SCLKO, SDOUT
- LVDS: differential pair

### Clock/Reset

- async reset with synced release
- clock tree:
  - external oscillator
  - internal oscillator: circuit, ring oscillator
  - PLL
  - clock divider
- PAD
  - pin mux
  - external pin for power-on register initialization
    - cpu auto boot up
    - master clock select

## board design

- pull up resistor: I2C, UART
- component placement
- 0Ohm resistor: configurable connection
- power measurement jumper
- power hierarchy: easier power measurement
- signal level shifter
<!--- TODO: make this into a chapter -->
- debug:
  - check 0ohm resistor configuration
  - voltage check with multimeter
  - control signals check with LA
    - I2C
      - nack
        - stable nack: slave may not be working at all
        - unstable nack:
          - oversampling frequency too slow: master uses slow clock
          - i2c transmission speed too fast
  - signals check with oscilloscope
    - clock
      - toggling
      - frequency
      - voltage level

## tool/software

- Hardware testing
  - 串口調適助手
  - Joulscope
  - TravelLogic Logic Analyzer
- lnav
- whisper.cpp

## Website

### For fun

#### Hardware

- [hackseter](https://www.hackster.io/)
