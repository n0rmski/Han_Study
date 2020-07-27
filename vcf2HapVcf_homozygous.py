#!/usr/bin/env python
"""
Converts a diploid vcf to a haploid vcf where each sample of the vcf is a diploid homozygous for the alleles of the haplotype. 
Note: Variants throughout vcf must be phased.
Note: Genotype field of vcf should not have any information beyond the phased alleles (e.g., 0|1 will work but 0|1:0.55, 0.45:... won't work)
"""

__author__ = 'jashortt'

import argparse
import sys
	
def duplicateNames(info):
	header_info=info[0:9]
	names=info[9:]
	dupnames=["_".join((name, str(hap))) for name in names for hap in range(2)]
	return ( header_info + dupnames )
	
def printVcfHeader (infp, outfp):
	line = infp.readline()
	while line.startswith('##'):
		outfp.write(line)
		line = infp.readline()
	if line.startswith('#'):
		line = line.strip().split()
		new_header = duplicateNames(line)
		outfp.write( '%s\n' % ('\t'.join(new_header)) )
	
def getAllelesOnlyAndDuplicate (genos):
	alleles = []
	for geno in genos:
		for allele in geno.split('|'): # may also want to put in a check that '|' is there and not something else
			alleles.append(allele + '|' + allele)			
	return alleles						
		
def getLocInfo(info):
	chr, pos, id, ref, alt, qual, filter, var_info, format = info
	return {'chr':chr, 'id':id, 'pos':pos, 'ref':ref, 'alt':alt, 'qual':qual, 'filter':filter, 'info':info, 'format':format}			

def printVcfVarLines(infp, outfp):
	for line in infp:
		info = line.strip().split()
		alleles = getAllelesOnlyAndDuplicate(info[9:])	
		outfp.write('%s\n' % ('\t'.join( info[0:9] + alleles) ) )					

def main(args):
	infile = args.vcf
	outfile = args.out + '.hapvcf'
	with open(infile, 'r') as infp, open(outfile, 'w') as outfp:
		printVcfHeader(infp, outfp)
		printVcfVarLines(infp, outfp)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(prog='vcf2Ped')
	    
	parser.add_argument('--vcf', help='vcf file to be converted', nargs='?', const=1, type=str, default='plink.vcf', required=False)
	parser.add_argument('--out', help='prefix for output', nargs='?', type=str, const=1, required=False)
	parser.add_argument('--version', action='version', version='%(prog)s 0.1')
		
	args = parser.parse_args()
	ns = parser.parse_args()
	args.out = args.out if args.out else args.vcf.replace('.vcf', '')
	main(args)
	sys.exit()