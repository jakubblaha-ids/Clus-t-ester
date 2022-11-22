import argparse
import pathlib
import re
import requests
from subprocess import check_output
from typing import List
from termcolor import cprint


LOG_PATH = "test_log.txt"
VIS_URL = "http://www.fit.vutbr.cz/study/courses/IZP/public/cluster.php"
TEMPLATE_FNAME = "template.html"
HTML_OUTPUT_PATH = "test_output.html"


file_dir = pathlib.Path(__file__).parent.resolve()


def parse_args():
    parser = argparse.ArgumentParser("Clustester :)")

    parser.add_argument("PROGRAM")
    parser.add_argument("INPUT_FILE")

    return parser.parse_args()


def get_object_count_from_file(filename):
    with open(filename, "r") as f:
        first_line = f.readline()

    match = re.match("count=(\d+)", first_line)

    if not match:
        return None

    count = int(match.group(1))

    return count


def run_clusters(program_path, input_path, target_cluster_count):
    args = [program_path, input_path, str(target_cluster_count)]

    print(f"Calling:", args)

    try:
        out = check_output(args)
    except Exception:
        return None

    out = out.decode('utf-8')

    return out


def scrape_visualiser(program_output):
    # print({"proj3output": program_output})

    res = requests.post(VIS_URL, files={"proj3output": (None, program_output)})

    svg = re.search("<svg.*>.+<\/svg>", res.text, re.S).group(0)

    return svg


def generate_output(svgs: List[str]):
    template_path = pathlib.Path(file_dir).joinpath(TEMPLATE_FNAME)

    with open(template_path) as f:
        template = f.read()

    svgs = [f"`{out}`" for out in svgs]

    replaced = template.replace("XXX", ','.join(svgs))

    with open(HTML_OUTPUT_PATH, "w") as f:
        f.write(replaced)


def main():
    args = parse_args()

    program_path = args.PROGRAM
    input_path = args.INPUT_FILE

    object_count = get_object_count_from_file(input_path)

    if not object_count:
        print("Failed to load object count from input file.")

    print("Loaded object count from input file is:", object_count)

    outputs = []
    svgs = []

    for i in range(object_count, 1, -1):
        print("\nRunning iteration:", object_count - i)

        out = run_clusters(program_path, input_path, i)

        if not out:
            cprint("Failed to run iteration. Skipping...", "red")
            outputs.append("Crashed")
            continue

        print("Program output:", out[:100].replace("\n", " "), "...")
        print("Scraping Smčka visualizer...")

        svg = scrape_visualiser(out)

        cprint("Scraped: " + svg[:100].replace("\n", " ") + " ...", "green")

        svgs.append(svg)

        outputs.append(out)

        # break

    print("Writing outputs into", LOG_PATH, "...")

    with open(LOG_PATH, "w") as f:
        for index, out in enumerate(outputs):
            f.write(f"----- Output for iteration: {index} -----\n")
            f.write(out + '\n')

    print("Writing output HTML into", HTML_OUTPUT_PATH, "...")
    generate_output(svgs)

    print("Done. Now open", HTML_OUTPUT_PATH, "in your favorite browser.")


if __name__ == "__main__":
    main()
