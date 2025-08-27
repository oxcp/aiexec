import yaml
import json

class VerifyConfiguration:
    def __init__(self, config_path='verify_config.yaml'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        self.models_json = json.dumps(self.config['models'], ensure_ascii=False)
        self.scenarios_json = json.dumps(self.config['scenarios'], ensure_ascii=False)


# print("Models JSON:", models_json)
# print("Scenarios JSON:", scenarios_json)