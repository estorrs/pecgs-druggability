import argparse
import os
import logging
import subprocess
from pathlib import Path

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

parser = argparse.ArgumentParser()

parser.add_argument('tumor_sample_name', type=str,
    help='sample or tumor sample name')

parser.add_argument('variant_filepath', type=str,
    help='variant filename')

parser.add_argument('variant_file_type', type=str, choices=['maf', 'fusion', 'basicmaf'],
    help='variation type: maf | fusion | basicmaf')

parser.add_argument('--output-dir', type=str, default='output',
    help='alteration database matches')

parser.add_argument('--d', action="store_true",
    help='debug mode')

parser.add_argument('--normal-sample-name', type=str,
    help='normal sample name')

parser.add_argument('--annotate-trials-keyword', type=str, choices=['CHOL', 'MM', 'CRC', 'NONE'],
    help='report clinical trials for this disease keyword')

parser.add_argument('--druggability-dir', type=str,
    help='working directory for script to be run in. this should be the root of the druggability repo')


args = parser.parse_args()


def druggability_cli(script_fp, t, f, nn, tn, l, o, at, ato):
    pieces = [
        f'python {script_fp}',
        '-t', t,
        '-f', f,
        '-nn', nn,
        '-tn', tn,
        '-l', l,
        '-o', o,
    ]
    if at is not None and at != 'NONE':
        pieces += [
            '-at', at,
            '-ato', ato,
        ]
    return ' '.join(pieces)


def run_druggability(args):
    out_dir = os.path.abspath(args.output_dir)
    logging.info(f'creating output directory at {out_dir}')
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    output_fp = os.path.join(out_dir, 'output.txt')
    at_output_fp = os.path.join(out_dir, 'aux_trials_output.txt')
    log_fp = os.path.join(out_dir, 'log.txt')

    logging.info(f'setting working directory as {args.druggability_dir}')
    script_fp = os.path.join(args.druggability_dir, 'druggability.py')
    os.chdir(args.druggability_dir)

    cmd = druggability_cli(
        script_fp, args.variant_file_type, args.variant_filepath,
        args.normal_sample_name, args.tumor_sample_name, log_fp,
        output_fp, args.annotate_trials_keyword, at_output_fp)
    logging.info(f'executing command: {cmd}')
    subprocess.check_output(cmd, shell=True)
    logging.info('druggability completed')
    
    logging.info(f'output written to {output_fp}')
    if args.annotate_trials_keyword is not None:
        logging.info(f'aux output written to {at_output_fp}')
    logging.info(f'logs written to {log_fp}')


def main():
    run_druggability(args)


if __name__ == '__main__':
    main()
