function [errorCode, ClosedLoopStatus, KP, KI, KD, KS, IntegrationTime, DerivativeFilterCutOffFrequency, GKP, GKI, GKD, KForm, KFeedForwardVelocity, KFeedForwardAcceleration, Friction] = PositionerCorrectorPIDDualFFVoltageGet(socketId, PositionerName)
%PositionerCorrectorPIDDualFFVoltageGet :  Read corrector parameters
%
%	[errorCode, ClosedLoopStatus, KP, KI, KD, KS, IntegrationTime, DerivativeFilterCutOffFrequency, GKP, GKI, GKD, KForm, KFeedForwardVelocity, KFeedForwardAcceleration, Friction] = PositionerCorrectorPIDDualFFVoltageGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		int16Ptr ClosedLoopStatus
%		doublePtr KP
%		doublePtr KI
%		doublePtr KD
%		doublePtr KS
%		doublePtr IntegrationTime
%		doublePtr DerivativeFilterCutOffFrequency
%		doublePtr GKP
%		doublePtr GKI
%		doublePtr GKD
%		doublePtr KForm
%		doublePtr KFeedForwardVelocity
%		doublePtr KFeedForwardAcceleration
%		doublePtr Friction


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
KD = 0;
KS = 0;
IntegrationTime = 0;
DerivativeFilterCutOffFrequency = 0;
GKP = 0;
GKI = 0;
GKD = 0;
KForm = 0;
KFeedForwardVelocity = 0;
KFeedForwardAcceleration = 0;
Friction = 0;

% lib call
[errorCode, PositionerName, ClosedLoopStatus, KP, KI, KD, KS, IntegrationTime, DerivativeFilterCutOffFrequency, GKP, GKI, GKD, KForm, KFeedForwardVelocity, KFeedForwardAcceleration, Friction] = calllib('XPS_Q8_drivers', 'PositionerCorrectorPIDDualFFVoltageGet', socketId, PositionerName, ClosedLoopStatus, KP, KI, KD, KS, IntegrationTime, DerivativeFilterCutOffFrequency, GKP, GKI, GKD, KForm, KFeedForwardVelocity, KFeedForwardAcceleration, Friction);
