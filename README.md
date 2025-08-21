# SMA REACT
SMA-REACT is an open-source, (hopefully) easy-to-use
tool for processing shape memory alloy experimental data and calibrating a constitutive model for use in other analyses(e.g., Abaqus).
Data processing and model calibration are presented in the form of a python GUI, allowing those unfamiliar with the intricate details of SMA constitutive modeling to easily calibrate appropriate models without writing their own custom subroutines. 
SMA-REACT is distributed under the BSD 3-Clause License, which [``allows unlimited redistribution for any purpose as long as its copyright notices and the license's disclaimers of warranty are maintained.''](https://en.wikipedia.org/wiki/BSD_licenses)

## Downloads

1. Go to the [Releases](https://github.com/maestrolab/SMA_REACT/releases) page and download the SMA_REACT executable for your operating system. 
	- 1a. Click **Assets** to expand the list of downloadable files and select/download the one for your operating system. You can also download the `input.zip` file which contains sample input files for the SMA_REACT software.

 	- 1b. Unzip the files and double click either the `calibration` <img src="icons/Rcalibration.png" alt="Icon" width="30" height="30"> or the `preprocessor` <img src="icons/Rpreprocessor.png" alt="Icon" width="30" height="30"> executables to run the SMA_REACT software.	

2. If you prefer to install the software from source, you can clone the repository and install the dependencies manually. We recommend doing this in a **virtual environment** to avoid package conflicts.
	
	- 2a. Clone the repository:
	
	    ```bash
	    git clone https://github.com/maestrolab/SMA_REACT.git
	    cd SMA_REACT
	    ```
	
   	- 2b. (Optional but recommended) Create and activate a virtual environment:
	
	    - On macOS/Linux:
	
	        ```bash
	        python3 -m venv venv
	        source venv/bin/activate
	        ```
	
	    - On Windows:
	
	        ```cmd
	        python -m venv venv
	        venv\Scripts\activate
	        ```
	
	- 2c. Install the package and its dependencies (from the directory containing the `pyproject.toml` file):
	
	    ```bash
	    pip install .
	    ```
	
	    This will install all required packages with the correct versions as defined in the project.

   	- 2d. Run the `calibration` <img src="icons/Rcalibration.png" alt="Icon" width="30" height="30"> GUI using the command:

   	    ```
	    sma-react-calibration
	    ```

		Run the `preprocessor` <img src="icons/Rpreprocessor.png" alt="Icon" width="30" height="30"> GUI using the command:

	     ```
	     sma-react-preprocessor
	     ```

3. If you prefer not to use `pip install .`, you can manually install the required packages individually (ensure you get the correct package versions).

## Documentation

See the [SMA REACT User's Guide](https://sma-react.readthedocs.io/en/latest/) for the full documentation. You can also build the documentation locally by navigating to the ``docs`` subfolder and running the command ``.\make.bat html``.
The documentation will be located under ``docs\_build\html``.

## Requirements

SMA-REACT is compatible with Python 3.9 and is built
with pyqt5, version 5.15.10. 
Here is a complete list of dependencies:

   * [deap](https://deap.readthedocs.io/en/master/)
   * [matplotlib](https://matplotlib.org/)
   * [numpy](https://numpy.org/)
   * [pandas](https://pandas.pydata.org/)
   * [pyqt5](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
   * [scikit-learn](https://scikit-learn.org/stable/)
   * [scipy](https://scipy.org/)

## How to cite SMA REACT
Authors of scientific papers including results generated using SMA-REACT are encouraged to cite the following paper.

```xml
@article{walgren_pre-print_2024,
	title = {[{PRE}-{PRINT}] {The} {Shape} {Memory} {Alloy} {Rendering} and {Calibration} {Tool} ({SMA}-{REACT})},
	journal = {Shape Memory and Superelasticity},
	author = {Walgren, Patrick and Mingear, Jacob},
	year = {2024},
}
```


