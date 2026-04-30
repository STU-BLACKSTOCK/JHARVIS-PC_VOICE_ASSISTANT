import os

def search_file(keyword: str, directory: str = "C:/Users") -> str:
    matches = []
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                if keyword.lower() in file.lower():
                    matches.append(os.path.join(root, file))
                    if len(matches) > 5: # Limit search for speed
                        break
            if len(matches) > 5:
                break
                
        if matches:
            return f"I found {len(matches)} matching files. Here is one: {matches[0]}"
        else:
            return "No files found with that name."
    except Exception as e:
        return f"Error searching for file: {e}"
