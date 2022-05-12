```
start date: 20.1.2022 (European date format)
last edit: 7.5.2022
```
# README.md for finding duplicates in 

## links
- [README2.md](README2.md) (general pipeline)
- [OPEN_visualisations.md](OPEN_visualisations.md)

## process flow
<img src="doc/process_flow_full_pipeline.png" alt="full_pipeline"/>

(generated from [process_flow.odp](doc/process_flow.odp))

The config.json files are also a good start to see the workflow and the sequence of steps to be taken. See e.g. [io.json](config/io.json) and [config_master.json](config/config_master.json).

## background
- it should scale to an arbitrary number of datasets
- you provide constraints through criteria on: 
    - how to determine duplicates (see pairwise)
    - subselections

## 0. preparation

### folder structure
![FolderStructure](doc/FolderStructure.png)
- **csv_per_measurements** contains files, where one entry corresponds to one measurement of the sensor/device, etc.
- **csv_per_day** contains files, where one entry corresponds to the aggregate per day

The folder structure is created in the scripts, if they do not yet exist.

The new folder structure (as of May 2022):
- a root data directory, relative to which all directories are located
- a per_day-directory
- a duplicates-directory
- a csv_per_measurement-directory

the input datasets are labeled in the [config_master.json](config_master.json) as ds0,ds1, ..., dsn.

## 1. processing per single dataset
<img src="doc/process_flow_single_dataset.png" alt="pipeline_single_dataset"/>

## 2. pairwise processing: finding duplicates

## 3. aggregation of all datasets

## 4. visualisation & quality control






## 1. preprocessing step: `python3 preprocessing.py` (per dataset)
preprocessing.py takes the json.gz files of OPENonOH_Data, gunzips them to json-files and selects **noise, sgv, date, dateString** and writes them into csv-files in the _csv_per_measurement_-subdirectory.
 
_Possible improvement: only a subset of all variables is stored in the csv-output files, store all variables._

One entry in the csv output file is one measurement. One file corresponds to one json file. 

_Maybe one could also share these csv-files in the google drive?_

Some statistics on the output is provided in [csv_statistics_count_days.txt](csv_statistics_count_days.txt): Total: more than 8 Million measurements

This brings the different formats into one common format: csv file with noise, bg, date, dateString.

## 2. aggregation_step.ipynb: aggregate into statistics per days: mean, rms (or stddev), min, max, count (per dataset)
Read the csv-files in csv_per_measurement as input.
Output is one csv-file containing approx. 8000 lines, with the aggregate per days and statistical variables.
(The aggregation per day is a somewhat arbitrary choice. Since one has up to 285 measurements per day, the error on the statistical measures becomes small. For higher granularity the statistical error becomes bigger, increasing the likelihood of false positive duplicates. Aggregate per week would be possible as well.)

_Paths need to be adjusted to your local environment._

## 3. self-duplicates (per dataset)


## 4. pairwise duplicates: combine with the OpenAPS data file in a smart way.
<img src="doc/ProcessFlow.png" alt="ProcessFlow" width="1000px"/>

Basic idea: if the statistical variables per day are very __"similar"__ in both datasets (OpenAPS and OPENonOH), then these are duplicate candidates. A distance metric to define __"similar"__ needs to be worked out.

The algorithm to detect duplicates applied here is a join by date between the Open Humans and the OpenAPS data commons dataset and then calculating the quadratic difference between the daily mean(plasma glucose), stddev, min, max and requiring a certain threshold.
A requirement here is that datetimes are consistent in both datasets, otherwise the daily mean, stddev, min, max are different even if the underlying data is identical except for the offset in time. An offset in time could lead to false negatives. This is achieved by calculating a UTC time from the unix_timestamps ("date"-column) and taking the date from that UTC timestamp.

False positives could arise if the threshold is chosen too loose.  

_Paths need to be adjusted to your local environment._

Here use the generic dataset_1,_2,_3 rather than the specific OpenAPS_NS (nightscout), OPENonOH, in the processing.
Because for duplicates it just matters, that they are distinct datasets, while in the previous steps the different format specific to each dataset was relevant.

## testing
A procedure is to be put in place to generate artificial per_day csv files from a matrix expressing the relationship between different datasets.
It allows to test the pipeline from step 2 to step 4. Validating the logic of generating the data_per_project_member_id.csv files.
As of May 2022 this deduplication framework is developed with four datasets. The testing allows to validate the generalization of the pipeline to more than four datasets.

## naming conventions
following: https://pythonguides.com/python-naming-conventions/

- functions and variables: snake case
- classes: camelCase, starting with a lowercase letter

## Datasets

### OpenAPS Data Commons
- Compressed: 9.6 GB
- Uncompressed: ~120 GB (!) 

## tested with
- python 3.8.10
- see requirements.txt

## dependencies
```
pip3 install -r requirements.txt
```
(requirements.txt was generated with `pipreqs .` + some manual adjustment)


```
first author: Bernd Reinhold
```
