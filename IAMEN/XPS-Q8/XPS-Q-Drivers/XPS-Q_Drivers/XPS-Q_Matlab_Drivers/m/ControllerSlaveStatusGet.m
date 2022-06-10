function [errorCode, SlaveControllerStatus] = ControllerSlaveStatusGet(socketId)
%ControllerSlaveStatusGet :  Read slave controller status
%
%	[errorCode, SlaveControllerStatus] = ControllerSlaveStatusGet(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		int32Ptr SlaveControllerStatus


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
SlaveControllerStatus = 0;

% lib call
[errorCode, SlaveControllerStatus] = calllib('XPS_C8_drivers', 'ControllerSlaveStatusGet', socketId, SlaveControllerStatus);
