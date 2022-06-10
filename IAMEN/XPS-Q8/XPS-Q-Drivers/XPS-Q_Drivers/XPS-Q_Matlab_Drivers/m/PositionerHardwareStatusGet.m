function [errorCode, HardwareStatus] = PositionerHardwareStatusGet(socketId, PositionerName)
%PositionerHardwareStatusGet :  Read positioner hardware status
%
%	[errorCode, HardwareStatus] = PositionerHardwareStatusGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		int32Ptr HardwareStatus


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
HardwareStatus = 0;

% lib call
[errorCode, PositionerName, HardwareStatus] = calllib('XPS_Q8_drivers', 'PositionerHardwareStatusGet', socketId, PositionerName, HardwareStatus);
