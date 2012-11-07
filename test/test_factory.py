data_object = {}

data_object['general'] = {'site': 'vampsdev', 'load_vamps_database': False, 'run': '20120614', 'primer_file': '', 'input_file_format': 'fastq', 'input_dir': './test/sample_data/illumina/Project_J_v6_30/', 'database_name': 'test', 'configpath': './test/sample_data/illumina/result/20120614/20120614.ini', 'anchor_file': '', 'platform': 'illumina', 'use_cluster': True, 'idx_keys': 'ATCACG_NNNNACGCA_3,ATCACG_NNNNCGCTC_3,ATCACG_NNNNCTAGC_3,ATCACG_NNNNGACTC_3,ATCACG_NNNNGAGAC_3,ATCACG_NNNNGCTAC_3,ATCACG_NNNNGTATC_3,ATCACG_NNNNTCAGC_3,CGATGT_NNNNACGCA_3,CGATGT_NNNNCGCTC_3,CGATGT_NNNNCTAGC_3,CGATGT_NNNNGACTC_3,CGATGT_NNNNGAGAC_3,CGATGT_NNNNGCTAC_3,CGATGT_NNNNGTATC_3,CGATGT_NNNNTCAGC_3,TTAGGC_NNNNACGCA_3,TTAGGC_NNNNCGCTC_3,TTAGGC_NNNNCTAGC_3,TTAGGC_NNNNGACTC_3,TTAGGC_NNNNGAGAC_3,TTAGGC_NNNNGCTAC_3,TTAGGC_NNNNGTATC_3,TTAGGC_NNNNTCAGC_3,TGACCA_NNNNACGCA_3,TGACCA_NNNNCGCTC_3,TGACCA_NNNNCTAGC_3,TGACCA_NNNNGACTC_3,TGACCA_NNNNGAGAC_3,TGACCA_NNNNGCTAC_3,TGACCA_NNNNGTATC_3,TGACCA_NNNNTCAGC_3,ACAGTG_NNNNACGCA_3,ACAGTG_NNNNCGCTC_3,ACAGTG_NNNNCTAGC_3,ACAGTG_NNNNGACTC_3,ACAGTG_NNNNGAGAC_3,ACAGTG_NNNNGCTAC_3,ACAGTG_NNNNGTATC_3,ACAGTG_NNNNTCAGC_3,GCCAAT_NNNNACGCA_3,GCCAAT_NNNNCGCTC_3,GCCAAT_NNNNCTAGC_3,GCCAAT_NNNNGACTC_3,GCCAAT_NNNNGAGAC_3,GCCAAT_NNNNGCTAC_3,GCCAAT_NNNNGTATC_3,GCCAAT_NNNNTCAGC_3,CAGATC_NNNNACGCA_3,CAGATC_NNNNCGCTC_3,CAGATC_NNNNCTAGC_3,CAGATC_NNNNGACTC_3,CAGATC_NNNNGAGAC_3,CAGATC_NNNNGCTAC_3,CAGATC_NNNNGTATC_3,CAGATC_NNNNTCAGC_3,ACTTGA_NNNNACGCA_3,ACTTGA_NNNNCGCTC_3,ACTTGA_NNNNCTAGC_3,ACTTGA_NNNNGACTC_3,ACTTGA_NNNNGAGAC_3,ACTTGA_NNNNGCTAC_3,ACTTGA_NNNNGTATC_3,ACTTGA_NNNNTCAGC_3,GATCAG_NNNNACGCA_3,GATCAG_NNNNCGCTC_3,GATCAG_NNNNCTAGC_3,GATCAG_NNNNGACTC_3,GATCAG_NNNNGAGAC_3,GATCAG_NNNNGCTAC_3,GATCAG_NNNNGTATC_3,GATCAG_NNNNTCAGC_3,TAGCTT_NNNNACGCA_3,TAGCTT_NNNNCGCTC_3,TAGCTT_NNNNCTAGC_3,TAGCTT_NNNNGACTC_3,TAGCTT_NNNNGAGAC_3,TAGCTT_NNNNGCTAC_3,TAGCTT_NNNNGTATC_3,TAGCTT_NNNNTCAGC_3,GGCTAC_NNNNACGCA_3,GGCTAC_NNNNCGCTC_3,GGCTAC_NNNNCTAGC_3,GGCTAC_NNNNGACTC_3,GGCTAC_NNNNGAGAC_3,GGCTAC_NNNNGCTAC_3,GGCTAC_NNNNGTATC_3,GGCTAC_NNNNTCAGC_3,CTTGTA_NNNNACGCA_3,CTTGTA_NNNNCGCTC_3,CTTGTA_NNNNCTAGC_3,CTTGTA_NNNNGACTC_3,CTTGTA_NNNNGAGAC_3,CTTGTA_NNNNGCTAC_3,CTTGTA_NNNNGTATC_3,CTTGTA_NNNNTCAGC_3,ATCACG_NNNNACGCA_4,ATCACG_NNNNCGCTC_4,ATCACG_NNNNCTAGC_4,ATCACG_NNNNGACTC_4,ATCACG_NNNNGAGAC_4,ATCACG_NNNNGCTAC_4,ATCACG_NNNNGTATC_4,ATCACG_NNNNTCAGC_4,CGATGT_NNNNACGCA_4,CGATGT_NNNNCGCTC_4,CGATGT_NNNNCTAGC_4,CGATGT_NNNNGACTC_4,CGATGT_NNNNGAGAC_4,CGATGT_NNNNGCTAC_4,CGATGT_NNNNGTATC_4,CGATGT_NNNNTCAGC_4,TTAGGC_NNNNACGCA_4,TTAGGC_NNNNCGCTC_4,TTAGGC_NNNNCTAGC_4,TTAGGC_NNNNGACTC_4,TTAGGC_NNNNGAGAC_4,TTAGGC_NNNNGCTAC_4,TTAGGC_NNNNGTATC_4,TTAGGC_NNNNTCAGC_4,TGACCA_NNNNACGCA_4,TGACCA_NNNNCGCTC_4,TGACCA_NNNNCTAGC_4,TGACCA_NNNNGACTC_4,TGACCA_NNNNGAGAC_4,TGACCA_NNNNGCTAC_4,TGACCA_NNNNGTATC_4,TGACCA_NNNNTCAGC_4,ACAGTG_NNNNACGCA_4,ACAGTG_NNNNCGCTC_4,ACAGTG_NNNNCTAGC_4,ACAGTG_NNNNGACTC_4,ACAGTG_NNNNGAGAC_4,ACAGTG_NNNNGCTAC_4,ACAGTG_NNNNGTATC_4,ACAGTG_NNNNTCAGC_4,GCCAAT_NNNNACGCA_4,GCCAAT_NNNNCGCTC_4,GCCAAT_NNNNCTAGC_4,GCCAAT_NNNNGACTC_4,GCCAAT_NNNNGAGAC_4,GCCAAT_NNNNGCTAC_4,GCCAAT_NNNNGTATC_4,GCCAAT_NNNNTCAGC_4,CAGATC_NNNNACGCA_4,CAGATC_NNNNCGCTC_4,CAGATC_NNNNCTAGC_4,CAGATC_NNNNGACTC_4,CAGATC_NNNNGAGAC_4,CAGATC_NNNNGCTAC_4,CAGATC_NNNNGTATC_4,CAGATC_NNNNTCAGC_4,ACTTGA_NNNNACGCA_4,ACTTGA_NNNNCGCTC_4,ACTTGA_NNNNCTAGC_4,ACTTGA_NNNNGACTC_4,ACTTGA_NNNNGAGAC_4,ACTTGA_NNNNGCTAC_4,ACTTGA_NNNNGTATC_4,ACTTGA_NNNNTCAGC_4,GATCAG_NNNNACGCA_4,GATCAG_NNNNCGCTC_4,GATCAG_NNNNCTAGC_4,GATCAG_NNNNGACTC_4,GATCAG_NNNNGAGAC_4,GATCAG_NNNNGCTAC_4,GATCAG_NNNNGTATC_4,GATCAG_NNNNTCAGC_4,TAGCTT_NNNNACGCA_4,TAGCTT_NNNNCGCTC_4,TAGCTT_NNNNCTAGC_4,TAGCTT_NNNNGACTC_4,TAGCTT_NNNNGAGAC_4,TAGCTT_NNNNGCTAC_4,TAGCTT_NNNNGTATC_4,TAGCTT_NNNNTCAGC_4,GGCTAC_NNNNACGCA_4,GGCTAC_NNNNCGCTC_4,GGCTAC_NNNNCTAGC_4,GGCTAC_NNNNGACTC_4,GGCTAC_NNNNGAGAC_4,GGCTAC_NNNNGCTAC_4,GGCTAC_NNNNGTATC_4,GGCTAC_NNNNTCAGC_4,CTTGTA_NNNNACGCA_4,CTTGTA_NNNNCGCTC_4,CTTGTA_NNNNCTAGC_4,CTTGTA_NNNNGACTC_4,CTTGTA_NNNNGAGAC_4,CTTGTA_NNNNGCTAC_4,CTTGTA_NNNNGTATC_4,CTTGTA_NNNNTCAGC_4', 'output_dir': './test/sample_data/illumina/result/20120614', 'configpath_orig': '', 'require_distal': True, 'date': '2012-08-13', 'input_files': '', 'database_host': 'vampsdev', 'compressed': False}

data_object['CGATGT_NNNNGCTAC_3'] = {'last_name': 'user', 'dna_region': 'v6', 'dataset': 'SMPL42_3', 'dataset_description': 'My dataset description', 'insert_size': '230', 'first_name': 'guest', 'funding': 'My favorite project', 'read_length': '101', 'seq_operator': 'JV', 'overlap': 'complete', 'email': 'guest@guest.com', 'barcode_index': 'CGATGT', 'project_description': 'My project description', 'run': '20120613', 'adaptor': '', 'barcode': '', 'file_prefix': 'SMPL42_3', 'run_key': 'NNNNGCTAC', 'data_owner': 'guest', 'institution': 'guest institution', 'lane': '3', 'project_title': 'My project title', 'env_sample_source_id': '130', 'primer_suite': 'Bacterial v6 Suite', 'project': 'AAA_BBB_Bv6', 'tubelabel': 'SMPL42', 'amp_operator': 'JR'}

data_object['ATCACG_NNNNCGCTC_3'] = {'last_name': 'user', 'dna_region': 'v6', 'dataset': 'SMPL5_3', 'dataset_description': 'My dataset description', 'insert_size': '230', 'first_name': 'guest', 'funding': 'My favorite project', 'read_length': '101', 'seq_operator': 'JV', 'overlap': 'complete', 'email': 'guest@guest.com', 'barcode_index': 'ATCACG', 'project_description': 'My project description', 'run': '20120613', 'adaptor': '', 'barcode': '', 'file_prefix': 'SMPL5_3', 'run_key': 'NNNNCGCTC', 'data_owner': 'guest', 'institution': 'guest institution', 'lane': '3', 'project_title': 'My project title', 'env_sample_source_id': '130', 'primer_suite': 'Bacterial v6 Suite', 'project': 'AAA_BBB_Bv6', 'tubelabel': 'SMPL5', 'amp_operator': 'JR'}

data_object['ATCACG_NNNNTCAGC_3'] = {'last_name': 'user', 'dna_region': 'v6', 'dataset': 'SMPL53_3', 'dataset_description': 'My dataset description', 'insert_size': '230', 'first_name': 'guest', 'funding': 'My favorite project', 'read_length': '101', 'seq_operator': 'JV', 'overlap': 'complete', 'email': 'guest@guest.com', 'barcode_index': 'ATCACG', 'project_description': 'My project description', 'run': '20120613', 'adaptor': '', 'barcode': '', 'file_prefix': 'SMPL53_3', 'run_key': 'NNNNTCAGC', 'data_owner': 'guest', 'institution': 'guest institution', 'lane': '3', 'project_title': 'My project title', 'env_sample_source_id': '130', 'primer_suite': 'Bacterial v6 Suite', 'project': 'AAA_BBB_Bv6', 'tubelabel': 'SMPL53', 'amp_operator': 'JR'}

data_object['CGATGT_NNNNTCAGC_3'] = {'last_name': 'user', 'dna_region': 'v6', 'dataset': 'SMPL61_3', 'dataset_description': 'My dataset description', 'insert_size': '230', 'first_name': 'guest', 'funding': 'My favorite project', 'read_length': '101', 'seq_operator': 'JV', 'overlap': 'complete', 'email': 'guest@guest.com', 'barcode_index': 'CGATGT', 'project_description': 'My project description', 'run': '20120613', 'adaptor': '', 'barcode': '', 'file_prefix': 'SMPL61_3', 'run_key': 'NNNNTCAGC', 'data_owner': 'guest', 'institution': 'guest institution', 'lane': '3', 'project_title': 'My project title', 'env_sample_source_id': '130', 'primer_suite': 'Bacterial v6 Suite', 'project': 'AAA_BBB_Bv6', 'tubelabel': 'SMPL61', 'amp_operator': 'JR'}

data_object['ATCACG_NNNNGTATC_3'] = {'last_name': 'user', 'dna_region': 'v6', 'dataset': 'SMPL79_3', 'dataset_description': 'My dataset description', 'insert_size': '230', 'first_name': 'guest', 'funding': 'My favorite project', 'read_length': '101', 'seq_operator': 'JV', 'overlap': 'complete', 'email': 'guest@guest.com', 'barcode_index': 'ATCACG', 'project_description': 'My project description', 'run': '20120613', 'adaptor': '', 'barcode': '', 'file_prefix': 'SMPL79_3', 'run_key': 'NNNNGTATC', 'data_owner': 'guest', 'institution': 'guest institution', 'lane': '3', 'project_title': 'My project title', 'env_sample_source_id': '130', 'primer_suite': 'Bacterial v6 Suite', 'project': 'AAA_BBB_Bv6', 'tubelabel': 'SMPL79', 'amp_operator': 'JR'}

data_object['ATCACG_NNNNGAGAC_3'] = {'last_name': 'user', 'dna_region': 'v6', 'dataset': 'SMPL8_3', 'dataset_description': 'My dataset description', 'insert_size': '230', 'first_name': 'guest', 'funding': 'My favorite project', 'read_length': '101', 'seq_operator': 'JV', 'overlap': 'complete', 'email': 'guest@guest.com', 'barcode_index': 'ATCACG', 'project_description': 'My project description', 'run': '20120613', 'adaptor': '', 'barcode': '', 'file_prefix': 'SMPL8_3', 'run_key': 'NNNNGAGAC', 'data_owner': 'guest', 'institution': 'guest institution', 'lane': '3', 'project_title': 'My project title', 'env_sample_source_id': '130', 'primer_suite': 'Bacterial v6 Suite', 'project': 'AAA_BBB_Bv6', 'tubelabel': 'SMPL8', 'amp_operator': 'JR'}

data_object['CGATGT_NNNNGTATC_3'] = {'last_name': 'user', 'dna_region': 'v6', 'dataset': 'SMPL80_3', 'dataset_description': 'My dataset description', 'insert_size': '230', 'first_name': 'guest', 'funding': 'My favorite project', 'read_length': '101', 'seq_operator': 'JV', 'overlap': 'complete', 'email': 'guest@guest.com', 'barcode_index': 'CGATGT', 'project_description': 'My project description', 'run': '20120613', 'adaptor': '', 'barcode': '', 'file_prefix': 'SMPL80_3', 'run_key': 'NNNNGTATC', 'data_owner': 'guest', 'institution': 'guest institution', 'lane': '3', 'project_title': 'My project title', 'env_sample_source_id': '130', 'primer_suite': 'Bacterial v6 Suite', 'project': 'AAA_BBB_Bv6', 'tubelabel': 'SMPL80', 'amp_operator': 'JR'}

data_object['CGATGT_NNNNGAGAC_3'] = {'last_name': 'user', 'dna_region': 'v6', 'dataset': 'SMPL9_3', 'dataset_description': 'My dataset description', 'insert_size': '230', 'first_name': 'guest', 'funding': 'My favorite project', 'read_length': '101', 'seq_operator': 'JV', 'overlap': 'complete', 'email': 'guest@guest.com', 'barcode_index': 'CGATGT', 'project_description': 'My project description', 'run': '20120613', 'adaptor': '', 'barcode': '', 'file_prefix': 'SMPL9_3', 'run_key': 'NNNNGAGAC', 'data_owner': 'guest', 'institution': 'guest institution', 'lane': '3', 'project_title': 'My project title', 'env_sample_source_id': '130', 'primer_suite': 'Bacterial v6 Suite', 'project': 'AAA_BBB_Bv6', 'tubelabel': 'SMPL9', 'amp_operator': 'JR'}

data_object['ATCACG_NNNNCTAGC_3'] = {'last_name': 'user', 'dna_region': 'v6', 'dataset': 'SMPL90_3', 'dataset_description': 'My dataset description', 'insert_size': '230', 'first_name': 'guest', 'funding': 'My favorite project', 'read_length': '101', 'seq_operator': 'JV', 'overlap': 'complete', 'email': 'guest@guest.com', 'barcode_index': 'ATCACG', 'project_description': 'My project description', 'run': '20120613', 'adaptor': '', 'barcode': '', 'file_prefix': 'SMPL90_3', 'run_key': 'NNNNCTAGC', 'data_owner': 'guest', 'institution': 'guest institution', 'lane': '3', 'project_title': 'My project title', 'env_sample_source_id': '130', 'primer_suite': 'Bacterial v6 Suite', 'project': 'AAA_BBB_Bv6', 'tubelabel': 'SMPL90', 'amp_operator': 'JR'}

data_object['CGATGT_NNNNCTAGC_3'] = {'last_name': 'user', 'dna_region': 'v6', 'dataset': 'SMPL91_3', 'dataset_description': 'My dataset description', 'insert_size': '230', 'first_name': 'guest', 'funding': 'My favorite project', 'read_length': '101', 'seq_operator': 'JV', 'overlap': 'complete', 'email': 'guest@guest.com', 'barcode_index': 'CGATGT', 'project_description': 'My project description', 'run': '20120613', 'adaptor': '', 'barcode': '', 'file_prefix': 'SMPL91_3', 'run_key': 'NNNNCTAGC', 'data_owner': 'guest', 'institution': 'guest institution', 'lane': '3', 'project_title': 'My project title', 'env_sample_source_id': '130', 'primer_suite': 'Bacterial v6 Suite', 'project': 'AAA_BBB_Bv6', 'tubelabel': 'SMPL91', 'amp_operator': 'JR'}


file_names_list = ['./test/sample_data/illumina/Project_J_v6_30/../result/20120614/analysis/perfect_reads/SMPL42_3-PERFECT_reads.fa.unique',
'./test/sample_data/illumina/Project_J_v6_30/../result/20120614/analysis/perfect_reads/SMPL5_3-PERFECT_reads.fa.unique',
'./test/sample_data/illumina/Project_J_v6_30/../result/20120614/analysis/perfect_reads/SMPL53_3-PERFECT_reads.fa.unique',
'./test/sample_data/illumina/Project_J_v6_30/../result/20120614/analysis/perfect_reads/SMPL61_3-PERFECT_reads.fa.unique',
'./test/sample_data/illumina/Project_J_v6_30/../result/20120614/analysis/perfect_reads/SMPL79_3-PERFECT_reads.fa.unique',
'./test/sample_data/illumina/Project_J_v6_30/../result/20120614/analysis/perfect_reads/SMPL8_3-PERFECT_reads.fa.unique',
'./test/sample_data/illumina/Project_J_v6_30/../result/20120614/analysis/perfect_reads/SMPL80_3-PERFECT_reads.fa.unique',
'./test/sample_data/illumina/Project_J_v6_30/../result/20120614/analysis/perfect_reads/SMPL9_3-PERFECT_reads.fa.unique',
'./test/sample_data/illumina/Project_J_v6_30/../result/20120614/analysis/perfect_reads/SMPL90_3-PERFECT_reads.fa.unique',
'./test/sample_data/illumina/Project_J_v6_30/../result/20120614/analysis/perfect_reads/SMPL91_3-PERFECT_reads.fa.unique']

gast_dict = {'A5BCDEF3:25:Z987YXWUQ:3:1101:4387:2211 1:N:0:ATCACG|frequency:1': ['Bacteria;Proteobacteria;Gammaproteobacteria',
 '0.017',
 'class',
 '1',
 '100',
 'class',
 '1;1;1;0;0;0;0;0',
 '100;100;100;0;0;0;0;0',
 '0;0;0;100;100;100;100;100',
 'v6_BW306\n'],
 'read_id': ['taxonomy',
 'distance',
 'rank',
 'refssu_count',
 'vote',
 'minrank',
 'taxa_counts',
 'max_pcts',
 'na_pcts',
 'refhvr_ids\n']}

gast_dict1 = {'read_id': ['taxonomy',
 'distance',
 'rank',
 'refssu_count',
 'vote',
 'minrank',
 'taxa_counts',
 'max_pcts',
 'na_pcts',
 'refhvr_ids\n'],
 'A5BCDEF3:25:Z987YXWUQ:3:1101:4849:2186 1:N:0:ATCACG|frequency:1': ['Bacteria;Proteobacteria;Deltaproteobacteria',
 '0.05',
 'class',
 '1',
 '100',
 'class',
 '1;1;1;0;0;0;0;0',
 '100;100;100;0;0;0;0;0',
 '0;0;0;100;100;100;100;100',
 'v6_DS955\n']}

gast_dict2 = {'A5BCDEF3:25:Z987YXWUQ:3:1101:4387:2211 1:N:0:ATCACG|frequency:1': ['Bacteria;Proteobacteria;Gammaproteobacteria',
 '0.017',
 'class',
 '1',
 '100',
 'class',
 '1;1;1;0;0;0;0;0',
 '100;100;100;0;0;0;0;0',
 '0;0;0;100;100;100;100;100',
 'v6_BW306\n'],
 'read_id': ['taxonomy',
 'distance',
 'rank',
 'refssu_count',
 'vote',
 'minrank',
 'taxa_counts',
 'max_pcts',
 'na_pcts',
 'refhvr_ids\n']}

dataset_emails = {'SMPL42_3': 'guest@guest.com',
'SMPL5_3': 'guest@guest.com',
'SMPL53_3': 'guest@guest.com',
'SMPL61_3': 'guest@guest.com',
'SMPL79_3': 'guest@guest.com',
'SMPL8_3': 'guest@guest.com',
'SMPL80_3': 'guest@guest.com',
'SMPL9_3': 'guest@guest.com',
'SMPL90_3': 'guest@guest.com',
'SMPL91_3': 'guest@guest.com'}
