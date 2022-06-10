function [errorCode, ControllerStatus] = ControllerStatusRead(socketId)
%ControllerStatusRead :  Read controller current status
%
%	[errorCode, ControllerStatus] = ControllerStatusRead(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		int32Ptr ControllerStatus


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
ControllerStatus = 0;

% lib call
[errorCode, ControllerStatus] = calllib('XPS_Q8_drivers', 'ControllerStatusRead', socketId, ControllerStatus);
