import pytest

import os

from mag_annotator.utils import run_process, make_mmseqs_db, merge_files, multigrep


def test_run_process():
    run_process(['echo', 'Hello', 'World'], verbose=True)
    assert True


@pytest.fixture()
def mmseqs_db_dir(tmpdir):
    output_loc = tmpdir.mkdir('make_mmseqs_db_test')
    return output_loc


@pytest.fixture()
def test_make_mmseqs_db(mmseqs_db_dir):
    faa_path = os.path.join('tests', 'data', 'NC_001422.faa')
    output_file = str(mmseqs_db_dir.join('mmseqs_db.mmsdb'))
    make_mmseqs_db(faa_path, output_file, True, 1)
    assert os.path.isfile(output_file)


@pytest.fixture()
def merge_test_dir(tmpdir):
    return tmpdir.mkdir('test_merge')


@pytest.fixture()
def files_to_merge_no_header(merge_test_dir):
    for i in range(3):
        merge_file = merge_test_dir.join('merge_test.%s.txt' % str(i))
        merge_file.write('test%s\n' % str(i))
    return os.path.join(str(merge_test_dir), 'merge_test.*.txt')


@pytest.fixture()
def files_to_merge_w_header(merge_test_dir):
    header = 'gene_name'
    for i in range(3):
        merge_file = merge_test_dir.join('merge_test_w_header.%s.txt' % str(i))
        merge_file.write('%s\ntest%s\n' % (header, str(i)))
    return os.path.join(str(merge_test_dir), 'merge_test_w_header.*.txt')


def test_merge_files(files_to_merge_no_header, files_to_merge_w_header, merge_test_dir):
    test_merge = merge_test_dir.join('merged_test.txt')
    merge_files(files_to_merge_no_header, test_merge, False)
    assert len(test_merge.readlines()) == 3

    test_merge_w_header = merge_test_dir.join('merged_test_w_header.txt')
    merge_files(files_to_merge_w_header, test_merge_w_header, True)
    assert len(test_merge_w_header.readlines()) == 4


@pytest.fixture()
def multigrep_inputs(tmpdir):
    hits = ['gene1', 'gene3', 'gene5']
    data_str = "gene1 something about gene1\n" \	
               "gene2 gene2 information\n" \	
               "gene3 data including gene3\n" \	
               "gene4 data including gene4\n" \	
               "gene5 data including gene5\n"
    data_file = tmpdir.mkdir('multigrep_test').join('multigrep_test_data.txt')
    data_file.write(data_str)
    return hits, str(data_file)


 def test_multigrep(multigrep_inputs):
    keys, values = multigrep_inputs
    dict_ = multigrep(keys, values, skip_chars=0)
    assert len(dict_) == len(keys)
    assert dict_['gene1'] == 'gene1 something about gene1'
    assert dict_['gene3'] == 'gene3 data including gene3'
    assert dict_['gene5'] == 'gene5 data including gene5'
