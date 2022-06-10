function [errorCode] = PositionerCorrectorPIPositionSet(socketId, PositionerName, ClosedLoopStatus, KP, KI, IntegrationTime)
%PositionerCorrectorPIPositionSet :  Update corrector parameters
%
%	[errorCode] = PositionerCorrectorPIPositionSet(socketId, PositionerName, ClosedLoopStatus, KP, KI, IntegrationTime)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		int16 ClosedLoopStatus
%		double KP
%		double KI
%		double IntegrationTime
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_Q8_drivers', 'PositionerCorrectorPIPositionSet', socketId, PositionerName, ClosedLoopStatus, KP, KI, IntegrationTime);
