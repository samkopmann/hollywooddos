# HollwooDDoS: Detecting Volumetric Attacks in Moving Images of Network Traffic

This repository contains the code used for [HollywooDDoS](s.kit.edu/skopmann), including preprocessing, model training, evaluation and visualization.

The repository is structured as follows:

- data/ <span style="color:grey">Holds all required data.</span>
  - datasets/ <span style="color:grey">Raw datasets ([CAIDA2007](https://www.caida.org/catalog/datasets/ddos-20070804_dataset/) and [MAWI2019](http://mawi.wide.ad.jp/mawi/samplepoint-F/2019/201909011400.html))</span>
  - preprocessing/ <span style="color:grey">Preprocessing ~ Image creation</span>
  - training/ <span style="color:grey">Training data is stored here after preprocessing.</span>
- evaluation/ <span style="color:grey">Results are analyzed, compared and visualized here.</span>
- models/ <span style="color:grey">Contains model architectures.</span>
  - trained/ <span style="color:grey">Stores trained models.</span>
- results/ <span style="color:grey">Holds training histories.</span>
- training/ <span style="color:grey">Holds training script and parameter file.</span>
