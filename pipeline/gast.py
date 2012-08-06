import subprocess
import sys, os,stat
import time
import shutil
from pipeline.pipelinelogging import logger
#import logging
import constants as C
import re
from types import *

class Gast:
    """Doc string here.."""
    Name = "GAST"
    def __init__(self, run = None, idx_keys=None):

        self.run     = run
        
        self.test = True
       
        self.basedir = self.run.output_dir
        
        self.use_cluster = self.run.use_cluster
        
        os.environ['SGE_ROOT']='/usr/local/sge'
        os.environ['SGE_CELL']='grendel'
        path = os.environ['PATH']
        os.environ['PATH'] = '/usr/local/sge/bin/lx24-amd64:'+path
        
        
       
        # If we are here from a vamps gast process
        # then there should be just one dataset to gast
        # but if MBL pipe then many datasets are prbably involved.
        self.refdb_dir = C.ref_database_dir
        
        print self.run.input_files
        
        
        
    def clustergast(self, idx_keys):
        """
        clustergast - runs the GAST pipeline on the cluster.
               GAST uses UClust to identify the best matches of a read sequence
               to references sequences in a reference database.
               The uniques and names files have previously been created in trim_run.py.
        """
        logger.info("Starting Clustergast")
        self.run.run_status_file_h.write("Starting clustergast\n")
        # Step1: create empty gast table in database: gast_<rundate>
        # Step2: Count the number of sequences so the job can be split for nodes
        # $facount = `grep -c \">\" $fasta_uniqs_filename`;
        # $calcs = `/bioware/seqinfo/bin/calcnodes -t $facount -n $nodes -f 1`;

        #   /bioware/seqinfo/bin/fastasampler -n $start,$end ${gastDir}/${fasta_uniqs_filename} $tmp_fasta_filename
        #   $usearch_binary --global --query $tmp_fasta_filename --iddef 3 --gapopen 6I/1E --db $refhvr_fa --uc $tmp_usearch_filename --maxaccepts $max_accepts --maxrejects $max_rejects --id $pctid_threshold
        #   # sort the results for valid hits, saving only the ids and pct identity
        #   grep -P \"^H\\t\" $tmp_usearch_filename | sed -e 's/|.*\$//' | awk '{print \$9 \"\\t\" \$4 \"\\t\" \$10 \"\\t\" \$8}' | sort -k1,1b -k2,2gr | clustergast_tophit > $gast_filename
        #   Submit the script
        #   /usr/local/sge/bin/lx24-amd64/qsub $qsub_priority $script_filename
 
        
        
        calcnodes = C.calcnodes_cmd
        sqlImportCommand = C.mysqlimport_cmd
        #qsub = '/usr/local/sge/bin/lx24-amd64/qsub'
        clusterize = C.clusterize_cmd
        



        ###################################################################
        # use fasta.uniques file
        # split into smaller files
        # usearch --cluster each
        #######################################
        #
        # Split the uniques fasta and run UClust per node
        #
        #######################################
        qsub_prefix = 'clustergast_sub_'
        gast_prefix = 'gast_'
        if self.use_cluster:
            logger.info("Using cluster for clustergast")
        else:
            logger.info("Not using cluster")
        for key in idx_keys:
            cluster_nodes = C.cluster_nodes
            logger.info("Cluster nodes set to: "+str(cluster_nodes))
            output_dir = os.path.join(self.basedir,key)
            if not os.path.exists(output_dir):	
                os.mkdir(output_dir)
            
            print 'OUT',output_dir
            # find gast_idr
            gast_dir = os.path.join(output_dir,'gast')
            print 'GAST',gast_dir
            if not os.path.exists(gast_dir):	
                os.mkdir(gast_dir)
            else:
                # empty then recreate directory
                shutil.rmtree(gast_dir)
                os.mkdir(gast_dir)
                
                
            if key in self.run.samples:
                dna_region = self.run.samples[key].dna_region
            else:            
                dna_region = self.run.dna_region
            if not dna_region:
                logger.error("clustergast: We have no DNA Region: Setting dna_region to 'unknown'")
                dna_region = 'unknown'
                
            (refdb,taxdb) = self.get_reference_databases(dna_region)
            print 'DBs',refdb,taxdb
            
            # if no dna_region OR no refdb can be found then use
            # refssu
            #if refdb contains refssu
            #the add this to grep command
            #and change usearch to usearch64
            
                
            unique_file = os.path.join(output_dir, key+'.unique.fa')
            print 'UNIQUE FILE',unique_file
            

            #print gast_dir
            #sys.exit("EXIT")
            
            
            i = 0
            if cluster_nodes:
                grep_cmd = ['grep','-c','>',unique_file]
                logger.debug( ' '.join(grep_cmd) )
                facount = subprocess.check_output(grep_cmd).strip()
                logger.debug( key+' count '+facount)
                calcnode_cmd = [calcnodes,'-t',str(facount),'-n',str(cluster_nodes),'-f','1']
                
                calcout = subprocess.check_output(calcnode_cmd).strip()
                logger.debug("calcout:\n"+calcout)
                #calcout:
                # node=1 start=1 end=1 rows=1
                # node=2 start=2 end=2 rows=1
                # node=3 start=3 end=3 rows=1           
                lines = calcout.split("\n")
                gast_file_list = []
                for line in lines:
                    i += 1
                    if i >= cluster_nodes:
                        continue
                    script_filename = os.path.join(gast_dir,qsub_prefix + str(i))
                    gast_filename   = os.path.join(gast_dir, gast_prefix + str(i))
                    fastasamp_filename = os.path.join(gast_dir, 'samp_' + str(i))
                    clustergast_filename   = os.path.join(gast_dir, key+".gast_" + str(i))
                    gast_file_list.append(clustergast_filename)
                    usearch_filename= os.path.join(gast_dir, "uc_" + str(i))
                    log_file = os.path.join(gast_dir, 'clustergast.log_' + str(i))
                    
                    data = line.split()
                    
                    if len(data) < 2:
                        continue
                    start = data[1].split('=')[1]
                    end  = data[2].split('=')[1]
                    
                    if self.use_cluster:
                        fh = open(script_filename,'w')
                        qstat_name = "gast" + key + '_' + self.run.run + "_" + str(i)
                        fh.write("#!/bin/csh\n")
                        fh.write("#$ -j y\n" )
                        fh.write("#$ -o " + log_file + "\n")
                        fh.write("#$ -N " + qstat_name + "\n\n")
                        #fh.write("source /xraid/bioware/Modules/etc/profile.modules\n");
                        #fh.write("module load bioware\n\n");
    
                        # setup environment
                        fh.write("source /xraid/bioware/Modules/etc/profile.modules\n")
                        fh.write("module load bioware\n\n")
                    
                    cmd1 = self.get_fastasampler_cmd(unique_file, fastasamp_filename,start,end)
                    

                    logger.debug("fastasampler command: "+cmd1)
                    
                    if self.use_cluster:
                        fh.write(cmd1 + "\n")
                    else:
                        subprocess.call(cmd1,shell=True)
                    
                    cmd2 = self.get_usearch_cmd(fastasamp_filename, refdb, usearch_filename)

                    logger.debug("usearch command: "+cmd2)
                    print 'usearch',cmd2
                    if self.use_cluster:
                        fh.write(cmd2 + "\n")
                    else:
                        subprocess.call(cmd2,shell=True)
                    
                    cmd3 = self.get_grep_cmd(usearch_filename, clustergast_filename)

                    logger.debug("grep command: "+cmd3)
                    if self.use_cluster:                
                        fh.write(cmd3 + "\n")
                        fh.close()
                        
                        # make script executable and run it
                        os.chmod(script_filename, stat.S_IRWXU)
                        qsub_cmd = clusterize + " " + script_filename
                        
                        # on vamps and vampsdev qsub cannot be run - unless you call it from the
                        # cluster aware directories /xraid2-2/vampsweb/vamps and /xraid2-2/vampsweb/vampsdev
                        qsub_cmd = C.qsub_cmd + " " + script_filename
                        logger.debug("qsub command: "+qsub_cmd)
                        
                        #subprocess.call(qsub_cmd, shell=True)
                        proc = subprocess.Popen(qsub_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        # proc.communicate will block - probably not what we want
                        #(stdout, stderr) = proc.communicate() #block the last onehere
                        #print stderr,stdout
    
                    else:
                        subprocess.call(cmd3,shell=True)
                        print cmd3
            
            else:
                #fastasamp_filename = os.path.join(gast_dir, 'samp')
                usearch_filename= os.path.join(gast_dir, "uc")
                clustergast_filename_single   = os.path.join(gast_dir, "gast"+dna_region)
                print usearch_filename,clustergast_filename_single
                cmd1 = self.get_usearch_cmd(unique_file,refdb,usearch_filename)
                print cmd1
                subprocess.call(cmd1,shell=True)
                cmd2 = self.get_grep_cmd(usearch_filename, clustergast_filename_single)
                print cmd2
                subprocess.call(cmd2,shell=True)
                
            if self.use_cluster:
                # wait here for all the clustergast scripts to finish
                temp_file_list = gast_file_list
            
                c = False
                maxwaittime = C.maxwaittime  # seconds
                sleeptime   = C.sleeptime    # seconds
                counter = 0
                while c == False:
                    counter += 1
                    if counter >= maxwaittime / sleeptime:
                        raise Exception("Max wait time exceeded in gast.py")
                    for index, file in enumerate(temp_file_list):
                        #print temp_file_list
                        if os.path.exists(file) and os.path.getsize(file) > 0:
                            # remove from tmp list
                            logger.debug("Found file now removing from list: "+file)
                            temp_file_list = temp_file_list[:index] + temp_file_list[index+1:]
                    
                    if temp_file_list:
                        logger.info("waiting for clustergast files to fill...")
                        logger.debug(' '.join(temp_file_list))
                        logger.info("\ttime: "+str(counter * sleeptime)+" | files left: "+str(len(temp_file_list)))
                        time.sleep(sleeptime)
                    else:
                        c = True
                    
            # now concatenate all the clustergast_files into one file (if they were split)
            if cluster_nodes:
                # gast file
                clustergast_filename_single   = os.path.join(gast_dir, "gast"+dna_region)
                clustergast_fh = open(clustergast_filename_single,'w')
                # have to turn off cluster above to be able to 'find' these files for concatenation
                for n in range(1,i-1):
                    #cmd = "cat "+ gast_dir + key+".gast_" + str(n) + " >> " + gast_dir + key+".gast"
                    file = os.path.join(gast_dir, key+".gast_" + str(n))
                    if(os.path.exists(file)):                    
                        shutil.copyfileobj(open(file,'rb'), clustergast_fh)
                    else:
                        logger.info( "Could not find file: "+os.path.basename(file)+" Skipping")

                clustergast_fh.flush()
                clustergast_fh.close()
            
        if not self.test:    
            # remove tmp files
            for n in range(i+1):
                #print "Trying to remove "+os.path.join(gast_dir,"uc_"+str(n))
                if os.path.exists(os.path.join(gast_dir,"uc_"+str(n))):
                    os.remove(os.path.join(gast_dir,"uc_"+str(n)))
                    pass
                #print "Trying to remove "+os.path.join(gast_dir,"samp_"+str(n))
                if os.path.exists(os.path.join(gast_dir,"samp_"+str(n))):    
                    os.remove(os.path.join(gast_dir,"samp_"+str(n)))
                    pass
                #print "Trying to remove "+os.path.join(self.gast_dir,key+".gast_"+str(n))
                if os.path.exists(os.path.join(gast_dir,key+".gast_"+str(n))):    
                    os.remove(os.path.join(gast_dir,key+".gast_"+str(n)))
                    pass
                    
                    
        
        print "Finished clustergast"
        logger.info("Finished clustergast")
        return ("SUCCESS","Clustergast")
    
        
            
    def gast_cleanup(self, idx_keys):
        """
        gast_cleanup - follows clustergast, explodes the data and copies to gast_concat and gast files
        """
        logger.info("Starting GAST Cleanup")
        self.run.run_status_file_h.write("Starting gast_cleanup\n")
        for key in idx_keys:
            output_dir = os.path.join(self.basedir,key)
            gast_dir = os.path.join(output_dir,'gast')
            if key in self.run.samples:
                dna_region = self.run.samples[key].dna_region
            else:            
                dna_region = self.run.dna_region
            if not dna_region:
                logger.error("gast_cleanup: We have no DNA Region: Setting dna_region to 'unknown'")
                self.run.run_status_file_h.write("gast_cleanup: We have no DNA Region: Setting dna_region to 'unknown'\n")
                dna_region = 'unknown'
            # find gast_dir
            

            # for vamps user upload
            # basedir is like avoorhis_3453211
            # and outdir is like avoorhis_3453211/2012-06-25
            # for MBL pipeline
            # basedir is like 1_AGTCG
            # and outdir is like 1_AGTCG/2012-06-25
            
            unique_file = os.path.join(output_dir,key+'.unique.fa')
            names_file = os.path.join(output_dir,key+'.names')
            #print 'names file',names_file
            
            if not os.path.exists(gast_dir):
                logger.error("Could not find gast directory: "+gast_dir+" Exiting")
                sys.exit()
            clustergast_filename_single   = os.path.join(gast_dir, "gast"+dna_region)
            
            logger.debug('gast filesize:'+str(os.path.getsize(clustergast_filename_single)))
            
            gast_filename          = os.path.join(gast_dir, "gast")
            gastconcat_filename    = os.path.join(gast_dir, "gast_concat")  
            #dupes_filename    = os.path.join(gast_dir, "dupes") 
            #nonhits_filename    = os.path.join(gast_dir, "nonhits")   
            copies = {}
            nonhits = {}
            # open and read names file
            names_fh = open(names_file,'r')
            for line in names_fh:
                s = line.strip().split("\t")
                
                index_read = s[0]                
                copies[index_read] = s[1].split(',')
                
                if index_read in nonhits:
                    nonhits[index_read] += 1
                else:
                    nonhits[index_read] = 1
                    
                
                
            names_fh.close()            
            #print nonhits
            #print copies
            
            #######################################
            # 
            #  Insert records with valid gast hits into gast_file
            # 
            #######################################   
            # read the .gast file from clustergast            
            concat = {}
            gast_fh     = open(gast_filename,'w')
            if(os.path.exists(clustergast_filename_single)):
                in_gast_fh  = open(clustergast_filename_single,'r')
            else:
                print "No clustergast file found:",clustergast_filename_single,"\nExiting"
                self.run.run_status_file_h.write("No clustergast file found:",clustergast_filename_single," Exiting\n")
                sys.exit()
            for line in in_gast_fh:
                
                s = line.strip().split()
                if len(s) == 4:
                    read_id     = s[0]
                    refhvr_id   = s[1].split('|')[0]
                    distance    = s[2]
                    alignment   = s[3]
                #print read_id,refhvr_id
                # if this was in the gast table zero it out because it had a valid hit
                # so we don't insert them as non-hits later
                if read_id in nonhits:
                    del nonhits[read_id]
                    #print 'deleling',read_id
                #print 'nonhits',nonhits
                if read_id not in copies:
                    logger.info(read_id+' not in names file: Skipping')
                    continue
                    
                # give the same ref and dist for each duplicate
                for id in copies[read_id]:
                    
                    if id != read_id:
                        #print id,read_id,distance,refhvr_id  
                        gast_fh.write( id + "\t" + refhvr_id + "\t" + distance + "\t" + alignment + "\n" )
                        
                                               
            in_gast_fh.close()
             
            #######################################
            # 
            #  Insert a record for any valid sequence that had no blast hit and therefore no gast result
            #       into gast_filename
            # 
            #######################################   
            for read in sorted(nonhits.iterkeys()):                
                for d in copies[read]: 
                    gast_fh.write( d+"\t0\t1\t\n")
                    
                    
            gast_fh.close()
            
            # concatenate the two gast files
            clustergast_fh = open(clustergast_filename_single,'a')            
            shutil.copyfileobj(open(gast_filename,'rb'), clustergast_fh)
            clustergast_fh.close()
            #the open again and get data for gast concat
            concat = {}
            print clustergast_filename_single
            for line in open(clustergast_filename_single,'r'):
                data = line.strip().split("\t")
                id = data[0]
                refhvr_id = data[1].split('|')[0]
                distance = data[2]
                #print 'data',data
                if id in concat:
                    concat[id]['refhvrs'].append(refhvr_id)                        
                else:
                    concat[id] = {}
                    concat[id]['refhvrs'] = [refhvr_id]
                concat[id]['distance'] = distance     
                
            
            
            #######################################
            #
            # Insert records into gast_concat_filename
            #
            #######################################             
            # first we need to open the gast_filename
            gastconcat_fh     = open(gastconcat_filename,'w')
            for id, value in concat.iteritems():
                #print 'trying gastconcat', id,value
                gastconcat_fh.write( id + "\t" + concat[id]['distance'] + "\t" + ' '.join(concat[id]['refhvrs']) + "\n" )
            gastconcat_fh.close()
            
            
        print "Finished gast_cleanup"   
        logger.info("Finished gast_cleanup")
        return ("SUCCESS","gast_cleanup")

    def gast2tax(self, idx_keys): 
        
        for key in keys:
            output_dir = os.path.join(self.basedir,key)
            gast_dir = os.path.join(output_dir,'gast')
            if key in self.run.samples:
                dna_region = self.run.samples[key].dna_region
            else:            
                dna_region = self.run.dna_region
            if not dna_region:
                logger.error("gast2tax: We have no DNA Region: Setting dna_region to 'unknown'")
                self.run.run_status_file_h.write("gast2tax: We have no DNA Region: Setting dna_region to 'unknown'")
                dna_region = 'unknown'
            
            (refdb,taxdb) = self.get_reference_databases(dna_region)
            
            
            #print tax_file
            max_distance = C.max_distance['default']
            if dna_region in C.max_distance:
                max_distance = C.max_distance[dna_region]    
            unique_file = os.path.join(output_dir, key+'.unique.fa')
            names_file  = os.path.join(output_dir, key+'.names')
            #usearch_filename= os.path.join(self.gast_dir, "uc")
            #uc_results = self.parse_uclust(usearch_filename)
            #print uc_results
            
            ref_taxa = self.load_reftaxa(taxdb)
            names_file  = os.path.join(output_dir, key+'.names')
            self.assign_taxonomy(gast_dir,dna_region,names_file, ref_taxa);
            
        return ("SUCCESS","gast2tax") 
        
    
    def get_reference_databases(self,dna_region):
        
        #if dna region == v6v4(a) change it to v4v6
        # other reverse regions? 
        if dna_region == 'v6v4':
            dna_region = 'v4v6'
        if dna_region == 'v6v4a':
            dna_region = 'v4v6a'
        if C.use_full_length:
            if os.path.exists(os.path.join(self.refdb_dir, 'refssu.udb')):
                refdb = os.path.join(self.refdb_dir, 'refssu.udb')
                taxdb = os.path.join(self.refdb_dir, 'refssu.tax')
            elif os.path.exists(os.path.join(self.refdb_dir, 'refssu.fa')):
                refdb = os.path.join(self.refdb_dir, 'refssu.fa')
                taxdb = os.path.join(self.refdb_dir, 'refssu.tax')
        else:
            if os.path.exists(os.path.join(self.refdb_dir, C.refdbs[dna_region])):
                refdb = os.path.join(self.refdb_dir, C.refdbs[dna_region])
                taxdb = os.path.join(self.refdb_dir, 'ref'+dna_region+'.tax')
            elif os.path.exists(os.path.join(self.refdb_dir, 'ref'+dna_region+'.fa')):
                refdb = os.path.join(self.refdb_dir, 'ref'+dna_region+'.fa')
                taxdb = os.path.join(self.refdb_dir, 'ref'+dna_region+'.tax')
            elif os.path.exists(os.path.join(self.refdb_dir, 'refssu.udb')):
                refdb = os.path.join(self.refdb_dir, 'refssu.udb')
                taxdb = os.path.join(self.refdb_dir, 'refssu.tax')
            elif os.path.exists(os.path.join(self.refdb_dir, 'refssu.fa')):
                refdb = os.path.join(self.refdb_dir, 'refssu.fa')
                taxdb = os.path.join(self.refdb_dir, 'refssu.tax')
            else:
                logger.error("Could not find reference database "+refdb+" Exiting")
                sys.exit()  
        
        logger.info('tax_file '+taxdb)
        logger.info('ref_file '+refdb)        
        return (refdb,taxdb)   
          
    def get_fastasampler_cmd(self,unique_file, fastasamp_filename,start,end):
        fastasampler = C.fastasampler_cmd
        fastasampler_cmd = fastasampler
        fastasampler_cmd += ' -n '+ str(start)+','+ str(end)
        fastasampler_cmd += ' ' + unique_file
        fastasampler_cmd += ' ' + fastasamp_filename        
        return fastasampler_cmd
        
    def get_usearch_cmd(self,fastasamp_filename, refdb,usearch_filename  ):    
        
        if C.use_full_length:            
            usearch = C.usearch64
        else:
            usearch = C.usearch_cmd
            
        usearch_cmd = usearch
        usearch_cmd += ' -usearch_global ' + fastasamp_filename
        #usearch_cmd += ' --iddef 3'
        usearch_cmd += ' -gapopen 6I/1E'
        usearch_cmd += ' -db ' + refdb  
        usearch_cmd += ' -strand both'              
        usearch_cmd += ' -uc ' + usearch_filename 
        usearch_cmd += ' -maxaccepts ' + str(C.max_accepts)
        usearch_cmd += ' -maxrejects ' + str(C.max_rejects)
        usearch_cmd += ' -id ' + str(C.pctid_threshold)
        return usearch_cmd
        
    def get_grep_cmd(self,usearch_filename,  clustergast_filename ):
        
        use_full_length = ''
        if C.use_full_length: 
            use_full_length = "-use_full_length"
            
        grep_cmd = "grep"
        grep_cmd += " -P \"^H\\t\" " + usearch_filename + " |"
        grep_cmd += " sed -e 's/|.*\$//' |"
        grep_cmd += " awk '{print $9 \"\\t\" $4 \"\\t\" $10 \"\\t\" $8}' |"
        grep_cmd += " sort -k1,1b -k2,2gr |"
        # append to file:
        grep_cmd += " clustergast_tophit "+use_full_length+" >> " + clustergast_filename
        print grep_cmd
        return grep_cmd  
          
    def load_reftaxa(self,tax_file):
    
        
        taxa ={}
        #open(TAX, "<$tax_file") || die ("Unable to open reference taxonomy file: $tax_file.  Exiting\n");
        #while (my $line = <TAX>) 
        n=1
        for line in  open(tax_file,'r'):
        
            # 0=ref_id, 1 = taxa, 2 = count
            data=line.strip().split("\t")
    
            copies = []
    
            # foreach instance of that taxa
            for i in range(0,int(data[2])):
            
                # add that taxonomy to an array
                copies.append(data[1])
            
            # add that array to the array of all taxa for that ref, stored in the taxa hash
            if data[0] in taxa:
                taxa[data[0]].append(copies)
            elif copies:         
                taxa[data[0]] =[copies]
            else:
                taxa[data[0]] =[]
            n += 1
        return taxa
    
    def assign_taxonomy(self, gast_dir, dna_region, names_file,  ref_taxa):
        from pipeline.taxonomy import Taxonomy,consensus
        #results = uc_results
        results = {}
        
        # open gast_file to get results
        tagtax_filename     = os.path.join(gast_dir,"tagtax")
        tagtax_fh = open(tagtax_filename,'w')
       
        gast_file          = os.path.join(gast_dir, "gast"+dna_region)
        if not os.path.exists(gast_file):
            logger.info("Could not find gast file: "+gast_file)
            sys.exit("Could not find gast file: "+gast_file)
        for line in  open(gast_file,'r'): 
            # must split on tab because last field may be empty and must be maintained as blank
            data=line.strip().split("\t")
            if len(data) == 3:
                data.append("")
            # 0=id, 1=ref, 2=dist, 3=align
            results[data[0]]=[data[1].split('|')[0],data[2],data[3]]
            
        for read in results:
            #print read, results[read]
            pass
        
        for line in  open(names_file,'r'):
            data=line.strip().split("\t")
            dupes = data[1].split(",")
            read  = data[0]
            taxObjects  = []
            distance    =0
            refs_for    ={}
            #print 'read',read
            if read not in results:
                results[read]=["Unknown", '1', "NA", '0', '0', "NA", "0;0;0;0;0;0;0;0", "0;0;0;0;0;0;0;0", "100;100;100;100;100;100;100;100"]
                refs_for[read] = [ "NA" ]
            else:
                #print 'read in res',read, results[read]
                for i in range( 0,len(results[read])):
                #for resultread in results[read]:
                    #print results[read]
                    ref = results[read][0]
                    if ref in ref_taxa:
                        for tax in ref_taxa[ref]:
                            for t in tax:
                                taxObjects.append(Taxonomy(t))
                    else:
                        pass
                    if read in refs_for:
                        if results[read][0] not in refs_for[read]:
                            refs_for[read].append(results[read][0])  
                    else:
                        refs_for[read] = [results[read][0]]                   
                     
                    # should all be the same distance
                    distance = results[read][1]
                #Lookup the consensus taxonomy for the array
                taxReturn = consensus(taxObjects, C.majority)
                
                # 0=taxObj, 1=winning vote, 2=minrank, 3=rankCounts, 4=maxPcts, 5=naPcts;
                taxon = taxReturn[0].taxstring()
                rank = taxReturn[0].depth()
                #print read,taxon,rank,taxReturn[0],taxReturn[1]
                if not taxon: taxon = "Unknown"
            
                # (taxonomy, distance, rank, refssu_count, vote, minrank, taxa_counts, max_pcts, na_pcts)
                results[read] = [ taxon, str(distance), rank, str(len(taxObjects)), str(taxReturn[1]), taxReturn[2], taxReturn[3], taxReturn[4], taxReturn[5] ] 
                #print "\t".join([read,taxon, str(distance), rank, str(len(taxObjects)), str(taxReturn[1]), taxReturn[2], taxReturn[3], taxReturn[4], taxReturn[5]]) + "\n"
                
            # Replace hash with final taxonomy results, for each copy of the sequence
            for d in dupes:
                
                tagtax_fh.write(d+"\t"+results[read][0]+"\t"+results[read][2]+"\t"+results[read][3]+"\t"+','.join(sorted(refs_for[read]))+"\t"+results[read][1]+"\n")
               
        tagtax_fh.close()
        return results

    def create_uniques_from_fasta(self,fasta_file,key):
        
        mothur_cmd = C.mothur_cmd+" \"#unique.seqs(fasta="+fasta_file+", outputdir="+os.path.join(self.basedir,key)+"/);\""; 
        
        #mothur_cmd = site_base+"/clusterize_vamps -site vampsdev -rd "+user+"_"+runcode+"_gast -rc "+runcode+" -u "+user+" /bioware/mothur/mothur \"#unique.seqs(fasta="+fasta_file+");\"";    
        subprocess.call(mothur_cmd, shell=True)
    def check_for_uniques_files(self,keys):
        if self.run.platform == 'vamps':
            # one fasta file or (one project and dataset from db)
            if self.run.fasta_file != '':
                pass
            else:
                if self.run.project and self.run.dataset:
                    pass
                else:
                    pass
                #get from database
        else:
            pass
        for key in keys:
            fasta_file = ""
            output_dir = os.path.join(self.basedir,key)
            unique_file = os.path.join(output_dir, key+'.unique.fa')
            if not os.path.exists(unique_file):
                mothur_cmd = C.mothur_cmd+" \"#unique.seqs(fasta="+fasta_file+", outputdir="+os.path.join(self.basedir,key)+"/);\""; 
        
                #mothur_cmd = site_base+"/clusterize_vamps -site vampsdev -rd "+user+"_"+runcode+"_gast -rc "+runcode+" -u "+user+" /bioware/mothur/mothur \"#unique.seqs(fasta="+fasta_file+");\"";    
                subprocess.call(mothur_cmd, shell=True)
        return ("SUCCESS","check for uniques")        
                
    def get_fasta_from_database(self):
        pass