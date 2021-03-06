import sys
import os
sys.path.append("/xraid/bioware/linux/seqinfo/bin")
sys.path.append("/Users/ashipunova/bin/illumina-utils")
sys.path.append("/bioware/merens-illumina-utils")
# sys.path.append("/bioware/pythonmodules/illumina-utils/")
import fastqlib as fq
import fastalib as fa
from subprocess import call
import ast
from pipeline.utils import Dirs, PipelneUtils
import constants as C

"TODO: add tests and test case"
#from collections import defaultdict

class IlluminaFiles:
    """
    0) from run create all dataset_lines names files in output dir
    1) split fastq files from casava into files with dataset_names
    2) create ini files 
    3) process them through Meren's script
    4) result - files dataset_lane-PERFECT_reads.fa.unique with frequencies - to process with env454upload()    
    
    """
    def __init__(self, runobj):
        self.utils = PipelneUtils()
        self.runobj         = runobj
        self.out_files      = {} 
        self.id_dataset_idx = {}
        self.in_file_path   = self.runobj.input_dir
                
        if self.runobj.vamps_user_upload:
            site = self.runobj.site
            dir_prefix=self.runobj.user+'_'+self.runobj.run
        else:
            site = ''
            dir_prefix = self.runobj.run
        if self.runobj.lane_name:
            lane_name = self.runobj.lane_name
        else:
            lane_name = ''
        
        dirs = Dirs(self.runobj.vamps_user_upload, dir_prefix, self.runobj.platform, lane_name = lane_name, site = site) 

        self.out_file_path = dirs.check_dir(dirs.analysis_dir)
        self.results_path  = dirs.check_dir(dirs.reads_overlap_dir)
        
    def split_files(self, compressed = False):
        """
        TODO: *) fastq_file_names method to collect all file_names with full path or directories_names (see get_all_files()?)
        """   
#        print "compressed = %s" %       compressed
#        compressed = ast.literal_eval(compressed)     
        (in_files_r1, in_files_r2) = self.get_fastq_file_names(self.in_file_path)
        self.read1(in_files_r1, compressed)
        self.read2(in_files_r2, compressed)
        self.create_inis()
        self.close_dataset_files()

#        self.perfect_reads()
#        self.uniq_fa()

    def open_dataset_files(self):
        file_name_base = [i + "_R1" for i in self.runobj.samples.keys()] + [i + "_R2" for i in self.runobj.samples.keys()]
        for f_name in file_name_base:
            output_file = os.path.join(self.out_file_path, f_name + ".fastq")
            self.out_files[f_name] = fq.FastQOutput(output_file)
        self.out_files["unknown"] = fq.FastQOutput(os.path.join(self.out_file_path, "unknown" + ".fastq"))        

    def close_dataset_files(self):
        [o_file[1].close() for o_file in self.out_files.iteritems()] 
        return
   
    def get_all_files(self):
        files = {}
        for dirname, dirnames, filenames in os.walk(self.out_file_path):
            for file_name in filenames:
                full_name = os.path.join(dirname, file_name)
                (file_base, file_extension) = os.path.splitext(os.path.join(dirname, file_name))
                files[full_name] = (file_base, file_extension)
#        print "len(files) = %s" % len(files)
        return files
    
    def perfect_reads(self):
        print "Extract perfect V6 reads:"
        for idx_key in self.runobj.samples.keys():
            file_name = os.path.join(self.out_file_path, idx_key + ".ini")
            program_name = C.perfect_overlap_cmd
            if self.utils.is_local():
                program_name = C.perfect_overlap_cmd_local                    
            try:
                if self.runobj.samples[idx_key].primer_suite.startswith('Archaeal'):
                    call([program_name, file_name, "--archaea"]) 
                else: 
                    call([program_name, file_name])
            except:
                print "Problems with program_name = %s, file_name = %s" % (program_name, file_name)
                raise  


    def partial_overlap_reads(self):
        print "Extract partial_overlap V4V5 reads:"
        for idx_key in self.runobj.samples.keys():
            ini_file_name = os.path.join(self.out_file_path, idx_key + ".ini")
            program_name = C.partial_overlap_cmd
            if self.utils.is_local():
                program_name = C.partial_overlap_cmd_local           
            call([program_name, "--fast-merge", "--compute-qual-dicts", ini_file_name, idx_key])
            
    def filter_mismatches(self, max_mismatch = 3):
        print "Filter mismatches if more then %s" % (max_mismatch)
        n = 0        
        files = self.get_all_files()
        for full_name in files.keys():    
            if files[full_name][0].endswith('_MERGED'):
                n +=1   
#                print "%s fasta file: %s" % (n, full_name)
                program_name = C.filter_mismatch_cmd
                if self.utils.is_local():
                    program_name = C.filter_mismatch_cmd_local
                output_flag = "--output " + full_name + "_FILTERED"                
                call([program_name, full_name, output_flag])
                    
    def uniq_fa(self):
        n = 0        
        print "Uniqueing fasta files"      
        files = self.get_all_files()
        for full_name in files.keys():    
            if files[full_name][1] == ".fa" or files[full_name][0].endswith('_MERGED_FILTERED'):
                n +=1   
#                print "%s fasta file: %s" % (n, full_name)
                program_name = C.fastaunique_cmd
                if self.utils.is_local():
                    program_name = C.fastaunique_cmd_local                
                call([program_name, full_name])

    def create_inis(self):
        for idx_key in self.runobj.samples.keys():
            run_key = idx_key.split('_')[1].replace("N", ".");
            email = self.runobj.samples[idx_key].email
#        for dataset in self.dataset_emails.keys():
#            dataset_idx_base = dataset + "_" + self.dataset_index[dataset]
#            print "dataset = %s, self.dataset_emails[dataset] = %s" % (dataset, self.dataset_emails[dataset])
            text = """[general]
project_name = %s
researcher_email = %s
input_directory = %s
output_directory = %s

[files]
pair_1 = %s
pair_2 = %s
""" % (idx_key, email, self.out_file_path, self.results_path, idx_key + "_R1.fastq", idx_key + "_R2.fastq")

            "That's for v4v5 miseq illumina" 
            if not self.runobj.do_perfect:    
                text += """
# following section is optional
[prefixes]
pair_1_prefix = ^""" + run_key + """CCAGCAGC[C,T]GCGGTAA.
pair_2_prefix = ^CCGTC[A,T]ATT[C,T].TTT[G,A]A.T
                """
                
            ini_file_name = os.path.join(self.out_file_path,  idx_key + ".ini")
            self.open_write_close(ini_file_name, text)

    def open_write_close(self, ini_file_name, text):
        ini_file = open(ini_file_name, "w")
        ini_file.write(text)
        ini_file.close()
 
    def get_fastq_file_names(self, f_input_file_path):
        in_files_r1 = []
        in_files_r2 = []
        "TODO: exclude dir with new created files from the loop"
        for dirname, dirnames, filenames in os.walk(f_input_file_path):
            for filename in filenames:
                if filename.find('_R1_') > 0:
                    in_files_r1.append(os.path.join(dirname, filename))
                elif filename.find('_R2_') > 0:
                    in_files_r2.append(os.path.join(dirname, filename))
                else:
                    sys.stderr.write("No read number in the file name: %s\n" % filename)
        return (in_files_r1, in_files_r2)
        
    def read1(self, files_r1, compressed):
        """ loop through the fastq_file_names
            1) e.pair_no = 1, find run_key -> dataset name
            2) collect the relevant part of id
        """
        for file_r1 in files_r1:
            print "FFF1: file %s" % file_r1
            index_sequence = self.get_index(file_r1)
            f_input  = fq.FastQSource(file_r1, compressed)
            while f_input.next():
                e = f_input.entry
                ini_run_key  = index_sequence + "_" + "NNNN" + e.sequence[4:9] + "_" + e.lane_number                
#                ini_run_key  = e.index_sequence + "_" + "NNNN" + e.sequence[4:9] + "_" + e.lane_number                
                if ini_run_key in self.runobj.samples.keys() and int(e.pair_no) == 1:
                    dataset_file_name_base_r1 = ini_run_key + "_R1"
                    if (dataset_file_name_base_r1 in self.out_files.keys()):
                        self.out_files[dataset_file_name_base_r1].store_entry(e)
                        "TODO: make a method:"
                        short_id1 = e.header_line.split()[0]
                        short_id2 = ":".join(e.header_line.split()[1].split(":")[1:])
                        id2 = short_id1 + " 2:" + short_id2
                        self.id_dataset_idx[id2] = ini_run_key
                else:
                    self.out_files["unknown"].store_entry(e)
                    
    def read2(self, files_r2, compressed):
        "3) e.pair_no = 2, find id from 2), assign dataset_name"
        for file_r2 in files_r2:
            print "FFF2: file %s" % file_r2
            f_input  = fq.FastQSource(file_r2, compressed)
            while f_input.next():
                e = f_input.entry
                
                if (int(e.pair_no) == 2) and (e.header_line in self.id_dataset_idx):
                    file_name = self.id_dataset_idx[e.header_line] + "_R2"
                    self.out_files[file_name].store_entry(e)        
                else:
                    self.out_files["unknown"].store_entry(e)

    def get_index(self, file_r1):
        file_name_parts = os.path.basename(file_r1).split("_")
#        if the file name starts with "IDX, then actual idx will be next.
        index = file_name_parts[0]
        if file_name_parts[0].startswith("IDX"):
            index = file_name_parts[1]
        return index
