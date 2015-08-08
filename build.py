#!/usr/bin/env
import os
import urllib2
import urllib
import zipfile
import shutil
import errno
import ConfigParser
import re
import argparse
import datetime

class LatestSU:
	def __getPage(self, url, retRedirUrl=False):
		try:
			bOpener = urllib2.build_opener()
			bOpener.addheaders = [("User-agent",
								   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36")]
			pResponse = bOpener.open(url)
			if retRedirUrl == True:
				return pResponse.geturl()
			else:
				pageData = pResponse.read()
				return pageData

		except urllib2.HTTPError, e:
			print('HTTPError = ' + str(e.code))
		except urllib2.URLError, e:
			print('URLError = ' + str(e.reason))

	def dlsupersu(self):

		getUrl = self.__getPage('http://download.chainfire.eu/supersu', True)
		latestUrl = getUrl + '?retrieve_file=1'

		return latestUrl


def supersu():

	ldclass = LatestSU()
	filename = os.path.join('supersu', 'supersu.zip')

	print('Downloading supersu.zip to supersu/supersu.zip ~4MB')
	urllib.urlretrieve(ldclass.dlsupersu(), filename)

def allapps():

	apps = {
		'BlueNMEA-2.1.3':'http://max.kellermann.name/download/blue-nmea/BlueNMEA-2.1.3.apk',
		'Hackerskeyboard-1.0.3.7':'https://hackerskeyboard.googlecode.com/files/hackerskeyboard-v1037.apk',
		'VNC-20110327':'https://android-vnc-viewer.googlecode.com/files/androidVNC_build20110327.apk',
		'Drivedroid-0.9.19':'http://softwarebakery.com/apps/drivedroid/files/drivedroid-free-0.9.19.apk',
		'USBKeyboard':'https://github.com/pelya/android-keyboard-gadget/raw/master/USB-Keyboard.apk',
		'RFAnalyzer':'https://github.com/demantz/RFAnalyzer/raw/master/RFAnalyzer.apk',
		'Shodan':'https://github.com/PaulSec/Shodan.io-mobile-app/raw/master/io.shodan.app.apk',
		'Term':'http://jackpal.github.com/Android-Terminal-Emulator/downloads/Term.apk'
	}

	try:
		for key, value in apps.iteritems():
			apkname = 'data/app/' + key + '.apk'

			if not os.path.isfile(apkname): # Check for existing apk download
				print('Downloading ' + value + 'to' + apkname)
				urllib.urlretrieve (value, apkname)
		print('Finished downloading all apps')

	except urllib.URLError, e:
		print('URLError = ' + str(e.reason))

def ignore_function(ignore):
	def _ignore_(path, names):
		ignored_names = []
		if ignore in names:
			ignored_names.append(ignore)
		return set(ignored_names)
	return _ignore_



# Modified source from: http://stackoverflow.com/questions/14568647/create-zip-in-python
# and http://www.pythoncentral.io/how-to-recursively-copy-a-directory-folder-in-python/
def zip(src, dst, status):
	# Copy all folders/files (except ignored) to tmp_out folder for zipping
	try:
		pwd = os.path.dirname(os.path.realpath(__file__))
		if status == "anykernel":
			shutil.copytree(pwd, 'tmp_out', ignore=shutil.ignore_patterns('*.py', 'README', 'placeholder','tmp_out',
																	  'devices.cfg', '.DS_Store', '.git', '.idea',
																	  'aroma', 'data', 'system', 'anykernel', 'wallpaper'
																	  'supersu', 'update-nethunter*'))
		elif status == "aroma":
			shutil.copytree(pwd, 'tmp_out', ignore=shutil.ignore_patterns('*.py', 'README', 'placeholder','tmp_out',
																	  'devices.cfg', '.DS_Store', '.git', '.idea',
																	  'modules', 'anykernel.sh',
																	  'ramdisk', 'patch', 'anykernel',
																	  'zImage*', 'aroma-update', 'update-nethunter*'))

	except OSError as e:
		if e.errno == errno.ENOTDIR:
			shutil.copy(pwd, 'tmp_out')
		else:
			print('Directory not copied. Error: %s' % e)
	try:
		zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
		abs_src = os.path.abspath(src)
		for dirname, subdirs, files in os.walk(src):
			for filename in files:
				absname = os.path.abspath(os.path.join(dirname, filename))
				arcname = absname[len(abs_src) + 1:]
				print 'zipping %s as %s' % (os.path.join(dirname, filename),
											arcname)
				zf.write(absname, arcname)
		zf.close()
		shutil.rmtree('tmp_out')
	except IOError, e:
		print('Error' + str(e.reason))

def regexanykernel(device):

	i = 0

	Config = ConfigParser.ConfigParser()
	Config.read('devices.cfg')

	file = 'anykernel.sh'
	developer = Config.get('DEVELOPER', 'kernelstring')
	developer = 'kernel.string=' + developer

	# Get device names, convert to list, and get size
	devicestrings = Config.get(device, 'devicenames')
	devicestrings = devicestrings.split()
	size = len(devicestrings)

	# Get name of block to extract kernel to
	block = Config.get(device, 'block')
	block = 'block=' + block + ';'

	# Open file as read only and copy to string
	file_handle = open(file, 'r')
	file_string = file_handle.read()
	file_handle.close()

	# Replace kernel.string=name of developer in file_string
	file_string = (re.sub(ur'''kernel\.string=.*''', developer, file_string))
	file_string = (re.sub(ur'''block=.*''', block, file_string))

	# Replace device names
	for device in devicestrings:
		i += 1
		devicecode = 'device.name' + str(i) + '=' + device
		deviceregex = 'device\.name' + str(i) + '=.*'
		file_string = (re.sub(deviceregex, devicecode, file_string))

	if size < 5:
		for extranumbers in range(size, 5):
			# Else make device string empty
			extranumbers += 1
			devicecode = 'device.name' + str(extranumbers) + '=' + ""
			deviceregex = 'device\.name' + str(extranumbers) + '=.*'
			file_string = (re.sub(deviceregex, devicecode, file_string))


	file_handle = open(file, 'w')
	file_handle.write(file_string)
	file_handle.close()

def main():
	######### Start Anykernel2 installer #############

	try:
		Config = ConfigParser.ConfigParser()
		Config.read('devices.cfg')
		devicenames = Config.sections()
	except IOError:
		print('Error opening devices.cfg')

	help_device = 'Device names: \n'

	for device in devicenames:
		if device != 'DEVELOPER':
			help_device += device + '\n'

	parser = argparse.ArgumentParser(description='Nethunter zip builder')
	parser.add_argument('--device', '-d', action='store', help=help_device)
	parser.add_argument('--forcedown', '-f', action='store_true', help='Force redownloading')

	args = parser.parse_args()

	if args.forcedown:
		supersu()
		allapps()	

	if args.device in devicenames:
		device = args.device	
	elif not args.device:
		print('No arguments supplied.  Try -h or --help')
		exit(0)
	else:
		print('Device ', args.device, 'not found devices.cfg')
		exit(0)

	regexanykernel(device)

	# Grab latestest SuperSU
	suzipfile = os.path.isfile('supersu/supersu.zip')

	if os.path.isdir('supersu') and not suzipfile:
		supersu()
	elif not os.path.isdir('supersu') and not suzipfile:
		os.mkdir('supersu')
		supersu()

	# Copy anykernel update-binary to android folder for installation
	dir = 'META-INF/com/google/android/'
	if os.path.exists(dir):
		shutil.rmtree(dir)
	shutil.copytree('anykernel', dir)

	zipfilename = 'anykernel2'

	# Finished--copy files to tmp folder and zip
	zip('tmp_out', zipfilename, 'anykernel')
	if os.path.exists('anykernelzip'):
		shutil.rmtree('anykernelzip')
	os.makedirs('anykernelzip')
	shutil.move('anykernel2.zip', 'anykernelzip/anykernel2.zip')

	####### End AnyKernel2 installer ############
	
	####### Start building aroma installer ######
	if os.path.isdir('data/app'):
		allapps()
	elif not os.path.isdir('data/app'):
		os.mkdir('data/app')
		allapps()

	dir = 'META-INF/com/google/android/'

	if os.path.exists(dir):
		shutil.rmtree(dir)

	shutil.copytree('aroma-update', dir)

	# Format for zip file is update-nethunter-devicename-DDMMYY_HHMMSS.zip
	i = datetime.datetime.now()
	current_time = "%s%s%s_%s%s%s" % (i.day, i.month, i.year, i.hour, i.minute, i.second)
	zipfilename = 'update-nethunter-' + device + '-' + str(current_time)
	
	zip('tmp_out', zipfilename, 'aroma')

	# Clean up
	if os.path.exists('anykernelzip'):
		shutil.rmtree('anykernelzip')

	print('Created: ', zipfilename + '.zip')

if __name__ == "__main__":
	main()
