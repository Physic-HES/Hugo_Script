function [errorCode] = PositionerCompensationFrequencyNotchsSet(socketId, PositionerName, NotchFrequency1, NotchBandwidth1, NotchGain1, NotchFrequency2, NotchBandwidth2, NotchGain2, NotchFrequency3, NotchBandwidth3, NotchGain3)
%PositionerCompensationFrequencyNotchsSet :  Update frequency compensation notch filters parameters 
%
%	[errorCode] = PositionerCompensationFrequencyNotchsSet(socketId, PositionerName, NotchFrequency1, NotchBandwidth1, NotchGain1, NotchFrequency2, NotchBandwidth2, NotchGain2, NotchFrequency3, NotchBandwidth3, NotchGain3)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		double NotchFrequency1
%		double NotchBandwidth1
%		double NotchGain1
%		double NotchFrequency2
%		double NotchBandwidth2
%		double NotchGain2
%		double NotchFrequency3
%		double NotchBandwidth3
%		double NotchGain3
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_C8_drivers', 'PositionerCompensationFrequencyNotchsSet', socketId, PositionerName, NotchFrequency1, NotchBandwidth1, NotchGain1, NotchFrequency2, NotchBandwidth2, NotchGain2, NotchFrequency3, NotchBandwidth3, NotchGain3);
