function [errorCode] = PositionerCorrectorPIDDualFFVoltageSet(socketId, PositionerName, ClosedLoopStatus, KP, KI, KD, KS, IntegrationTime, DerivativeFilterCutOffFrequency, GKP, GKI, GKD, KForm, KFeedForwardVelocity, KFeedForwardAcceleration, Friction)
%PositionerCorrectorPIDDualFFVoltageSet :  Update corrector parameters
%
%	[errorCode] = PositionerCorrectorPIDDualFFVoltageSet(socketId, PositionerName, ClosedLoopStatus, KP, KI, KD, KS, IntegrationTime, DerivativeFilterCutOffFrequency, GKP, GKI, GKD, KForm, KFeedForwardVelocity, KFeedForwardAcceleration, Friction)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		int16 ClosedLoopStatus
%		double KP
%		double KI
%		double KD
%		double KS
%		double IntegrationTime
%		double DerivativeFilterCutOffFrequency
%		double GKP
%		double GKI
%		double GKD
%		double KForm
%		double KFeedForwardVelocity
%		double KFeedForwardAcceleration
%		double Friction
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_Q8_drivers', 'PositionerCorrectorPIDDualFFVoltageSet', socketId, PositionerName, ClosedLoopStatus, KP, KI, KD, KS, IntegrationTime, DerivativeFilterCutOffFrequency, GKP, GKI, GKD, KForm, KFeedForwardVelocity, KFeedForwardAcceleration, Friction);
