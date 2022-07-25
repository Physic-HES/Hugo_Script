function [errorCode] = PositionerCompensationLowPassTwoFilterSet(socketId, PositionerName, CutOffFrequency)
%PositionerCompensationLowPassTwoFilterSet :  Update second order low-pass filter parameters 
%
%	[errorCode] = PositionerCompensationLowPassTwoFilterSet(socketId, PositionerName, CutOffFrequency)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		double CutOffFrequency
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_C8_drivers', 'PositionerCompensationLowPassTwoFilterSet', socketId, PositionerName, CutOffFrequency);