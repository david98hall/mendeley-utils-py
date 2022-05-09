import yaml
from mendeley_utils import MendeleyHelper

if __name__ == '__main__':
    
    with open('secrets/secret_config.yml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    client_config = config["client"]

    mendeley_helper = MendeleyHelper(
        client_id=client_config["id"], 
        client_secret=client_config["secret"])
    
    session = mendeley_helper.get_session()
    print(session.token)