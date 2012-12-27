import os, sys
from subprocess import check_output
import constants as C
from time import sleep
import datetime
from pipeline.pipelinelogging import logger
from contextlib import closing
import zipfile
import zlib
from string import maketrans
import collections


base_complement_translator = maketrans("ACGTRYMK", "TGCAYRKM")

# the json expected files get loaded and parsed into Unicode strings
# but the asserts won't work comparing unicode to ascii so we need change them
# to plain strings
def convert_unicode_dictionary_to_str(data):
    if isinstance(data, unicode):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert_unicode_dictionary_to_str, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert_unicode_dictionary_to_str, data))
    else:
        return data        


########################################################    
def check_for_Ns(seq):
    """Doc string here.."""
    nCount = seq.count('N') 
    if( nCount > 0 ):
        return nCount
    else:
        return 0

def remove_runkey(seq,runkeys):
    """Doc string here.."""
    found_key = ''
    for key in runkeys:
        if (seq.find(key) == 0):
            found_key = key
            seq = seq[len(key):]
            break
        else:
            continue 
    return found_key, seq
    
def find_sequence_direction( direction = '' ):
    """Doc string here.."""
    seqFwd = 0
    seqRev = 0
    if(direction == 'F'):
        seqFwd = 1
    if(direction == "R"):
        seqRev = 1
        
    if ( not direction or (seqFwd + seqRev) == 0 ):
        return 0
    elif ( (seqFwd + seqRev) == 2 ):
        return "B"
    elif (seqFwd):
        return "F"
    else:
        return "R"

def check_for_quality(rawseq, trimseq, quality_scores):
    """Doc string here.."""
    start = rawseq.find(trimseq)
    end   = start + len(trimseq)
    
    scores = quality_scores[start:end]
    
    return sum(scores,0.0) / len(scores)

def revcomp(sequence):
    reversed = str(sequence[::-1])
    return reversed.translate(base_complement_translator)

def set_trim1():
    return (True,False,False,False)
 
def set_trim2():
    return (True,True,False,False)
 
def set_trim3():
    return (True,True,True,False)
 
def set_chim4():
    return (False,True,False,False)
    
def set_chim5():
    return (False,True,True,False)
 
def set_chim6():
    return (False,True,True,True)
 
def set_gast7():
    return (False,False,True,False)
 
def set_gast8():
    return (False,False,True,True)

def set_vamps9():
    return (False,False,False,True)
 
def set_all10():
    return (True,True,True,True)
    
options = {
        1 : set_trim1,
        2 : set_trim2,
        3 : set_trim3,
        4 : set_chim4,
        5 : set_chim5,
        6 : set_chim6,
        7 : set_gast7,
        8 : set_gast8,
        9 : set_vamps9,
        10 : set_all10,
}
 
def wait_for_cluster_to_finish(my_running_id_list):
    #print 'My IDs',running_id_list
    logger.debug('Max run time set to ' + str(C.cluster_max_wait) + ' seconds')
    logger.debug('These are my running qsub IDs ' + str(my_running_id_list))
    my_working_id_list = my_running_id_list

    counter =0

    sleep(C.cluster_initial_check_interval)
    
    while my_working_id_list:
    
    
        qstat_codes = get_qstat_id_list()
        if not qstat_codes['id']:
            #print 'No qstat ids'
            logger.debug("id list not found: may need to increase initial_interval if you haven't seen running ids.")
            return ('SUCCESS','id list not found','',)
        if 'Eqw' in qstat_codes['code']:
            logger.debug( "Check cluster: may have error code(s), but they may not be mine!")
        
        
        got_one = False
    
        #print 'working ids',my_working_id_list
        if my_working_id_list[0] in qstat_codes['id']:
            
            got_one = True
            name = qstat_codes['name'][qstat_codes['id'].index(my_working_id_list[0])]
            user = qstat_codes['user'][qstat_codes['id'].index(my_working_id_list[0])]
            code = qstat_codes['code'][qstat_codes['id'].index(my_working_id_list[0])]
            
            
            if code == 'Eqw':
                return ('FAIL','Found Eqw code',my_working_id_list[0])
            elif code == 'qw':
                logger.debug("id is still queued: " +  str(my_working_id_list[0]) + " " + str(code))
            elif code == 'r':
                logger.debug("id is still running: " + str(my_working_id_list[0]) + " " + str(code))
            else:
                logger.debug('Unknown qstat code ' + str(code))
        else:
            my_working_id_list = my_working_id_list[1:]
            logger.debug('id finished ' + str(my_working_id_list[0]))
 
        if not my_working_id_list:
            return ('SUCCESS','not my_working_id_list','')
        #if not got_one:
            #print 'IN not got one',
        #    return ('SUCCESS','not got one','')
                
        sleep(C.cluster_check_interval)
        counter = counter + C.cluster_check_interval
        if counter >= C.cluster_max_wait:
            return ('FAIL','Max Time exceeded',C.cluster_max_wait)
    
    return ('FAIL','Unknown','Unknown')
    
def get_qstat_id_list():
    
    # ['139239', '0.55500', 'usearch', 'avoorhis', 'r', '01/22/2012', '09:00:39', 'all.q@grendel-07.bpcservers.pr', '1']
    # 1) id
    # 2) 
    # 3) name
    # 4) username
    # 5) code r=running, Ew=Error
    qstat_cmd = 'qstat'
    qstat_codes={}
    output = check_output(qstat_cmd)
    #print output
    output_list = output.strip().split("\n")[2:]
    qstat_codes['id'] = [n.split()[0] for n in output_list]
    qstat_codes['name'] = [n.split()[2] for n in output_list]
    qstat_codes['user'] = [n.split()[3] for n in output_list]
    qstat_codes['code'] = [n.split()[4] for n in output_list]
    #print 'Found IDs',qstat_ids
 
    
    
    return qstat_codes


def find_key(dic, val):
    """return the first key of dictionary dic given the value"""
    return [k for k, v in dic.iteritems() if v == val][0]
    
def mysort(uniques,names):
    """ Sorts the uniques using the uniques and names hashes:
    
    uniques[lane_tag][trimmed_sequence] = read_id
    names[lane_tag][read_id1] = [read_id1, read_id2, read_id3, read_id4]
    
    returns a list of tuples (read_id, count, sequence) highest to lowest
    """
    sorted_uniques = []
    
    # sorted_names should be list of ids with the highest number at the top
    sorted_names = sorted(names.items(), key=lambda x: len(x[1]), reverse=True)

    for n in sorted_names:
       
        seq = find_key(uniques, n[0])
        sorted_uniques.append( (n[0], len(n[1]),seq) )
    
    return sorted_uniques     

def extract_zipped_file(run_date, outdir, filename):
    """
    
    """
    # check if zipped
    assert os.path.isdir(outdir)
    archivename = os.path.join(outdir,run_date+'.zip')
    if zipfile.is_zipfile(archivename):
        zf = zipfile.ZipFile(archivename, 'r')
        
        try:
            data = zf.read(filename)
        except KeyError:
            print 'ERROR: Did not find %s in zip file' % filename
        else:
            print filename, ':'
            print repr(data)
        print
        zf.close()
    else:
        print "No zipfile archive found:",archivename
                
def zip_up_directory(run_date, dirPath, mode='a'):
    """
    This should be run at the end of each process to zip the files in each directory
    """
    files_to_compress = ['fa','db','names','sff','fasta','fastq']
    assert os.path.isdir(dirPath)
    zipFilePath = os.path.join(dirPath,run_date+'.zip')
    
    zf = zipfile.ZipFile(zipFilePath, mode)
    
    for (archiveDirPath, dirNames, fileNames) in os.walk(dirPath):
        for file in fileNames: 
            if file.split('.')[-1] in files_to_compress:
                filePath = os.path.join(dirPath, file)
                zf.write(filePath, compress_type=zipfile.ZIP_DEFLATED)
                
    zipInfo = zipfile.ZipInfo(zipFilePath)
    
    for i in zf.infolist():
        dt = datetime.datetime(*(i.date_time))
        print "%s\tSize: %sb\tCompressed: %sb\t\tModified: %s" % (i.filename, i.file_size, i.compress_size, dt.ctime())    
        os.remove(i.filename)

    zf.close()
      
class PipelneUtils:
    def __init__(self):
        pass

    def write_seq_frequencies_in_file(self, out_file, fa_file_name, seq_in_file):
        try: 
            with open(out_file, "a") as myfile:
                myfile.write(str(fa_file_name) + ": " + str(seq_in_file) + "\n")
        except Exception:
            print Exception            
    
    def get_all_files(self, out_file_path):
        files = {}
        for dirname, dirnames, filenames in os.walk(out_file_path):
            for file_name in filenames:
                full_name = os.path.join(dirname, file_name)
                (file_base, file_extension) = os.path.splitext(os.path.join(dirname, file_name))
                files[full_name] = (file_base, file_extension)
#        print "len(files) = %s" % len(files)
        return files    

    def is_local(self):
        dev_comps = ['ashipunova.mbl.edu', "as-macbook.home", "as-macbook.local", "Ashipunova.local"]
        if os.uname()[1] in dev_comps:
            return True
        else:
            return False

class Dirs:
    """get input dir from args, create all other dirs
input_dir - directory with fastq or sff files
Output path example: /xraid2-2/g454/run_new_pipeline/illumina/miseq/20121025/analysis/gast
id_number is a run date for MBL and a random number for VAMPS users
"""
    def __init__(self, runobj):
        self.utils             = PipelneUtils()
        self.analysis_dir      = None 
        self.check_and_make_analysis_dir(runobj)
        self.gast_dir          = os.path.join(self.analysis_dir, C.gast_dir)
        self.reads_overlap_dir = os.path.join(self.analysis_dir, C.reads_overlap_dir)
        self.vamps_upload_dir  = os.path.join(self.analysis_dir, C.vamps_upload_dir)
        self.chimera_dir       = os.path.join(self.analysis_dir, C.chimera_dir)
        self.trimming_dir      = os.path.join(self.analysis_dir, C.trimming_dir)        
        
    def check_and_make_dir(self, dir_name):
#        if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
        except OSError:
            if os.path.isdir(dir_name):
                print "\nDirectory %s already exists and will be overwritten."  % (dir_name)
                confirm_msg = "Do you want to continue? (Yes / No) "
                answer = raw_input(confirm_msg)
                if answer != 'Yes':
                    sys.exit()
                elif answer == 'Yes':
                    pass

#                print "Directory %s already exists and will be overwritten"
            else:
            # There was an error on creation, so make sure we know about it
                raise    
        return dir_name
    
    def check_and_make_analysis_dir(self, runobj):      
        if 'vamps_user_upload' in runobj.keys():
            id_number = None
            root_dir  = C.output_root_vamps_users
        else:
            id_number = runobj['run']
            root_dir  = C.output_root_mbl
        if self.utils.is_local():
            root_dir  = '/Users/ashipunova/BPC/py_mbl_sequencing_pipeline/results'

        self.analysis_dir = os.path.join(root_dir, runobj['platform'], id_number, C.analysis_dir)
        self.check_and_make_dir(self.analysis_dir)
    
    def create_output_dirs(self, runobj):
        self.check_and_make_dir(self.gast_dir)
        self.check_and_make_dir(self.reads_overlap_dir)
        self.check_and_make_dir(self.vamps_upload_dir)
        self.check_and_make_dir(self.chimera_dir)
        self.check_and_make_dir(self.trimming_dir)
        
if __name__=='__main__':
    print "GTTCAAAGAYTCGATGATTCAC"
    print revcomp("GTTCAAAGAYTCGATGATTCAC")




