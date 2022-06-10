function [errorCode, PrimaryDAC1, PrimaryDAC2, SecondaryDAC1, SecondaryDAC2] = PositionerMotorOutputOffsetGet(socketId, PositionerName)
%PositionerMotorOutputOffsetGet :  Get soft (user defined) motor output DAC offsets
%
%	[errorCode, PrimaryDAC1, PrimaryDAC2, SecondaryDAC1, SecondaryDAC2] = PositionerMotorOutputOffsetGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr PrimaryDAC1
%		doublePtr PrimaryDAC2
%		doublePtr SecondaryDAC1
%		doublePtr SecondaryDAC2


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
PrimaryDAC1 = 0;
PrimaryDAC2 = 0;
SecondaryDAC1 = 0;
SecondaryDAC2 = 0;

% lib call
[errorCode, PositionerName, PrimaryDAC1, PrimaryDAC2, SecondaryDAC1, SecondaryDAC2] = calllib('XPS_Q8_drivers', 'PositionerMotorOutputOffsetGet', socketId, PositionerName, PrimaryDAC1, PrimaryDAC2, SecondaryDAC1, SecondaryDAC2);
