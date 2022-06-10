function [errorCode, ClosedLoopStatus, KP, KI, KV, ObserverFrequency, CompensationGainVelocity, CompensationGainAcceleration, CompensationGainJerk] = PositionerCorrectorSR1AccelerationGet(socketId, PositionerName)
%PositionerCorrectorSR1AccelerationGet :  Read corrector parameters
%
%	[errorCode, ClosedLoopStatus, KP, KI, KV, ObserverFrequency, CompensationGainVelocity, CompensationGainAcceleration, CompensationGainJerk] = PositionerCorrectorSR1AccelerationGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		uint16Ptr ClosedLoopStatus
%		doublePtr KP
%		doublePtr KI
%		doublePtr KV
%		doublePtr ObserverFrequency
%		doublePtr CompensationGainVelocity
%		doublePtr CompensationGainAcceleration
%		doublePtr CompensationGainJerk


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
ClosedLoopStatus = 0;
KP = 0;
KI = 0;
KV = 0;
ObserverFrequency = 0;
CompensationGainVelocity = 0;
CompensationGainAcceleration = 0;
CompensationGainJerk = 0;

% lib call
[errorCode, PositionerName, ClosedLoopStatus, KP, KI, KV, ObserverFrequency, CompensationGainVelocity, CompensationGainAcceleration, CompensationGainJerk] = calllib('XPS_C8_drivers', 'PositionerCorrectorSR1AccelerationGet', socketId, PositionerName, ClosedLoopStatus, KP, KI, KV, ObserverFrequency, CompensationGainVelocity, CompensationGainAcceleration, CompensationGainJerk);
