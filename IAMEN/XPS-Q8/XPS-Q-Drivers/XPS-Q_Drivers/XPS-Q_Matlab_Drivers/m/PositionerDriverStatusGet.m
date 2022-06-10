function [errorCode, DriverStatus] = PositionerDriverStatusGet(socketId, PositionerName)
%PositionerDriverStatusGet :  Read positioner driver status
%
%	[errorCode, DriverStatus] = PositionerDriverStatusGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		int32Ptr DriverStatus


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
DriverStatus = 0;

% lib call
[errorCode, PositionerName, DriverStatus] = calllib('XPS_Q8_drivers', 'PositionerDriverStatusGet', socketId, PositionerName, DriverStatus);
