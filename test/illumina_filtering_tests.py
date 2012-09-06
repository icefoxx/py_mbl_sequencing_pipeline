import unittest
import sys
import os
import shutil
sys.path.append("../")

import pipeline.illumina_filtering as ill_f

from pipeline.run import Run
import test.test_factory as fake_data_object
from pipeline.galaxy.fastq import fastqReader, fastqWriter

"""
to run: python pipeline/test/illumina_filtering_tests.py -v
"""

class IlluminaFilteringTestCase(unittest.TestCase): 
    @classmethod  
    def setUpClass(cls):
        if os.path.exists("test/sample_data/illumina/result/20120614"):
            shutil.rmtree("test/sample_data/illumina/result/20120614")
        data_object = fake_data_object.data_object
        pi_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
        cls._runobj = Run(data_object, pi_path)    
        if not os.path.exists(cls._runobj.output_dir):
            os.mkdir(cls._runobj.output_dir)
        cls._illumina_filtering = ill_f.IlluminaFiltering(cls._runobj)
        in_filepath  = "./test/sample_data/illumina/Project_J_v6_30/Sample_v6_Amplicon_IDX1/v6_Amplicon_IDX1_ATCACG_L003_R1_001.fastq"    
        cls._fp      = cls._illumina_filtering.open_in_file(in_filepath)      
        cls._format  = 'sanger'  


    @classmethod  
    def tearDownClass(cls):
        print "\nDone!"
        
    "Run setUp to clean db and fill out run info"
        
    def test_01_compare(self):
        result_true = self._illumina_filtering.compare(1, "<", 2)
        self.assertTrue(result_true)
        result_false = self._illumina_filtering.compare(1, ">", 2)
        self.assertEqual(result_false, False)
        
    def test_02_count_of_Ns(self):
        count_of_Ns  = 0    
        filter_Nx    = True
        "Seq has no Ns"
        seq          = "CGACGGCCATGGCACCTGTATAGGCGTCCCGAAAGAGGGACCTGTTTCCAGGTCTTGCGCCTATATGTCAAACCCGGGTAAGGTTCGTCGGTTAGGATA"    
        self.assertEqual(count_of_Ns, 0)
        "Seq has Ns"
        seq          = "CGACGGCCATGNNGCACCTGTATAGGCGTCCCGAAAGAGGGACCTGTTTCCAGGTCTTGCGCCTATATGTCAAACCCGGGTAAGGTTCGTCGGTTAGGATA"    
        count_of_Ns  = self._illumina_filtering.filter_ns(seq, filter_Nx, count_of_Ns)
        self.assertEqual(count_of_Ns, 1)
        
#        seq          = "CGACGGCCATGNNGCACCTGTATAGGCGTCCCGAAAGAGGGACCTGTTTCCAGGTCTTGCGCCTATATGTCAAACCCGGGTAAGGTTCGTCGGTTAGGATA"    
#        count_of_Ns  = 2    
#        filter_Nx    = 0    
#        failed_fastq = True    
#        out_filepath = "results/illumina_filtering/123001/illumina_filtered/v6_Amplicon_IDX1_ATCACG_L003_R1_001.filtered.fastq"    
#        in_filepath  = "./test/sample_data/illumina/Project_J_v6_30/Sample_v6_Amplicon_IDX1/v6_Amplicon_IDX1_ATCACG_L003_R1_001.fastq"    
#        fp           = self._illumina_filtering.open_in_file(in_filepath)      
#        format       = 'sanger'  
#        fail         = fastqWriter( open( out_filepath+'.failed', 'wb' ), format = format )        
#        self._illumina_filtering.desc_items = ['@D4ZHLFP1', '25', 'B022DACXX', '3', '1101', '5090', '2177 2', 'N', '0', 'ATCACG']    
#        for num_reads, fastq_read in enumerate( fastqReader( fp, format = format ) ):
#            res = self._illumina_filtering.filter_by_ambiguous_bases(seq, count_of_Ns, filter_Nx, failed_fastq, fastq_read, fail)
#            self.assertEqual(res, 3)           
#            break
    
    def test_03_check_chastity(self):
        self.assertEqual(self._illumina_filtering.count_of_unchaste, 0)           
        for num_reads, fastq_read in enumerate( fastqReader(self._fp, format = self._format)):
            desc_items = fastq_read.identifier.split(':')
            self._illumina_filtering.check_chastity(desc_items)
        self.assertEqual(self._illumina_filtering.count_of_unchaste, 1)           
    

#                    first50_maxQ = 30
#                first50_maxQ_count = 34


if __name__ == '__main__':
    unittest.main()

