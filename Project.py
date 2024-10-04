import json
from dataclasses import dataclass
# Parses json data and use it to determine our clock project

SCALE = 1  # how much to scale your clock
POSITION = (100, 100)  # distance to the top right corner
settings = {
    "ticktock": 3.2,  # seconds between ticks
    "alwaysdisplay": False,
}

@dataclass
class Interval:
    totalPip: int = 0
    totalTime: float = float("inf")  # in seconds
    karmaSymbol : int = 10  # 0 to maxKarma
    karmaReinforced : bool = False
    maxKarma : int = 5 # 5 to 10 excluding 6


def loadData():
    # 定义文件路径
    file_path = "./data.json"
    try:
        # 打开文件并读取 JSON 数据
        with open(file_path, 'r', encoding='utf-8') as file:
            r = json.load(file)
            # 输出读取的数据
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    if "ticktock" in r:
        settings["ticktock"] = r["ticktock"]
    if "alwaysdisplay" in r:
        settings["alwaysdisplay"] = r["alwaysdisplay"]
    if "intervals" in r and type(r["intervals"]) == list:
        intervals = []
        for obj in r["intervals"]:
            try:
                intervals.append(Interval(**obj))
            except:
                return "Invalid interval: " + repr(obj)
        return intervals
    return "Intervals not readable."