function [errorCode] = PositionerCorrectorSR1ObserverAccelerationSet(socketId, PositionerName, ParameterA, ParameterB, ParameterC)
%PositionerCorrectorSR1ObserverAccelerationSet :  Update SR1 corrector observer parameters
%
%	[errorCode] = PositionerCorrectorSR1ObserverAccelerationSet(socketId, PositionerName, ParameterA, ParameterB, ParameterC)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		double ParameterA
%		double ParameterB
%		double ParameterC
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_C8_drivers', 'PositionerCorrectorSR1ObserverAccelerationSet', socketId, PositionerName, ParameterA, ParameterB, ParameterC);
