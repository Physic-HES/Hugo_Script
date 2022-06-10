function [errorCode, SlaveControllerStatusString] = ControllerSlaveStatusStringGet(socketId, SlaveControllerStatusCode)
%ControllerSlaveStatusStringGet :  Return the slave controller status string
%
%	[errorCode, SlaveControllerStatusString] = ControllerSlaveStatusStringGet(socketId, SlaveControllerStatusCode)
%
%	* Input parameters :
%		int32 socketId
%		int32 SlaveControllerStatusCode
%	* Output parameters :
%		int32 errorCode
%		cstring SlaveControllerStatusString


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
SlaveControllerStatusString = '';
for i = 1:103
	SlaveControllerStatusString = [SlaveControllerStatusString '          '];
end

% lib call
[errorCode, SlaveControllerStatusString] = calllib('XPS_C8_drivers', 'ControllerSlaveStatusStringGet', socketId, SlaveControllerStatusCode, SlaveControllerStatusString);
