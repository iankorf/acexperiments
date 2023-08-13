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
		[0, 50],
		[500, 62],
		[1000, 78],
		[1500, 101],
		[2000, 113],
		[2500, 128],
		[3000, 134],
		[3500, 139],
		[4000, 143],
		[4500, 147],
		[5000, 149],
		[5500, 152],
		[6000, 149],
		[6500, 141],
		[7000, 125],
		[7500, 112]
	],
	'powerCurve': [
		[0, 0],
		[500, 4],
		[1000, 11],
		[1500, 21],
		[2000, 32],
		[2500, 45],
		[3000, 56],
		[3500, 68],
		[4000, 80],
		[4500, 93],
		[5000, 105],
		[5500, 115],
		[6000, 126],
		[6500, 130],
		[7000, 123],
		[7500, 118]
	]
}

AEROBASE = {
	'aero.ini': {
		'HEADER': {'VERSION': 2 },
		'WING_0': {
			'NAME': 'BODY', # just the name
			'CHORD': '1.0', # length in meters
			'SPAN': '1.62', # width in meters
			'POSITION': '0,0.04,0.2', # x,y,z position relative to CoG
			'LUT_AOA_CL': 'wing_body_AOA_CL.lut', # CoL lookup table
			'LUT_GH_CL': '',                      # height lift table
			'CL_GAIN': 0,                         # CoL lift multiplier
			'LUT_AOA_CD': 'wing_body_AOA_CD.lut', # CoD LUT
			'LUT_GH_CD': '',                      # height lift table
			'CD_GAIN': 1.4,                       # CoD multiplier
			'ANGLE': 0,                           # Default wing angle
			'ZONE_FRONT_CL': 0,     # CL=CL/(1.0+ZONE_0_CL*DAMAGE)
			'ZONE_FRONT_CD': 0.002, # CD=CD*(1.0+ZONE_0_CD*DAMAGE)
			'ZONE_REAR_CL':  0,     # CL=CL/(1.0+ZONE_0_CL*DAMAGE)
			'ZONE_REAR_CD':  0.002, # CD=CD*(1.0+ZONE_0_CD*DAMAGE)
			'ZONE_LEFT_CL':  0,     # CL=CL/(1.0+ZONE_0_CL*DAMAGE)
			'ZONE_LEFT_CD':  0.005, # CD=CD*(1.0+ZONE_0_CD*DAMAGE)
			'ZONE_RIGHT_CL': 0,     # CL=CL/(1.0+ZONE_0_CL*DAMAGE)
			'ZONE_RIGHT_CD': 0.005, # CD=CD*(1.0+ZONE_0_CD*DAMAGE)
		},
		'WING_1': {
			'NAME': 'FRONT',
			'CHORD': '1.0',
			'SPAN': '1.62',
			'POSITION': '0,-0.10,1.6',
			'LUT_AOA_CL': 'wing_front_AOA_CL.lut',
			'LUT_GH_CL': '',
			'CL_GAIN': 1.0, # used here, but not in body
			'LUT_AOA_CD': 'wing_front_AOA_CD.lut',
			'LUT_GH_CD': '',
			'CD_GAIN': 0,
			'ANGLE': 0,
			'ZONE_FRONT_CL': 0,
			'ZONE_FRONT_CD': 0.002,
			'ZONE_REAR_CL':  0,
			'ZONE_REAR_CD':  0.002,
			'ZONE_LEFT_CL':  0,
			'ZONE_LEFT_CD':  0.005,
			'ZONE_RIGHT_CL': 0,
			'ZONE_RIGHT_CD': 0.005,
		},
		'WING_2': {
			'NAME': 'REAR',
			'CHORD': '1.0',
			'SPAN': '1.62',
			'POSITION': '0,0.35,-1.7',
			'LUT_AOA_CL': 'wing_rear_AOA_CL.lut',
			'LUT_GH_CL': '',
			'CL_GAIN': 1.0, # used here, but not in body
			'LUT_AOA_CD': 'wing_rear_AOA_CD.lut',
			'LUT_GH_CD': '',
			'CD_GAIN': 0,
			'ANGLE': 0,
			'ZONE_FRONT_CL': 0,
			'ZONE_FRONT_CD': 0.002,
			'ZONE_REAR_CL':  0,
			'ZONE_REAR_CD':  0.002,
			'ZONE_LEFT_CL':  0,
			'ZONE_LEFT_CD':  0.005,
			'ZONE_RIGHT_CL': 0,
			'ZONE_RIGHT_CD': 0.005,
		},
	},

	'wing_body_AOA_CL.lut': {
		0	:	0
	},
	'wing_body_AOA_CD.lut': {
		-10	:	1,
		-2	:	0.52,
		-1	:	0.47,
		0	:	0.46,
		1	:	0.48,
		2	:	0.51,
		3	:	0.55,
		4	:	0.60,
		5	:	0.64,
		6	:	0.66,
		7	:	0.66,
		8	:	0.69,
		9	:	0.70,
		10	:	1,
	},
	'wing_front_AOA_CL.lut': {
		-10	:	-0.3,
		-2	:	-0.102,
		-1	:	-0.100,
		0	:	-0.098,
		1	:	-0.094,
		2	:	-0.090,
		10	:	-0.100,
	},
	'wing_front_AOA_CD.lut': {
		0	:	0
	},
	'wing_rear_AOA_CL.lut': {
		-10	:	-0.4,
		-2	:	-0.110,
		-1	:	-0.106,
		0	:	-0.100,
		1	:	-0.095,
		2	:	-0.090,
		10	:	-0.120,
	},
	'wing_rear_AOA_CD.lut': {
		0	:	0
	},
}

def write_aero(dir, aero):
	for filename in aero:
		with open(f'{dir}/{filename}', 'w') as fp:
			if filename == 'aero.ini':
				for section in aero[filename]:
						fp.write(f'[{section}]\n')
						for k, v in aero[filename][section].items():
							fp.write(f'{k}={v}\n')
						fp.write('\n')
			else:
				for deg, val in aero[filename].items():
					fp.write(f'{deg}|{val}\n')
				fp.write('\n')

def mod_aero(dir, front=0.0, rear=0.0):
	aero = copy.deepcopy(AEROBASE)

	## front aero section ##
	aero['aero.ini']['WING_1']['CHORD'] = front
	aero['aero.ini']['WING_1']['CL_GAIN'] = 1.0
	aero['aero.ini']['WING_1']['CD_GAIN'] = 1.0
	aero['aero.ini']['WING_1']['ANGLE'] = 0
	aero['wing_front_AOA_CL.lut'] = {
		-10	:	0.000,
		-2	:	0.400,
		0	:	0.400,
		2	:	0.400,
		10	:	0.000,
	}
	aero['wing_front_AOA_CD.lut'] = {
		-10	:	0.100,
		-2	:	0.002,
		0	:	0.000,
		2	:	0.002,
		10	:	0.100,
	}

	## rear aero section ##
	aero['aero.ini']['WING_2']['CHORD'] = rear
	aero['aero.ini']['WING_2']['CL_GAIN'] = 1.0
	aero['aero.ini']['WING_2']['CD_GAIN'] = 1.0
	aero['aero.ini']['WING_2']['ANGLE'] = 0
	aero['wing_rear_AOA_CL.lut'] = {
		-10	:	0.000,
		-2	:	0.300,
		0	:	0.500,
		2	:	0.500,
		10	:	0.500,
	}
	aero['wing_rear_AOA_CD.lut'] = {
		-10	:	0.300,
		-2	:	0.200,
		0	:	0.100,
		2	:	0.200,
		10	:	0.300,
	}

	write_aero(dir, aero)

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

def change(file, find, replace):
	lines = []
	with open(file) as fp:
		for line in fp.readlines():
			if line.startswith(find): line = f'{replace}\n'
			lines.append(line)
	with open(file, 'w') as fp:
		for line in lines:
			fp.write(line)

##############################

parser = argparse.ArgumentParser(description='miata.py')
parser.add_argument('root', type=str, metavar='<ac root>',
	help='assetto corsa root directory (or an alias)')
parser.add_argument('source', type=str, metavar='<source>',
	help='name of source vehicle directory (e.g. ks_mazda_miata)')
arg = parser.parse_args()


layouts = (
	# drive, cog, bbias
	('FF', 63, 76),
	('MR', 45, 64),
	('FR', 52, 68), 
)

aeros = {
	('Naked', 0, 0),
	('Split', 3, 0),
	('Wing',  0, 3),
	('Full',  3, 3),
}

power = 125

for layout, c, b in layouts:
	for aero, f, r in aeros:
		name = f'ACE-{layout}-{aero}'
		d = f'build/{name}/data'
		os.system(f'cp -r "{arg.root}"/content/cars/{arg.source} build/{name}')
		os.system(f'rm build/{name}/data.acd')
		
		# descriptions
		desc = f'Experimental: {name} {aero}'
		write_ui(f'build/{name}/ui/ui_car.json', name, desc, power)
		swap(f'{d}/car.ini', 'SCREEN_NAME=Mazda MX5 NA', f'SCREEN_NAME={name}')
		
		# FWD modifications
		if layout == 'FF': # swap a few things front-rear
			swap(f'{d}/drivetrain.ini', 'TYPE=RWD', 'TYPE=FWD')
			swap(f'{d}/suspensions.ini', 'FRONT=9502', 'FRONT=4260')
			swap(f'{d}/suspensions.ini', 'REAR=4259', 'REAR=9500')
			swap(f'{d}/data/suspensions.ini', 'TRACK=1.410', 'TRACK=1.43')
			swap(f'{d}/suspensions.ini', 'TRACK=1.427', 'TRACK=1.41')

		# power is increased
		mod_power(f'{d}/power.lut', power)

		# layout dictates center of gravity and brake bias
		swap(f'{d}/suspensions.ini', 'CG_LOCATION=0.515', f'CG_LOCATION={c/100}')
		swap(f'{d}/brakes.ini', 'FRONT_SHARE=0.67', f'FRONT_SHARE={b/100}')
		
		# tires are custom (more difference in lat and lon grip, more sticky)
		swap(f'{d}/tyres.ini', 'DX_REF=1.22', f'DX_REF={1.3 * g / 100}')
		swap(f'{d}/tyres.ini', 'DY_REF=1.21', f'DY_REF={1.2 * g / 100}')
		
		# aero: front aero weighs more but has less drag
		swap(f'{d}/car.ini', 'TOTALMASS=1080', f'TOTALMASS={int(1080 + f*20 + r*10)}')
		mod_aero(d, front=f, rear=r)
