import os

folder = os.path.join(os.path.dirname(__file__), "files")

destinations = {
    "桃美": "桃美",
    "桃美連通橋": "桃美連通橋",
}

def identify_file(filename):
    for name in sorted(destinations, key=len, reverse=True):
        if name in filename:
            return destinations[name]
            
    return "其他"

for filename in os.listdir(folder):
    destination = identify_file(filename)

    print(filename)
    print(f" {destination}")
