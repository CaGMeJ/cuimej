import argparse
import os
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--mode', choices=["r", "w"])
parser.add_argument('--file', required=True)
parser.add_argument('arg', nargs='*')
args = parser.parse_args()

def sample_conf_read(out):
    mode = ""
    sample_conf = {}
    with open(out) as lines:
        for line in lines:
            config = re.sub(r"[\s\n\t]", "", line)
            if config.startswith('#'):
                continue 
            if config.startswith('['):
                mode = re.search(r"(?<=\[)(.+?)(?=\])",config).group()
                if mode == "fastq":
                    sample_conf[mode] = {}
                else:
                    sample_conf[mode] = []
                continue
            if len(config) and mode != "":
                if mode == "fastq":
                    if config.count(",") == 0:
                        sample_name = config
                        sample_conf[mode][sample_name] = []
                    elif config.count(",") == 2:
                        sample_conf[mode][sample_name].append(config)
                    else:
                        print("wrong csv format !", file=sys.stderr)
                        sys.exit(1)
                else:
                    sample_conf[mode].append(config)
    return sample_conf

if args.mode == "r":
    sample_conf = sample_conf_read(args.file)
    for line in args.arg:
        if line[:6] == "fastq,":
            mode, sample_name = line.split(",", 1)
            for config in sample_conf["fastq"][sample_name]:
                print(config)
        elif line == "fastq":
            for sample_name in sample_conf["fastq"]:
                print(sample_name)
        else:
            for config in sample_conf[line]:
                print(config)
 
elif args.mode == "w":
    mode = ""
    sample_conf = {}
    out = args.file
    if os.path.isfile(out):
        sample_conf = sample_conf_read(out)
        out += ".tmp"
    for line in args.arg:
        mode, config = line.split(",", 1)
        if mode == "fastq":
            sample_name, config = config.split(",", 1)
            if mode in sample_conf:
                if sample_name in sample_conf[mode]:
                    sample_conf[mode][sample_name].append(config)
                else:
                    sample_conf[mode][sample_name] = [config]
            else:
                sample_conf[mode] = {}
                sample_conf[mode][sample_name] = [config]
        else:
            if mode in sample_conf:
                sample_conf[mode].append(config)
            else:
                sample_conf[mode] = [config]

    with open(out, mode="w") as f:
        for mode in sample_conf:
            f.write("["+mode+"]\n")
            if mode == "fastq":
                for sample_name in sample_conf[mode]:
                    f.write(sample_name+"\n")
                    for config in sample_conf[mode][sample_name]:
                        f.write(config+"\n")
            else:
                for config in sample_conf[mode]:
                    f.write(config+"\n")

    if out != args.file:
        os.rename(out, args.file)
else:
    print("Please set mode option !", file=sys.stderr)
    sys.exit(1)
