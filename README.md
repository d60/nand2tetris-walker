# Nand2tetris Walker

This tool recursively analyzes the components of each chip in Nand2tetris.

## Usage

### Installing
```shell
$ uv tool install git+https://github.com/d60/nand2tetris-walker
```

### CLI

```shell
$ n2tw path/to/nand2tetris/nand2tetris/projects
ALU         1125
Add16       231
And         2
And16       32
DMux        5
DMux4Way    15
DMux8Way    35
FullAdder   15
HalfAdder   6
Inc16       231
Mux         8
Mux16       128
Mux4Way16   384
Mux8Way16   896
Not         1
Not16       16
Or          3
Or16        48
Or8Way      21
Xor         4
```
The number on the right indicates the total number of NAND gates.
