function [errorCode] = PositionerPositionComparePulseParametersSet(socketId, PositionerName, PCOPulseWidth, EncoderSettlingTime)
%PositionerPositionComparePulseParametersSet :  Set position compare PCO pulse parameters
%
%	[errorCode] = PositionerPositionComparePulseParametersSet(socketId, PositionerName, PCOPulseWidth, EncoderSettlingTime)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		double PCOPulseWidth
%		double EncoderSettlingTime
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_Q8_drivers', 'PositionerPositionComparePulseParametersSet', socketId, PositionerName, PCOPulseWidth, EncoderSettlingTime);
