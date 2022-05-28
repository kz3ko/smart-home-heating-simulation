## Logs directory

This directory is used for storing logs. They are included in `.gitignore`, thus this stays empty. After turning logging
process on all logs will be stored here.

### Creation of temperature graph for all rooms

In order to create graph of room temperatures use `logs_plot.py`. This is not included in app itself, so you have to 
have both `matplotlib` and `pandas` libraries installed locally. After that you can simply run this script running:

```
python logs_plot.py
```

from level of this directory. You will be asked for name of logs_directory (pattern is similar to `19:42:03-03.02.2022`).
After providing it plot should appear.
