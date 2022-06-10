function [errorCode] = XYLineArcPulseOutputSet(socketId, GroupName, StartLength, EndLength, PathLengthInterval)
%XYLineArcPulseOutputSet :  Configure pulse output on trajectory
%
%	[errorCode] = XYLineArcPulseOutputSet(socketId, GroupName, StartLength, EndLength, PathLengthInterval)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		double StartLength
%		double EndLength
%		double PathLengthInterval
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, GroupName] = calllib('XPS_Q8_drivers', 'XYLineArcPulseOutputSet', socketId, GroupName, StartLength, EndLength, PathLengthInterval);
