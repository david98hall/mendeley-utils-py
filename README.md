# mendeley-utils-py
Utilities for simplifying the use of the Python [Mendeley API](https://github.com/Mendeley/mendeley-python-sdk).

### Example
```python
import yaml
from mendeley_utils import MendeleyHelper

if __name__ == '__main__':
    
    with open('secrets/secret_config.yml') as file:
        client_config = yaml.load(file, Loader=yaml.FullLoader)["client"]

    mendeley_helper = MendeleyHelper(client_id=client_config["id"], client_secret=client_config["secret"])
    
    # Opens a web browser tab where you can log in to Mendeley
    session = mendeley_helper.get_session()
    
    # Do stuff with the Mendeley session object...
    documents = session.documents

```

### Notes
Tested using Python 3.8.
