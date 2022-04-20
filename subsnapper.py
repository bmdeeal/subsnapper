#!/usr/bin/env python3

"""
	subsnapper - take screenshots of a video with subs
	(C) 2022 B.M.Deeal
	subsnapper is distributed under the terms of the ISC License, see the provided license.txt or visit <https://opensource.org/licenses/ISC> for details.
	
	subsnapper requires ffmpeg in the $PATH to run. subsnapper has been tested under Python 3.8.5, running on Ubuntu 20.04 under WSL1.
	
	Note that as of this writing, subsnapper is currently EXTREMELY alpha and DOES NOT WORK.

	plan:
	* read [events] section
	* load start+end, use floor average (so we aren't caught out by transitions)
	* clear duplicates
	* run ffmpeg for every line

	TODO:
	* finish tests
	* split tests to separate file
	* handle calling ffmpeg

	possible TODO:
	* ability to specify skip regions (eg, OP/ED, credits)
	* rate limiting (we fold duplicate time codes, but we should also rate limit)

"""
import subprocess, math

def testResult(test_name, test_value=0, expected_value=0):
	"""
	Check if a test passes or not.
	Returns 1 on success (since it is added to a running counter), 0 on failure.
	"""
	if test_value==expected_value:
		print(f"Test '{test_name}' passed.")
		return 1
	else:
		print("error: test '{test_name}' failed! Expected '{expected_value}', got '{test_value}'!")
		return 0

def tests_decodeTime():
	"""
	Test time string decoding.
	TODO: error handling test?
	"""
	test_time="1:23:45.67"
	test_value=decodeTime(test_time)
	expected_value=502567
	return testResult("decodeTime", test_value, expected_value)

def tests_getTimes():
	"""
	Test decoding a list of event data.
	TODO: there are events other than Dialogue: that I should probably test, but I need to actually look into that
	"""
	test_data=[]
	test_data.append(["Format:","Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"])
	test_data.append( "0,0:00:10.24,0:00:14.30,Default,,0000,0000,0000,,Okay, let's go.")
	test_data.append(["Dialogue:", "0,0:00:10.24,0:00:20.00,Heading,,0000,0000,0000,,Sign: Karaoke hours: 4pm to midnight"])
	test_data.append(["Dialogue:",  "0,0:00:15.23,0:00:20.30,Default,,0000,0000,0000,,Alright, I'm coming."])
	test_data.append(["Dialogue:",  "0,0:00:22.68,0:00:28.11,Default,,0000,0000,0000,,You better hurry!"])
	print("error: test 'tests_getTimes' not implemented!")
	return 0

def testRunAll():
	"""
	Run each test.
	Tests are done as follows:
		passed+=TEST_FUNCTION(); total+=1
	where TEST_FUNCTION() is the function to test.
	TODO: refactor all these tests out
	"""
	print("Running all tests...")
	total=0
	passed=0
	#run and tally tests
	passed+=tests_decodeTime(); total+=1
	passed+=tests_getTimes(); total+=1
	print(f"{passed} of {total} tests passed.")

def decodeTime(data):
	"""
	Returns a single number in centiseconds for a given time string, such as 366101 for "1:01:01.01". The format is H:MM:SS.CC where H is hours, M is minutes, S is seconds, and C is centiseconds.
	All parts of the timestamp are mandatory.
	Malformed data is currently accepted (such as "15:0:94.2"), but this may change, and it is currently undefined what it will parse to.
	Raises a ValueError if the string's format is bad.
	"""
	#split off just the centiseconds
	#TODO: should I accept time strings without them?
	try:
		components=data.strip().split(".")
		centiseconds=int(components[1])
		components=components[0].split(":")
		centiseconds+=int(components[-1])*100 #seconds
		centiseconds+=int(components[-2])*60*100 #minutes
		centiseconds+=int(components[-3])*60*60*100 #hours
	except:
		raise ValueError(f"Invalid time string '{data}'!")
	return centiseconds

def getTimes(data):
	"""
	Generate a list of timestamps.
	[0] is the numeric version, [1] is the text version
	pulls out the order from the format line, which MUST be the first one.
	Raises a ValueError if there is an error parsing the data.
	"""
	#make sure the Format: section is is the first line
	if data[0][0]!="Format":
		raise ValueError("Data does not start with 'Format:' section!")
	#read the format, look for Start and End
	data_format=[line.strip() for line in data[0][1].split(",")]
	#extract and decode the start and end

def loadSubs(filename):
	"""
	Read in the [Events] section of a file.
	Each line is a list.
	[0] is the event type, [1] is the event data
	Raises OSError for if there is an error during load.
	"""
	#read each line, clean out whitespace and blanks
	with open(filename) as file:
		#strip+load each line
		lines=[line.strip() for line in file.readlines()]
	#grab the [Events] section
	#TODO: replace with an index() call
	for ii in range(0,len(lines)-1):
		if lines[ii]=="[Events]":
			lines=lines[ii+1:]
			break
	#stop at any other section
	for ii in range(0,len(lines)-1):
		if lines[ii]!="" and lines[ii][0]=="[":
			lines=lines[:ii]
			break
	#TODO: pretty sure there's a way to combine these, I haven't messed with list comprehensions in a while
	#as it stands now, it's ugly
	#split each event type
	lines=[line.split(":",1) for line in lines if line!=""]
	#strip each event
	lines=[[line[0],line[1].strip()] for line in lines if len(line)==2]
	return lines

def main():
	"""
	Main entry point.
	Currently very unfinished.
	"""
	file_data=loadSubs("input.ass")
	for line in file_data:
		print(line)
	getTimes(file_data)
	#loadSubs("input.ass")

if __name__=="__main__":
	testRunAll()
	#main()
