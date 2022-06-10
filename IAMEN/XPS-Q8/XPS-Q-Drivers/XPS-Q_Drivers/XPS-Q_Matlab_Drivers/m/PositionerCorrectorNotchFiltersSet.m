function [errorCode] = PositionerCorrectorNotchFiltersSet(socketId, PositionerName, NotchFrequency1, NotchBandwidth1, NotchGain1, NotchFrequency2, NotchBandwidth2, NotchGain2)
%PositionerCorrectorNotchFiltersSet :  Update filters parameters 
%
%	[errorCode] = PositionerCorrectorNotchFiltersSet(socketId, PositionerName, NotchFrequency1, NotchBandwidth1, NotchGain1, NotchFrequency2, NotchBandwidth2, NotchGain2)
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
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_Q8_drivers', 'PositionerCorrectorNotchFiltersSet', socketId, PositionerName, NotchFrequency1, NotchBandwidth1, NotchGain1, NotchFrequency2, NotchBandwidth2, NotchGain2);
