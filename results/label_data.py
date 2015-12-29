import csv


def write_label(fname, label):
    with open(fname, "r") as old_csvfile:
        with open(fname+"_labeled", "w") as new_csvfile:
            csvwriter = csv.writer(new_csvfile)
            for row in csv.reader(old_csvfile):
                csvwriter.writerow(row[:-1] + [row[-1][:-1], label])

if __name__ == "__main__":
    import sys
    write_label(sys.argv[2], sys.argv[1])

