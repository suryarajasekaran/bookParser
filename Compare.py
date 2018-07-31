import logging


class Compare(object):

    def __init__(self, actual_file_data, regenerate_file_data):
        self.actual_file_data = actual_file_data
        self.regenerate_file_data = regenerate_file_data

    # generates shingles for a file
    def generate_shingles(self, file_data):
        logging.info("generating shingles")
        shingle_size = 9
        file_data_len = len(file_data)
        file_data_shingles = {}
        for i in xrange(0, file_data_len - shingle_size):
            hashed_key = self.actual_file_data[i:i+9-1]
            if hashed_key in file_data_shingles:
                file_data_shingles[hashed_key] = file_data_shingles[hashed_key] + 1
            else:
                file_data_shingles[hashed_key] = 1
        return file_data_shingles

    # uses k-shingling approach to compare 2 files
    def compare_data(self):
        logging.info("comparing shingles")
        actual_file_shingles = self.generate_shingles(file_data=self.actual_file_data)
        regenerate_file_shingles = self.generate_shingles(file_data=self.regenerate_file_data)
        union_shingles = {}
        for key, value in actual_file_shingles.iteritems():
            if key in regenerate_file_shingles:
                union_shingles[key] = True
            else:
                union_shingles[key] = False
        for key, value in regenerate_file_shingles.iteritems():
            if key in union_shingles:
                continue
            else:
                union_shingles[key] = False
        match_count = 0
        for key, value in union_shingles.iteritems():
            if value:
                match_count += 1
            else:
                continue
        match_percentage = float(match_count)/float(len(union_shingles)) * 100
        logging.info("shingle computation matches={} total={} accuracy={}".format(match_count, len(union_shingles), match_percentage))
        return match_percentage





