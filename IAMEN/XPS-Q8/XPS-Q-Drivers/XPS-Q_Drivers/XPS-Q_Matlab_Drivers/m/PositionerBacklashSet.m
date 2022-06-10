function [errorCode] = PositionerBacklashSet(socketId, PositionerName, BacklashValue)
%PositionerBacklashSet :  Set backlash value
%
%	[errorCode] = PositionerBacklashSet(socketId, PositionerName, BacklashValue)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		double BacklashValue
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_Q8_drivers', 'PositionerBacklashSet', socketId, PositionerName, BacklashValue);
