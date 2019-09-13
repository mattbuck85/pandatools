## File Extraction

### Encoding Detection
```python
import extract
extract.encoding('./file.txt')

>>> "utf-8"
```

### Problematic CSV Extraction
```python
import extract
extract.workaround('./file.csv')
```