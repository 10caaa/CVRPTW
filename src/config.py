import yaml
import os
from typing import Dict, Any


class Config:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_path):
            return self._default_config()
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _default_config(self) -> Dict[str, Any]:
        return {
            'solver': {
                'initial_temperature': 2000,
                'cooling_rate': 0.999,
                'max_iterations': 50000,
                'min_temperature': 0.1,
                'verbose': True
            },
            'heuristics': {
                'initial_solution_method': 'clarke_wright',
                'local_search_iterations': 100,
                'operators': ['swap', 'relocate', 'two_opt', 'or_opt', 'cross_exchange']
            },
            'instance': {
                'default_num_vehicles': 5,
                'data_path': 'instance/VRPLIB/tests/data/'
            },
            'output': {
                'save_plots': True,
                'save_results': True,
                'results_directory': 'results/',
                'plot_directory': 'results/plots/'
            }
        }
    
    def get(self, *keys):
        value = self.config
        for key in keys:
            value = value.get(key, {})
        return value
    
    def __getitem__(self, key):
        return self.config[key]
