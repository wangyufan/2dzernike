root_dir=/home/dongxq/Desktop/mol2-file
doc_dir=/home/dongxq/Documents/2d_proj
for(( i=1; i<=10; i++ ))
do
	chmod 777 generate_stream_job.sh
	./generate_stream_job.sh $i $root_dir $doc_dir
done
filename=_stream_job.pbs
for(( i=1; i<=10; i++ ))
do
	echo $i
	qsub $i$filename
done