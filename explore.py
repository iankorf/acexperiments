import os
import re
import sys

def get_value(file, section, tag):
	sect = None
	with open(file) as fp:
		for line in fp:
			line = line.rstrip()
			if line.startswith(f'['):
				m = re.search('\[(\S+)\]', line)
				sect = m.group(1)
				continue
			if sect == section:
				m = re.search(f'{tag}=(\S+)', line)
				if m: return m.group(1)
	return None
	#raise Exception(f'{tag} not found in {section} of {file}')

def get_tires(file):
	dx = 0
	dy = 0
	with open(file) as fp:
		for line in fp:
			if line.startswith('DY_REF'):
				d = float(line.split('=')[1])
				if d > dy: dy = d
			if line.startswith('DX_REF'):
				d = float(line.split('=')[1])
				if d > dx: dx = d
	return dx, dy

def get_aero(ddir):
	wings = []
	with open(f'{ddir}/aero.ini') as fp:
		wing = {}
		for line in fp:
			if line.startswith('[WING'):
				if 'NAME' in wing: wings.append(wing)
				wing = {}
				continue
			m = re.search('(\S+)=(\S+)', line)
			if m:
				wing[m.group(1)] = m.group(2)
	
	for wing in wings:
		wing['CoL'] = get_lut(f'{ddir}/{wing["LUT_AOA_CL"]}')
		wing['CoD'] = get_lut(f'{ddir}/{wing["LUT_AOA_CD"]}')
	return wings
			
def get_lut(file):
	lut = []
	with open(file) as fp:
		for line in fp:
			line = line.rstrip()
			f = line.split('|')
			if len(f) == 2:
				lut.append(( float(f[0]), float(f[1]) ))
	return lut

for car in sys.argv[1:]: # assumes soft-link to content/cars
	cd = f'{car}/data'
	if not os.path.exists(cd): continue

	# car.ini
	file = f'{cd}/car.ini'
	mass = get_value(file, 'BASIC', 'TOTALMASS')
	inertia = get_value(file, 'BASIC', 'INERTIA') # what is this for?
	
	# aero.ini
	wings = get_aero(cd)
	
	# brakes
	file = f'{cd}/brakes.ini'
	b_torque = get_value(file, 'DATA', 'MAX_TORQUE')
	b_bias = get_value(file, 'DATA', 'FRONT_SHARE')
	
	# drivetrain
	file = f'{cd}/drivetrain.ini'
	d_type = get_value(file, 'TRACTION', 'TYPE')
	d_power = get_value(file, 'DIFFERENTIAL', 'POWER')
	d_coast = get_value(file, 'DIFFERENTIAL', 'COAST')
	d_preload = get_value(file, 'DIFFERENTIAL', 'PRELOAD')
	
	# engine
	file = f'{cd}/engine.ini'
	boost = get_value(file, 'TURBO_0', 'WASTEGATE')
	file = f'{cd}/power.lut'
	power = get_lut(file)
	max_hp = max([rpm * tq / 6300 for rpm, tq in power])
	if boost is not None: max_hp *= (1 + float(boost))
	max_hp = int(max_hp)
	
	# suspension (lots of parameters here)
	file = f'{cd}/suspensions.ini'
	wb = get_value(file, 'BASIC', 'WHEELBASE')
	cg = get_value(file, 'BASIC', 'CG_LOCATION') # % front
	
	f_tw = get_value(file, 'FRONT', 'TRACK')
	f_arb = get_value(file, 'ARB', 'FRONT')
	f_sr = get_value(file, 'FRONT', 'SPRING_RATE')
	
	r_tw = get_value(file, 'REAR', 'TRACK')
	r_arb = get_value(file, 'ARB', 'REAR')
	r_sr = get_value(file, 'REAR', 'SPRING_RATE')
	
	# tyres
	file = f'{cd}/tyres.ini'
	dx, dy = get_tires(file)
	
	print(car, d_type, mass, max_hp, cg, wb, dx, dy, r_tw, f_sr, r_sr, sep='\t')
	
	