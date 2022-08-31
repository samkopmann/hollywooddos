# HollwooDDoS: Detecting Volumetric Attacks in Moving Images of Network Traffic

This repository contains the code used for [HollywooDDoS](s.kit.edu/skopmann), including preprocessing, model training, evaluation and visualization.

The repository is structured as follows:

- data/<br>Holds all required data.
  - datasets/<br>Raw datasets ([CAIDA2007](https://www.caida.org/catalog/datasets/ddos-20070804_dataset/) and [MAWI2019](http://mawi.wide.ad.jp/mawi/samplepoint-F/2019/201909011400.html))
  - preprocessing/ <br>Preprocessing ~ Image creation
  - training/ <br>Training data is stored here after preprocessing.
- evaluation/ <br>Results are analyzed, compared and visualized here.
- models/ <br>Contains model architectures.
  - trained/ <br>Stores trained models.
- results/ <br>Holds training histories.
- training/ <br>Holds training script and parameter file.
