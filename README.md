# ![donut.png](https://github.com/juvarlet/a_table/blob/ju_branch/UI/images/donut_icon.png?raw=true) À Table !
![app_screenshot.png](https://github.com/juvarlet/a_table/blob/ju_branch/images/app_screenshot.png?raw=true)

App to create, organize and plan your own recipes

## Prerequesites
* Python 3.8.5 or higher


### Python dependencies
- Refer to [requirements.txt](https://github.com/juvarlet/a_table/blob/ju_branch/requirements.txt)


## Installation
* Clone the repository
* Run 
  >     pip install -r requirements.txt
* Launch main.py

## Generate standalone executable for windows
* Checkout [exe_pack branch](https://github.com/juvarlet/a_table/tree/exe_pack)
* Create and activate virtual environment
  >     python -m venv path\to\venv
  >     cd path\to\venv\Scripts
  >     activate
* Install required python libraries 
  >     pip install -r requirements.txt
* Generate package with pyinstaller
  >     cd path\to\a_table
  >     path\to\venv\Scripts\pyinstaller.exe --onefile --paths path\to\venv\Lib\site-packages -w --noconsole --clean main.spec
* Copy data files and folders to \dist\ (next to "A_Table.exe")
  * images\ 
  * Mes_Fiches\
  * Historique.csv
  * MesRecettes.csv

## Repository visualization
Interactive HTML visualization: [Diagram](https://octo-repo-visualization.vercel.app/?repo=juvarlet%2Fa_table)
![Visualization of this repo](./diagram.svg)
