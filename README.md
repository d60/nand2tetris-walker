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
Chip        Nand
ALU         741
Add16       231
And         2
And16       32
DMux        5
DMux4Way    15
DMux8Way    35
FullAdder   15
HalfAdder   6
Inc16       231
Mux         4
Mux16       64
Mux4Way16   192
Mux8Way16   448
Not         1
Not16       16
Or          3
Or16        48
Or8Way      21
Xor         4
```
The number on the right indicates the total number of NAND gates.
Also, specify the chip name as the second argument to display the tree.
If specifying multiple names, separate them with commas e.g. `FullAdder,Inc16,Mux`.
Specify a wildcard `*` to display all trees. Empty trees will be omitted.

```shell
$ n2tw path/to/nand2tetris/nand2tetris/projects FullAdder
Chip        Count
ALU         741
Add16       231
And         2
And16       32
DMux        5
DMux4Way    15
DMux8Way    35
FullAdder   15
HalfAdder   6
Inc16       231
Mux         4
Mux16       64
Mux4Way16   192
Mux8Way16   448
Not         1
Not16       16
Or          3
Or16        48
Or8Way      21
Xor         4

FullAdder
├── HalfAdder
│   ├── Xor
│   │   └── Nand
│   └── And
│       ├── Nand
│       └── Not
│           └── Nand
└── Or
    ├── Not
    │   └── Nand
    └── Nand
```