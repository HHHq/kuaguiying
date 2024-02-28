import os

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# excel存放的路径
excel_path = os.path.join(root_path, "data", "case.xlsx")
# log存放的路径
log_path = os.path.join(root_path, "logs", "log.txt")
# yaml存放的路径
yaml_path = os.path.join(root_path, "config", "config.yaml")
# json存放的路径
json_path = os.path.join(root_path, "data", "info.json")

