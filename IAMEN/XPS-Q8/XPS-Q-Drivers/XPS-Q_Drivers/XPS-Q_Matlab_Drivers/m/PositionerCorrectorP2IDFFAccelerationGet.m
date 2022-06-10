function [errorCode, ClosedLoopStatus, KP, KI, KI2, KD, KS, IntegrationTime, DerivativeFilterCutOffFrequency, GKP, GKI, GKD, KForm, KFeedForwardAcceleration, KFeedForwardJerk, SetpointPositionDelay] = PositionerCorrectorP2IDFFAccelerationGet(socketId, PositionerName)
%PositionerCorrectorP2IDFFAccelerationGet :  Read corrector parameters
%
%	[errorCode, ClosedLoopStatus, KP, KI, KI2, KD, KS, IntegrationTime, DerivativeFilterCutOffFrequency, GKP, GKI, GKD, KForm, KFeedForwardAcceleration, KFeedForwardJerk, SetpointPositionDelay] = PositionerCorrectorP2IDFFAccelerationGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		int16Ptr ClosedLoopStatus
%		doublePtr KP
%		doublePtr KI
%		doublePtr KI2
%		doublePtr KD
%		doublePtr KS
%		doublePtr IntegrationTime
%		doublePtr DerivativeFilterCutOffFrequency
%		doublePtr GKP
%		doublePtr GKI
%		doublePtr GKD
%		doublePtr KForm
%		doublePtr KFeedForwardAcceleration
%		doublePtr KFeedForwardJerk
%		doublePtr SetpointPositionDelay


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
KI2 = 0;
KD = 0;
KS = 0;
IntegrationTime = 0;
DerivativeFilterCutOffFrequency = 0;
GKP = 0;
GKI = 0;
GKD = 0;
KForm = 0;
KFeedForwardAcceleration = 0;
KFeedForwardJerk = 0;
SetpointPositionDelay = 0;

% lib call
[errorCode, PositionerName, ClosedLoopStatus, KP, KI, KI2, KD, KS, IntegrationTime, DerivativeFilterCutOffFrequency, GKP, GKI, GKD, KForm, KFeedForwardAcceleration, KFeedForwardJerk, SetpointPositionDelay] = calllib('XPS_Q8_drivers', 'PositionerCorrectorP2IDFFAccelerationGet', socketId, PositionerName, ClosedLoopStatus, KP, KI, KI2, KD, KS, IntegrationTime, DerivativeFilterCutOffFrequency, GKP, GKI, GKD, KForm, KFeedForwardAcceleration, KFeedForwardJerk, SetpointPositionDelay);
