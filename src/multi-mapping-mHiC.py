import bisect
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from collections import defaultdict


def main():
    parser = ArgumentParser("multi-mapping-mHiC",
                            formatter_class=ArgumentDefaultsHelpFormatter,
                            conflict_handler='resolve')
    parser.add_argument("--input", default='None')
    parser.add_argument("--frag", default='None')
    parser.add_argument("--output", default='None')

    args = parser.parse_args()
    input_file = args.input
    output_file = args.output
    fragment_file = args.frag

    fragment_dic = defaultdict(list)

    with open(fragment_file) as f:
        next(f)
        next(f)
        for line in f:
            fragment_info = line.split()

            if fragment_info[1] != "1":
                fragment_dic[fragment_info[0]].append(int(fragment_info[1]))

    curr_read = ""
    curr_reads = []

    output_f = open(output_file, "w")

    count_unique = 0
    count_all = 0

    with open(input_file) as f:
        for line in f:
            read_id = line.split()[0]
            if curr_read == "":
                curr_reads.append(line)
                curr_read = read_id
            elif curr_read == read_id:
                curr_reads.append(line)
            elif curr_read != read_id:
                count_all += 1
                result = process_read(curr_reads, fragment_dic, output_f)

                if result:
                    count_unique += 1

                curr_read = read_id
                curr_reads = [line]

    result = process_read(curr_reads, fragment_dic, output_f)

    if result:
        count_unique += 1

    output_f.close()

    print("Processed " + str(count_all) + " reads")
    print("Processed " + str(count_unique) + " multi mapping reads")
    print("Output is written to " + output_file)
    print("Done.")


# process the read
def process_read(reads, fragment_dic, output_sam):
    if len(reads) == 1:
        output_sam.write(reads[0])
        return False

    frag_diff_dic = defaultdict(list)

    min_diff = None
    for read in reads:
        fragment_diff = get_fragment_diff_both(read, fragment_dic)

        frag_diff_dic[fragment_diff].append(read)

        if not min_diff:
            min_diff = fragment_diff
        elif min_diff > fragment_diff:
            min_diff = fragment_diff

    if len(frag_diff_dic[min_diff]) == 1:
        output_sam.write(frag_diff_dic[min_diff][0].replace("MULTI", "UNI"))
        return True


# get the sum of the differences of both reads of the pair
def get_fragment_diff_both(read, fragment_dic):
    read_info = read.split()
    return get_fragment_diff(read_info[1], read_info[2], fragment_dic) + get_fragment_diff(read_info[6], read_info[7],
                                                                                           fragment_dic)


# get the difference from the nearest fragment
def get_fragment_diff(chr, pos, fragment_dic):
    fragments = fragment_dic[chr]
    read_value = int(float(pos))
    idx = bisect.bisect_left(fragments, read_value)

    if idx == 0:
        fragment_index_diff = fragments[idx] - read_value
    elif idx == len(fragments):
        fragment_index_diff = read_value - fragments[idx - 1]
    else:
        if (read_value - fragments[idx - 1]) < (fragments[idx] - read_value):
            fragment_index_diff = (read_value - fragments[idx - 1])
        else:
            fragment_index_diff = (fragments[idx] - read_value)

    return fragment_index_diff


if __name__ == '__main__':
    main()
