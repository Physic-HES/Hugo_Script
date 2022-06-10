function [errorCode, ClosedLoopStatus, KP, KI, IntegrationTime] = PositionerCorrectorPIPositionGet(socketId, PositionerName)
%PositionerCorrectorPIPositionGet :  Read corrector parameters
%
%	[errorCode, ClosedLoopStatus, KP, KI, IntegrationTime] = PositionerCorrectorPIPositionGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		int16Ptr ClosedLoopStatus
%		doublePtr KP
%		doublePtr KI
%		doublePtr IntegrationTime


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
ClosedLoopStatus = 0;
KP = 0;
KI = 0;
IntegrationTime = 0;

% lib call
[errorCode, PositionerName, ClosedLoopStatus, KP, KI, IntegrationTime] = calllib('XPS_Q8_drivers', 'PositionerCorrectorPIPositionGet', socketId, PositionerName, ClosedLoopStatus, KP, KI, IntegrationTime);
