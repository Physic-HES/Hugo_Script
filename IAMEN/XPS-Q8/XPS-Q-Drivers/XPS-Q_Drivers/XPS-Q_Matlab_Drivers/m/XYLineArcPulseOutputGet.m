function [errorCode, StartLength, EndLength, PathLengthInterval] = XYLineArcPulseOutputGet(socketId, GroupName)
%XYLineArcPulseOutputGet :  Get pulse output on trajectory configuration
%
%	[errorCode, StartLength, EndLength, PathLengthInterval] = XYLineArcPulseOutputGet(socketId, GroupName)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%	* Output parameters :
%		int32 errorCode
%		doublePtr StartLength
%		doublePtr EndLength
%		doublePtr PathLengthInterval


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
StartLength = 0;
EndLength = 0;
PathLengthInterval = 0;

% lib call
[errorCode, GroupName, StartLength, EndLength, PathLengthInterval] = calllib('XPS_Q8_drivers', 'XYLineArcPulseOutputGet', socketId, GroupName, StartLength, EndLength, PathLengthInterval);
