# Ecotone Biogas

## About

`seahorse_camera.py` and `read_meter.py` are two scripts that capture images of the biogas meter in Ecotone's system and read the gas volume from the images. The read data is then added to a `csv` file. A sample biogas volume vs time plot is shown below. 

![sample_data](https://github.com/Shizhen-L/Biogas/blob/main/sampel_gas_meter_graph.png)

## `seahorse_camera.py`
The script captures 750x750 images of the biogas meter using a RaspberryPi camera at a set time interval.

## `read_meter.py`
The script downloads the captured images from the remote server to the local machine, and then uses [`pytesseract`](https://pypi.org/project/pytesseract/) to obtain the gas meter readings from the images. The reasonable readings are kept and added to a csv file. 

## Future improvements
- Improve optical character recognition (OCR) to extract more reliable readings from the images
- Processes gas meter readings to remove outliers using statistical tools
- Fully automate the script
