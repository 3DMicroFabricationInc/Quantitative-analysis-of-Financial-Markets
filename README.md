###### moving_average_crossover_point.py Version 3.0 ######
In order to run moving_average_crossover_point.py install python (follow link https://www.python.org/downloads/windows/)
Confirm installation by typing "Python --version" in cli (command link interface)
In order to get all the dependancies type "pip install yfinance mathplotlib numpy pandas"

---------------------------------------------------------------

* moving_average_crossover_point.py NOTES:

(1) Added cli helperbot to select program functions, to view the functions available type "help" at cli.

(2) Updated config.json to list company stock name and date setting.

(3) Renamed moving_average_crossover_point.py to market_trend.py to market_trend.py.

(3) To do list: create a automatic expansion update (to add new companies to list without changing program logic)

---------------------------------------------------------------

* market_trend.py Changelog:

| Date | Version | Author | File(s) Changed | Description of Change | Reason/Impact |
| --- | --- | --- | --- | --- | --- |
| 2026-04-24 | v1.2.1 | Theunis | ``config.json and market_trend.py`` | Added ability to add companies without having to change program logic or add new folders | Reduces time taken to add new companies to anlalysis |
| 2026-04-24 | v1.2.0 | Theunis | ``market_trends.py`` | Added new_company, reload function | Reduces time taken to add new companies to anlalysis |
| 2026-04-24 | v1.1.5 | Theunis | ``microsoft_trends.py`` | Fixed bug in moving average calculation | Ensures accurate smoothing |
| 2026-04-23 | v1.1.0 | Theunis | ``tesla_trends.py`` | Introduced Bollinger Bands visualization | Enhances volatility tracking |
| 2026-04-22 | v1.0.0 | Theunis | ``nike_trends.py``, README | Initial commit with baseline scripts | Establishes reproducible workflow |
