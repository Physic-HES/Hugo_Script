function [errorCode] = PositionerMotorOutputOffsetSet(socketId, PositionerName, PrimaryDAC1, PrimaryDAC2, SecondaryDAC1, SecondaryDAC2)
%PositionerMotorOutputOffsetSet :  Set soft (user defined) motor output DAC offsets
%
%	[errorCode] = PositionerMotorOutputOffsetSet(socketId, PositionerName, PrimaryDAC1, PrimaryDAC2, SecondaryDAC1, SecondaryDAC2)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		double PrimaryDAC1
%		double PrimaryDAC2
%		double SecondaryDAC1
%		double SecondaryDAC2
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_Q8_drivers', 'PositionerMotorOutputOffsetSet', socketId, PositionerName, PrimaryDAC1, PrimaryDAC2, SecondaryDAC1, SecondaryDAC2);
