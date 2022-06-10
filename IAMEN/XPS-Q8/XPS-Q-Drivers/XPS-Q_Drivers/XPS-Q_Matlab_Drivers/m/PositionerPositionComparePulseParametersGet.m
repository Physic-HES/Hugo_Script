function [errorCode, PCOPulseWidth, EncoderSettlingTime] = PositionerPositionComparePulseParametersGet(socketId, PositionerName)
%PositionerPositionComparePulseParametersGet :  Get position compare PCO pulse parameters
%
%	[errorCode, PCOPulseWidth, EncoderSettlingTime] = PositionerPositionComparePulseParametersGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr PCOPulseWidth
%		doublePtr EncoderSettlingTime


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
PCOPulseWidth = 0;
EncoderSettlingTime = 0;

% lib call
[errorCode, PositionerName, PCOPulseWidth, EncoderSettlingTime] = calllib('XPS_Q8_drivers', 'PositionerPositionComparePulseParametersGet', socketId, PositionerName, PCOPulseWidth, EncoderSettlingTime);
