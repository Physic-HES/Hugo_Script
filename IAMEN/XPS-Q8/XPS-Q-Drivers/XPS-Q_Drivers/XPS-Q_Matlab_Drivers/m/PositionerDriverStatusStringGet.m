function [errorCode, PositionerDriverStatusString] = PositionerDriverStatusStringGet(socketId, PositionerDriverStatus)
%PositionerDriverStatusStringGet :  Return the positioner driver status string corresponding to the positioner error code
%
%	[errorCode, PositionerDriverStatusString] = PositionerDriverStatusStringGet(socketId, PositionerDriverStatus)
%
%	* Input parameters :
%		int32 socketId
%		int32 PositionerDriverStatus
%	* Output parameters :
%		int32 errorCode
%		cstring PositionerDriverStatusString


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
PositionerDriverStatusString = '';
for i = 1:103
	PositionerDriverStatusString = [PositionerDriverStatusString '          '];
end

% lib call
[errorCode, PositionerDriverStatusString] = calllib('XPS_Q8_drivers', 'PositionerDriverStatusStringGet', socketId, PositionerDriverStatus, PositionerDriverStatusString);
