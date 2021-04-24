import os
import time

def write_sbatch_conf(f, exp_name = "default", grace_partition = "day", dir_name = "./", SF_PATH = "stockfish_13_linux_x64/stockfish_13_linux_x64"):
    f.write('#!/bin/bash\n')
    f.write('#SBATCH --job-name=' + exp_name + '\n')
    f.write('#SBATCH --ntasks=1 --nodes=1\n')
    f.write('#SBATCH --partition=' + grace_partition + '\n')
    f.write('#SBATCH --mem=8G\n')
    f.write('#SBATCH --cpus-per-task=8\n')
    f.write('#SBATCH --time=24:00:00\n')
    f.write('#SBATCH --output=./create_dataset_logs/'  + exp_name + '_log\n')
    f.write('module load miniconda\n')
    f.write('conda activate py37_dev\n')

def generate_cmd(white_start, white_end, black_start, black_end, reps = 1):
    cmd = "python src/create_dataset.py "
    cmd = cmd + str(white_start) + " "
    cmd = cmd + str(white_end) + " "
    cmd = cmd + str(black_start) + " "
    cmd = cmd + str(black_end) + " "
    cmd = cmd + str(reps)
    return cmd

def generate_script(file_name, white_start = 0, white_end = 1, black_start = 0, black_end = 1, reps = 1, grace_partition = "day", exp_name = "default"):
    f = open(file_name, 'w', buffering = 1)
    write_sbatch_conf(f, exp_name = exp_name, grace_partition = grace_partition)
    s = generate_cmd(white_start, white_end, black_start, black_end, reps = reps)
    f.write(s)
    f.close()

def main():
    grace_partition = "day"
    exp_name = "create_dataset"
    reps = 5
    for _ in range(1):
        for i in range(0, 1):
            file_name = "rog_scipt" + str(time.time()) + ".sh"
            exp_name = "create_dataset_" + str(i) + "_" + str(i+1) + "_" + str(0) + "_" + str(141) + "_" + str(reps) + "_" + str(time.time())
            generate_script(file_name, white_start = i, white_end = i + 1, black_start = 0, black_end = 141, reps = reps, grace_partition = grace_partition, exp_name = exp_name)
            os.system("sbatch " + file_name)

if __name__ == "__main__":
    main()