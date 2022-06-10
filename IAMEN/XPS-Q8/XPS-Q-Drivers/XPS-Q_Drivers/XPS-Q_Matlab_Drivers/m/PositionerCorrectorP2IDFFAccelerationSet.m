function [errorCode] = PositionerCorrectorP2IDFFAccelerationSet(socketId, PositionerName, ClosedLoopStatus, KP, KI, KI2, KD, KS, IntegrationTime, DerivativeFilterCutOffFrequency, GKP, GKI, GKD, KForm, KFeedForwardAcceleration, KFeedForwardJerk, SetpointPositionDelay)
%PositionerCorrectorP2IDFFAccelerationSet :  Update corrector parameters
%
%	[errorCode] = PositionerCorrectorP2IDFFAccelerationSet(socketId, PositionerName, ClosedLoopStatus, KP, KI, KI2, KD, KS, IntegrationTime, DerivativeFilterCutOffFrequency, GKP, GKI, GKD, KForm, KFeedForwardAcceleration, KFeedForwardJerk, SetpointPositionDelay)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		int16 ClosedLoopStatus
%		double KP
%		double KI
%		double KI2
%		double KD
%		double KS
%		double IntegrationTime
%		double DerivativeFilterCutOffFrequency
%		double GKP
%		double GKI
%		double GKD
%		double KForm
%		double KFeedForwardAcceleration
%		double KFeedForwardJerk
%		double SetpointPositionDelay
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_Q8_drivers', 'PositionerCorrectorP2IDFFAccelerationSet', socketId, PositionerName, ClosedLoopStatus, KP, KI, KI2, KD, KS, IntegrationTime, DerivativeFilterCutOffFrequency, GKP, GKI, GKD, KForm, KFeedForwardAcceleration, KFeedForwardJerk, SetpointPositionDelay);
