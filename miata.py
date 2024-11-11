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

def section_edit(file, sect, find, replace):
	lines = []
	section = None
	with open(file) as fp:
		for line in fp.readlines():
			if line.startswith('['): section = line.rstrip()
			elif sect == section and line.startswith(find): line = f'{replace}\n'
			lines.append(line)
	with open(file, 'w') as fp:
		for line in lines:
			fp.write(line)


parser = argparse.ArgumentParser(description='miata.py')
parser.add_argument('root', type=str, metavar='<path>',
	help='assetto corsa root directory')
parser.add_argument('source', type=str, metavar='<name>',
	help='name of source vehicle directory')
parser.add_argument('target', type=str, metavar='<name>',
	help='name of target vehicle directory')
arg = parser.parse_args()

# main control
fcog = [0.65]  # FWD only, fabricated values
fbias = [0.75] # FWD only, fabricated values
rcog = [0.515] # RWD only, default 0.515
rbias = [0.67] # RWD only, default 0.67
power = [100]
fgs = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110]
rgs = [110, 109, 108, 107, 106, 105, 104, 103, 102, 101, 100]

# main loop
for fg, rg in zip(fgs, rgs):
		
	# FWD
	for p in power:
		for c, b in zip(fcog, fbias):
			name = f'{arg.target}-FWD-F{fg}-R{rg}-C{c}-P{p}'
			print(name, file=sys.stderr)
			os.system(f'cp -r "{arg.root}"/content/cars/{arg.source} {name}') # copy directory
			os.system(f'rm {name}/data.acd') # force to re-pack data
			desc = f'ACE FWD Miata with Grip {fg}/{rg}, CoG {c}, and Power {p}%'
			write_ui(f'{name}/ui/ui_car.json', name, desc, p); # write ui_car.json
			quick_edit(f'{name}/data/drivetrain.ini', 'TYPE=RWD', 'TYPE=FWD') # RWD -> FWD
			quick_edit(f'{name}/data/suspensions.ini', 'CG_LOCATION=0.515', f'CG_LOCATION={c}') # CoG
			quick_edit(f'{name}/data/brakes.ini', 'FRONT_SHARE=0.67', f'FRONT_SHARE={b}') # brake bias
			quick_edit(f'{name}/data/suspensions.ini', 'FRONT=9502', 'FRONT=4260') # ARB swap
			quick_edit(f'{name}/data/suspensions.ini', 'REAR=4259', 'REAR=9500') # ARB swap
			quick_edit(f'{name}/data/suspensions.ini', 'TRACK=1.410', 'TRACK=1.43') # track width swap
			quick_edit(f'{name}/data/suspensions.ini', 'TRACK=1.427', 'TRACK=1.41') # track width swap
			section_edit(f'{name}/data/tyres.ini', '[FRONT]', 'DX_REF=1.22', f'DX_REF={1.22 * rg / 100}') # front grip
			section_edit(f'{name}/data/tyres.ini', '[FRONT]', 'DY_REF=1.21', f'DY_REF={1.21 * rg / 100}') # front grip
			section_edit(f'{name}/data/tyres.ini', '[REAR]', 'DX_REF=1.22', f'DX_REF={1.22 * rg / 100}') # rear grip
			section_edit(f'{name}/data/tyres.ini', '[REAR]', 'DY_REF=1.21', f'DY_REF={1.21 * rg / 100}') # rear grip
			mod_power(f'{name}/data/power.lut', p) # power
	
	# RWD
	for p in power:
		for c, b in zip(rcog, rbias):
			name = f'{arg.target}-RWD-F{fg}-R{rg}-C{c}-P{p}'
			print(name, file=sys.stderr)
			os.system(f'cp -r "{arg.root}"/content/cars/{arg.source} {name}') # copy directory
			os.system(f'rm {name}/data.acd') # force to re-pack data
			desc = f'ACE RWD Miata with Grip {fg}/{rg}, CoG {c}, and Power {p}%'
			write_ui(f'{name}/ui/ui_car.json', name, desc, p); # write ui_car.json
			section_edit(f'{name}/data/tyres.ini', '[FRONT]', 'DX_REF=1.22', f'DX_REF={1.22 * rg / 100}') # front grip
			section_edit(f'{name}/data/tyres.ini', '[FRONT]', 'DY_REF=1.21', f'DY_REF={1.21 * rg / 100}') # front grip
			section_edit(f'{name}/data/tyres.ini', '[REAR]', 'DX_REF=1.22', f'DX_REF={1.22 * rg / 100}') # rear grip
			section_edit(f'{name}/data/tyres.ini', '[REAR]', 'DY_REF=1.21', f'DY_REF={1.21 * rg / 100}') # rear grip
			mod_power(f'{name}/data/power.lut', p) # power



"""

for gb in range(1, 10):
	for f, r in fr:
		fg = 100 + gb*f
		rg = 100 + gb*r
		
		# FWD
		for p in power:
			for c, b in zip(cog, bias):
				name = f'{arg.target}-C{c}-P{p}-G{g}'
				os.system(f'cp -r "{arg.root}"/content/cars/{arg.source} {name}') # copy directory
				os.system(f'rm {name}/data.acd') # force to re-pack data
				desc = f'Experimental FWD Miata with CoG {c}%, Power {p}%, and Grip {g}%'
				write_ui(f'{name}/ui/ui_car.json', name, desc, p, g); # write ui_car.json
				quick_edit(f'{name}/data/drivetrain.ini', 'TYPE=RWD', 'TYPE=FWD') # RWD -> FWD
				quick_edit(f'{name}/data/suspensions.ini', 'CG_LOCATION=0.515', f'CG_LOCATION={c/100}') # CoG
				quick_edit(f'{name}/data/brakes.ini', 'FRONT_SHARE=0.67', f'FRONT_SHARE={b/100}') # brake bias
				quick_edit(f'{name}/data/suspensions.ini', 'FRONT=9502', 'FRONT=4260') # ARB swap
				quick_edit(f'{name}/data/suspensions.ini', 'REAR=4259', 'REAR=9500') # ARB swap
				quick_edit(f'{name}/data/suspensions.ini', 'TRACK=1.410', 'TRACK=1.43') # track width swap
				quick_edit(f'{name}/data/suspensions.ini', 'TRACK=1.427', 'TRACK=1.41') # track width swap
				quick_edit(f'{name}/data/tyres.ini', 'DX_REF=1.22', f'DX_REF={1.22 * g / 100}') # grip
				quick_edit(f'{name}/data/tyres.ini', 'DY_REF=1.21', f'DY_REF={1.21 * g / 100}') # grip
				mod_power(f'{name}/data/power.lut', p) # power
				
				
	# variables for CoG experiments
	cog  =  [55, 60, 65]
	bias =  [70, 74, 78]
	power = [100]
	grip =  [100]

	# FWD Miatas
	for p in power:
		for g in grip:
			for c, b in zip(cog, bias):
				name = f'{arg.target}-C{c}-P{p}-G{g}'
				os.system(f'cp -r "{arg.root}"/content/cars/{arg.source} {name}') # copy directory
				os.system(f'rm {name}/data.acd') # force to re-pack data
				desc = f'Experimental FWD Miata with CoG {c}%, Power {p}%, and Grip {g}%'
				write_ui(f'{name}/ui/ui_car.json', name, desc, p, g); # write ui_car.json
				quick_edit(f'{name}/data/drivetrain.ini', 'TYPE=RWD', 'TYPE=FWD') # RWD -> FWD
				quick_edit(f'{name}/data/suspensions.ini', 'CG_LOCATION=0.515', f'CG_LOCATION={c/100}') # CoG
				quick_edit(f'{name}/data/brakes.ini', 'FRONT_SHARE=0.67', f'FRONT_SHARE={b/100}') # brake bias
				quick_edit(f'{name}/data/suspensions.ini', 'FRONT=9502', 'FRONT=4260') # ARB swap
				quick_edit(f'{name}/data/suspensions.ini', 'REAR=4259', 'REAR=9500') # ARB swap
				quick_edit(f'{name}/data/suspensions.ini', 'TRACK=1.410', 'TRACK=1.43') # track width swap
				quick_edit(f'{name}/data/suspensions.ini', 'TRACK=1.427', 'TRACK=1.41') # track width swap
				quick_edit(f'{name}/data/tyres.ini', 'DX_REF=1.22', f'DX_REF={1.22 * g / 100}') # grip
				quick_edit(f'{name}/data/tyres.ini', 'DY_REF=1.21', f'DY_REF={1.21 * g / 100}') # grip
				mod_power(f'{name}/data/power.lut', p) # power


	# variables for power and grip experiments
	cog  =  [60]
	bias =  [74]
	power = [100, 150, 200]
	grip =  [50, 67, 100]

	# FWD Miatas
	for p in power:
		for g in grip:
			for c, b in zip(cog, bias):
				name = f'{arg.target}-C{c}-P{p}-G{g}'
				os.system(f'cp -r "{arg.root}"/content/cars/{arg.source} {name}') # copy directory
				os.system(f'rm {name}/data.acd') # force to re-pack data
				desc = f'Experimental FWD Miata with CoG {c}%, Power {p}%, and Grip {g}%'
				write_ui(f'{name}/ui/ui_car.json', name, desc, p, g); # write ui_car.json
				quick_edit(f'{name}/data/drivetrain.ini', 'TYPE=RWD', 'TYPE=FWD') # RWD -> FWD
				quick_edit(f'{name}/data/suspensions.ini', 'CG_LOCATION=0.515', f'CG_LOCATION={c/100}') # CoG
				quick_edit(f'{name}/data/brakes.ini', 'FRONT_SHARE=0.67', f'FRONT_SHARE={b/100}') # brake bias
				quick_edit(f'{name}/data/suspensions.ini', 'FRONT=9502', 'FRONT=4260') # ARB swap
				quick_edit(f'{name}/data/suspensions.ini', 'REAR=4259', 'REAR=9500') # ARB swap
				quick_edit(f'{name}/data/suspensions.ini', 'TRACK=1.410', 'TRACK=1.43') # track width swap
				quick_edit(f'{name}/data/suspensions.ini', 'TRACK=1.427', 'TRACK=1.41') # track width swap
				quick_edit(f'{name}/data/tyres.ini', 'DX_REF=1.22', f'DX_REF={1.22 * g / 100}') # grip
				quick_edit(f'{name}/data/tyres.ini', 'DY_REF=1.21', f'DY_REF={1.21 * g / 100}') # grip
				mod_power(f'{name}/data/power.lut', p) # power

	# RWD Miatas
	for p in power:
		for g in grip:
			name = f'{arg.target}-RWD-P{p}-G{g}'
			os.system(f'cp -r "{arg.root}"/content/cars/{arg.source} {name}') # copy directory
			os.system(f'rm {name}/data.acd') # force to re-pack data
			desc = f'Experimental RWD Miata with Power {p}%, and Grip {g}%'
			write_ui(f'{name}/ui/ui_car.json', name, desc, p, g); # write ui_car.json
			quick_edit(f'{name}/data/tyres.ini', 'DX_REF=1.22', f'DX_REF={1.22 * g / 100}') # grip
			quick_edit(f'{name}/data/tyres.ini', 'DY_REF=1.21', f'DY_REF={1.21 * g / 100}') # grip
			mod_power(f'{name}/data/power.lut', p) # power
"""
