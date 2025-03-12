import os


def viewTree(directory, prefix=""):
    print("\033[94m[View Tree] Scanning a directory\033[0m\n")

    def scan(directory, prefix=""):
        entries = sorted(os.listdir(directory))
        for index, entry in enumerate(entries):
            if entry == "packages":
                continue

            path = os.path.join(directory, entry)
            is_last = index == len(entries) - 1
            tree_symbol = " |___  " if is_last else " |---  "

            print(f"{prefix}{tree_symbol}{entry}")

            if os.path.isdir(path):
                new_prefix = prefix + ("    " if is_last else " |    ")
                scan(path, new_prefix)

    scan(directory, prefix)
