function [errorCode, ParameterA, ParameterB, ParameterC] = PositionerCorrectorSR1ObserverAccelerationGet(socketId, PositionerName)
%PositionerCorrectorSR1ObserverAccelerationGet :  Read SR1 corrector observer parameters
%
%	[errorCode, ParameterA, ParameterB, ParameterC] = PositionerCorrectorSR1ObserverAccelerationGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr ParameterA
%		doublePtr ParameterB
%		doublePtr ParameterC


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
ParameterA = 0;
ParameterB = 0;
ParameterC = 0;

% lib call
[errorCode, PositionerName, ParameterA, ParameterB, ParameterC] = calllib('XPS_C8_drivers', 'PositionerCorrectorSR1ObserverAccelerationGet', socketId, PositionerName, ParameterA, ParameterB, ParameterC);
