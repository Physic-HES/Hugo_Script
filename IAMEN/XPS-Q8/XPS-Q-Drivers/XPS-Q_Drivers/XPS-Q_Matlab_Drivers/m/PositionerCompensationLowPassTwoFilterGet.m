function [errorCode, CutOffFrequency] = PositionerCompensationLowPassTwoFilterGet(socketId, PositionerName)
%PositionerCompensationLowPassTwoFilterGet :  Read second order low-pass filter parameters 
%
%	[errorCode, CutOffFrequency] = PositionerCompensationLowPassTwoFilterGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr CutOffFrequency


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
CutOffFrequency = 0;

% lib call
[errorCode, PositionerName, CutOffFrequency] = calllib('XPS_C8_drivers', 'PositionerCompensationLowPassTwoFilterGet', socketId, PositionerName, CutOffFrequency);
