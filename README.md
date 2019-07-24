# sedonalib
A library of companion tools for the Sedona radiation/hydrodynamics code.

Library Organization:
* sedona.py
  I think this was supposed to be like a lightweight Python version of
  Sedona?
* analysis
  Modules for calculating new quantities from on a Sedona
  model output, e.g., light curves in actual observational bands.
* io
  Modules for creating Sedona input or altering a Sedona output,
  primarily aimed at facilitating cross-talk with other codes.
* plot
  Modules for plotting Sedona outputs including grid quantities
  and spectra.
* data
  Backend component. Contains physical data and the tools for using them.
* loaders
  Backend component. Contains classes for loading Sedona output into
  data structures for calculations.
