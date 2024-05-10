import argparse
import copy
import json
import os
import sys

CAR = {
	'name': None,
	'brand': 'ACE',
	'description': None,
	'tags': ['ace', 'experimental', 'street'],
	'class': 'street',
	'torqueCurve': [
		[0,50],
		[500,62],
		[1000,78],
		[1500,101],
		[2000,113],
		[2500,128],
		[3000,134],
		[3500,139],
		[4000,143],
		[4500,147],
		[5000,149],
		[5500,152],
		[6000,149],
		[6500,141],
		[7000,125],
		[7500,112]
	],
	'powerCurve': [
		[0,0],
		[500,4],
		[1000,11],
		[1500,21],
		[2000,32],
		[2500,45],
		[3000,56],
		[3500,68],
		[4000,80],
		[4500,93],
		[5000,105],
		[5500,115],
		[6000,126],
		[6500,130],
		[7000,123],
		[7500,118]
	]
}

def modify_curve(curve, mod):
	for i in range(len(curve)):
		rpm, val = curve[i]
		curve[i][1] = int(val * mod)

def mod_power(file, mod):
	lines = []
	with open(file) as fp:
		for line in fp.readlines():
			f = line.split('|')
			if len(f) == 2:
				rpm = int(f[0])
				tq = int(f[1])
				tq = int(mod*tq/100)
				lines.append(f'{rpm}|{tq}\n')
	with open(file, 'w') as fp:
		for line in lines:
			fp.write(line)

def write_ui(file, name, desc, power):
	car = copy.deepcopy(CAR)
	car['name'] = name
	car['description'] = desc
	modify_curve(car['torqueCurve'], power/100)
	modify_curve(car['powerCurve'], power/100)
	with open(file, 'w') as fp:
		fp.write(json.dumps(car, indent=4))

def quick_edit(file, find, replace):
	lines = []
	with open(file) as fp:
		for line in fp.readlines():
			if line.startswith(find): line = f'{replace}\n'
			lines.append(line)
	with open(file, 'w') as fp:
		for line in lines:
			fp.write(line)

def quick_edit(file, find, replace):
	lines = []
	with open(file) as fp:
		for line in fp.readlines():
			if line.startswith(find): line = f'{replace}\n'
			lines.append(line)
	with open(file, 'w') as fp:
		for line in lines:
			fp.write(line)

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='aces.py')
	parser.add_argument('root', type=str, metavar='<path>',
		help='assetto corsa root directory')
	parser.add_argument('source', type=str, metavar='<name>',
		help='name of source vehicle directory')
	parser.add_argument('target', type=str, metavar='<name>',
		help='name of target vehicle directory')
	arg = parser.parse_args()

	p = 140

	# RWD - just power mod
	name = f'ace_rwd'
	os.system(f'cp -r "{arg.root}"/content/cars/{arg.source} {name}') # copy directory
	os.system(f'rm {name}/data.acd') # force to re-pack data
	desc = f'RWD Miata w/ extra power'
	write_ui(f'{name}/ui/ui_car.json', name, desc, p); # write ui_car.json
	mod_power(f'{name}/data/power.lut', p) # power

	# FWD - minimal modifications
	name = f'ace_fwd'
	os.system(f'cp -r "{arg.root}"/content/cars/{arg.source} {name}') # copy directory
	os.system(f'rm {name}/data.acd') # force to re-pack data
	desc = f'FWD Miata w/ extra power'
	write_ui(f'{name}/ui/ui_car.json', name, desc, p); # write ui_car.json
	quick_edit(f'{name}/data/drivetrain.ini', 'TYPE=RWD', 'TYPE=FWD') # RWD -> FWD
	quick_edit(f'{name}/data/suspensions.ini', 'CG_LOCATION=0.515', f'CG_LOCATION=0.62') # CoG
	quick_edit(f'{name}/data/brakes.ini', 'FRONT_SHARE=0.67', f'FRONT_SHARE=0.74') # brake bias
	mod_power(f'{name}/data/power.lut', p) # power

	# AWD - minimal modifications
	name = f'ace_awd'
	os.system(f'cp -r "{arg.root}"/content/cars/{arg.source} {name}') # copy directory
	os.system(f'rm {name}/data.acd') # force to re-pack data
	desc = f'AWD Miata w/ extra power'
	write_ui(f'{name}/ui/ui_car.json', name, desc, p); # write ui_car.json
	quick_edit(f'{name}/data/drivetrain.ini', 'TYPE=RWD', 'TYPE=AWD') # RWD -> AWD
	quick_edit(f'{name}/data/suspensions.ini', 'CG_LOCATION=0.515', f'CG_LOCATION=0.60') # CoG
	quick_edit(f'{name}/data/brakes.ini', 'FRONT_SHARE=0.67', f'FRONT_SHARE=0.74') # brake bias
	mod_power(f'{name}/data/power.lut', p) # power

	awd = [
		'[AWD'], # from Audi S1
		'FRONT_SHARE=98',
		'FRONT_DIFF_POWER=0.06',
		'FRONT_DIFF_COAST=0.02',
		'FRONT_DIFF_PRELOAD=0',
		'CENTRE_DIFF_POWER=0.03',
		'CENTRE_DIFF_COAST=0.03',
		'CENTRE_DIFF_PRELOAD=1',
		'REAR_DIFF_POWER=0.03',
		'REAR_DIFF_COAST=0.03',
		'REAR_DIFF_PRELOAD=0',
	]
	contents = []
	with open(f'{name}/data/drivetrain.ini') as fp:
		for line in fp: contents.append(line)

	with open(f'{name}/data/drivetrain.ini', 'w') as fp:
		for line in contents: fp.write(line)
		for line in awd: fp.write(line)
