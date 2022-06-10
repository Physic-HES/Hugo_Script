function [errorCode, PositionerHardwareStatusString] = PositionerHardwareStatusStringGet(socketId, PositionerHardwareStatus)
%PositionerHardwareStatusStringGet :  Return the positioner hardware status string corresponding to the positioner error code
%
%	[errorCode, PositionerHardwareStatusString] = PositionerHardwareStatusStringGet(socketId, PositionerHardwareStatus)
%
%	* Input parameters :
%		int32 socketId
%		int32 PositionerHardwareStatus
%	* Output parameters :
%		int32 errorCode
%		cstring PositionerHardwareStatusString


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
PositionerHardwareStatusString = '';
for i = 1:103
	PositionerHardwareStatusString = [PositionerHardwareStatusString '          '];
end

% lib call
[errorCode, PositionerHardwareStatusString] = calllib('XPS_Q8_drivers', 'PositionerHardwareStatusStringGet', socketId, PositionerHardwareStatus, PositionerHardwareStatusString);
