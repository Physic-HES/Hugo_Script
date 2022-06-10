function [errorCode] = PositionerCorrectorSR1AccelerationSet(socketId, PositionerName, ClosedLoopStatus, KP, KI, KV, ObserverFrequency, CompensationGainVelocity, CompensationGainAcceleration, CompensationGainJerk)
%PositionerCorrectorSR1AccelerationSet :  Update corrector parameters
%
%	[errorCode] = PositionerCorrectorSR1AccelerationSet(socketId, PositionerName, ClosedLoopStatus, KP, KI, KV, ObserverFrequency, CompensationGainVelocity, CompensationGainAcceleration, CompensationGainJerk)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		uint16 ClosedLoopStatus
%		double KP
%		double KI
%		double KV
%		double ObserverFrequency
%		double CompensationGainVelocity
%		double CompensationGainAcceleration
%		double CompensationGainJerk
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_C8_drivers', 'PositionerCorrectorSR1AccelerationSet', socketId, PositionerName, ClosedLoopStatus, KP, KI, KV, ObserverFrequency, CompensationGainVelocity, CompensationGainAcceleration, CompensationGainJerk);
