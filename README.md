# HollwooDDoS: Detecting Volumetric Attacks in Moving Images of Network Traffic

This repository contains the code used for [HollywooDDoS](s.kit.edu/skopmann), including preprocessing, model training, evaluation and visualization.

## Repository structure
- data/<br>Holds all required data.
  - datasets/<br>Raw datasets ([CAIDA2007](https://www.caida.org/catalog/datasets/ddos-20070804_dataset/) and [MAWI2019](http://mawi.wide.ad.jp/mawi/samplepoint-F/2019/201909011400.html))
  - preprocessing/ <br>Preprocessing ~ Image creation
  - training/ <br>Training data is stored here after preprocessing.
- evaluation/ <br>Results are analyzed, compared and visualized here.
- models/ <br>Contains model architectures.
  - trained/ <br>Stores trained models.
- results/ <br>Holds training histories.
- training/ <br>Holds training script and parameter file.

## Repository setup instructions
Download the datasets and store them in the `datasets/` directory.<br>
After the download is finished, navigate to the preprocessing directory `cd data/preprocessing` and
run the preprocessing scripts for each dataset `./mawi_preprocessing.sh` and `./caida_preprocessing.sh`.

After the raw traffic traces have been preprocessed, run the traffic composer `./traffic_composer.sh`.
The traffic composer injects CAIDA attack traffic into the MAWI background traffic.

Note that access to the DDoS traffic dataset needs to be provided by CAIDA. If you are not authorized to
access CAIDA data, you need to either request it for your research purposes or fall back to the preprocessed (aggregated) data provided by us via git large file storage.

Preprocessed datasets are in `csv` format. Each row of the `csv`-files represents a traffic image with its corresponding label (0,1) or (1,0).

## Datasets' visualization
![MAWI Traffic Intensity Development](./results/mawi_intensity_over_time.png) ![MAWI Traffic Intensity Development](./results/caida_intensity_over_time.png)