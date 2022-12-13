# mbusgemdecoder package
Decode MBUS-GEM register data into human-readable JSON.

## Introduction
The goal of `mbusgemdecoder` package is to convert a list of ten integer values into human-readable data object. `mbusgemdecoder` package automatically detects the type (`MBUS-GEM gateway`, `METER`, `METER VALUE`) of the register(s) and parses the data accordingly.

However, `mbusgemdecoder` package is only for data conversion. Use, for example, [pyModbusTCP](https://pypi.org/project/pyModbusTCP/) to obtain data to convert with `mbusgemdecoder`.
