function [errorCode, NotchFrequency1, NotchBandwidth1, NotchGain1, NotchFrequency2, NotchBandwidth2, NotchGain2, NotchFrequency3, NotchBandwidth3, NotchGain3] = PositionerCompensationFrequencyNotchsGet(socketId, PositionerName)
%PositionerCompensationFrequencyNotchsGet :  Read frequency compensation notch filters parameters 
%
%	[errorCode, NotchFrequency1, NotchBandwidth1, NotchGain1, NotchFrequency2, NotchBandwidth2, NotchGain2, NotchFrequency3, NotchBandwidth3, NotchGain3] = PositionerCompensationFrequencyNotchsGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr NotchFrequency1
%		doublePtr NotchBandwidth1
%		doublePtr NotchGain1
%		doublePtr NotchFrequency2
%		doublePtr NotchBandwidth2
%		doublePtr NotchGain2
%		doublePtr NotchFrequency3
%		doublePtr NotchBandwidth3
%		doublePtr NotchGain3


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
NotchFrequency1 = 0;
NotchBandwidth1 = 0;
NotchGain1 = 0;
NotchFrequency2 = 0;
NotchBandwidth2 = 0;
NotchGain2 = 0;
NotchFrequency3 = 0;
NotchBandwidth3 = 0;
NotchGain3 = 0;

% lib call
[errorCode, PositionerName, NotchFrequency1, NotchBandwidth1, NotchGain1, NotchFrequency2, NotchBandwidth2, NotchGain2, NotchFrequency3, NotchBandwidth3, NotchGain3] = calllib('XPS_C8_drivers', 'PositionerCompensationFrequencyNotchsGet', socketId, PositionerName, NotchFrequency1, NotchBandwidth1, NotchGain1, NotchFrequency2, NotchBandwidth2, NotchGain2, NotchFrequency3, NotchBandwidth3, NotchGain3);
