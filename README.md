# sstcam-simulation [![tests](https://github.com/sstcam/sstcam-simulation/workflows/tests/badge.svg)](https://github.com/sstcam/sstcam-simulation/actions?query=workflow%3Atests) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/sstcam/sstcam-simulation/master)

Low-level and simple simulation package for the SST camera. 


### Purpose

* Provide a simulation framework of the SST camera where we have full control over the camera description, readout chain, and trigger logic. 
* Inform on decisions for the final camera design.
* Demonstrate the capability of the camera design to meet the level-C CTA requirements.


### Why not simtelarray?

1. We want something simple - This project is intended to be a simple Python package, avoiding the need to dig into simtelarray code, or the need to account for all the inputs required for a simtelarray production.
2. We only care about the performance of our camera -  We don't need to worry about ray tracing, array layouts, or other cameras. 
3. Finer specification of the camera - Simtelarray does not allow us to easily investigate some parameters of our camera, such as the crosstalk between pixels, and realistic noise spectrum.
4. Direct control of pixel illumination - Many of the important camera specifications can be examined without Corsika Cherenkov shower and ray tracing simulations. Specifying exactly the average illumination you wish to simulate for each pixel allows more statistics to be gathered with less CPU time.
5. Trigger performance - Investigating all aspects of trigger performance in simtelarray is difficult (due to lack of "noise events"). This is a simple operation in this package.


## Install

An environment.yml is provided to setup a conda environment with all the 
required dependencies.

```bash
git clone https://github.com/sstcam/sstcam-simulation.git
cd sstcam-simulation
conda env create -f environment.yml
conda activate sstcam-simulation
python setup.py develop
```


## Design

This package does not provide a single pipeline, and is not configured through 
input files. Users are instead expected to create scripts which piece together the 
parts of this package they require to obtain the output they are interested in. This 
provides the user with full control over the camera description, and can avoid 
performing operations that may be unnecessary for a particular investigation. For 
example, investigating the trigger rate of a single superpixel from NSB only requires 
one superpixel to be simulated, and does not require the Cherenkov shower, 
the waveform sampling, or the backplane trigger to be simulated. As a result, 
users gain learn how the SST camera operates, instead of working 
with a black-box simulation. This design also allows the package to be kept 
extremely simple, requiring no complex configuration or factory classes in 
order to flexibly define the camera.

Typical scripts that utilise this package are summarised in four steps:
1. Define the camera (Pulse shape, SPE spectrum, noise spectrum, number of pixels...).
2. Simulate the photoelectrons (NSB, uniform light, Cherenkov shower ellipse...).
3. Acquire the event (readout/trigger) by processing the input through the camera electronics.
4. Perform the analysis you require on the camera outputs to investigate the camera performance.


## Tutorials

Tutorial notebooks are provided in the tutorials directory, detailing the 
possible operations this package provides, and also some demonstrations on 
obtaining camera performance results.

These notebooks can also be ran without installing the package locally, through 
clicking the Binder badge above.
