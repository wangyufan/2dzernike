cat > $1_stream_job.pbs << END_TEXT
#!/bin/bash
### job Name
#PBS -N $1_0306_yf
### Output Files
#PBS -o $1_0306.out
#PBS -e $1_0306.err
### Queue Name
#PBS -q low
### Number of nodes
#PBS -l nodes=1:ppn=24
cd $2/align_code
sastbx.python nprocess_peak_find_stream.py -input $3/asdf_0125.stream -template $3/100_braycurtis_templates.h5 -mask $3/signal_235_braycurtis_mask.npy -node 10 -node_n $1 -processnum 24