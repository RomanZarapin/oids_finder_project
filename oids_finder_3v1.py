import argparse


class SnmpRecLine:

    def __init__(self, oid, data_type, value):
        self.oid = oid
        self.type = data_type
        self.value = value

    def __str__(self):
        str_oid = "{0}|{1}|{2}\n".format(str(self.oid), self.type, self.value)
        return f"{str_oid}"

    def __repr__(self):
        str_oid = "{0}|{1}|{2}\n".format(str(self.oid), self.type, self.value)
        return f"{str_oid}"


class OidsStruct:
    def __init__(self, row_oid):
        row_oid = row_oid
        if row_oid[0] == '.':
            row_oid = row_oid[1:]
        separated_oid = row_oid.split('.')
        self.int_oid = [int(splitted_oid) for splitted_oid in separated_oid]

    def __eq__(self, other):
        min_len = len(other)
        if len(self.int_oid) < min_len:
            min_len = len(self.int_oid)
        return self.int_oid[:min_len] == other[:min_len]

    def __lt__(self, other):
        min_len = len(other)
        if len(self.int_oid) < min_len:
            min_len = len(self.int_oid)
        return self.int_oid[:min_len] < other[:min_len]

    def __gt__(self, other):
        min_len = len(other)
        if len(self.int_oid) < min_len:
            min_len = len(self.int_oid)
        return self.int_oid[:min_len] > other[:min_len]

    def __str__(self):
        str_oid = ".".join([str(num) for num in self.int_oid])
        return f"{str_oid}"

    def __repr__(self):
        str_oid = ".".join([str(num) for num in self.int_oid])
        return f"{str_oid}"

    def __iter__(self):
        return self.int_oid.__iter__()

    def __len__(self):
        return len(self.int_oid)

    def __getitem__(self, item):
        return self.int_oid[item]


def source_file_opening(file_name):
    with open(file_name, 'r') as source_file:
        separated_data = [line.rstrip().split('|') for line in source_file]
    ready_data = [SnmpRecLine(OidsStruct(sd[0]), sd[1], sd[2]) for sd in separated_data]
    return ready_data


def our_oids_file_opening(file_name):
    with open(file_name, 'r') as our_file:
        oids_lst = [OidsStruct(line.rstrip()) for line in our_file]
    return oids_lst


def int_oid_making(oids_lst):
    int_oids_lst = [OidsStruct(oid) for oid in oids_lst]
    return int_oids_lst


def comparing(sought_oids, all_oids):
    eq_oid_lst = []
    sought_oid = sorted(sought_oids)
    for sought_oid in sought_oids:
        eq_oid_lst.extend(list(filter(lambda eq_oid: eq_oid.oid == sought_oid, all_oids)))
    return eq_oid_lst


def result_data_format(eq_oids):
    formatted_data = "".join(str(oid) for oid in eq_oids)
    return formatted_data


def save_data(data_to_save, file_name):
    with open(file_name, 'w') as result_file:
        result_file.write(data_to_save)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Oids finder')
    parser.add_argument('source_file_name', action='store', help='Name of file containing all oids')
    parser.add_argument('sought_file_name', action='store', help='Name of file containing sought oids')
    parser.add_argument('result_file_name', action='store', help='Name of result file')
    args = parser.parse_args()
    source_data = source_file_opening(args.source_file_name)
    our_oids_lst = our_oids_file_opening(args.sought_file_name)
    result_lst = comparing(our_oids_lst, source_data)
    result_data = result_data_format(result_lst)
    save_data(result_data, args.result_file_name)
