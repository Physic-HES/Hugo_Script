function [errorCode, RawEncoderPosition] = PositionerRawEncoderPositionGet(socketId, PositionerName, UserEncoderPosition)
%PositionerRawEncoderPositionGet :  Get the raw encoder position
%
%	[errorCode, RawEncoderPosition] = PositionerRawEncoderPositionGet(socketId, PositionerName, UserEncoderPosition)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		double UserEncoderPosition
%	* Output parameters :
%		int32 errorCode
%		doublePtr RawEncoderPosition


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
RawEncoderPosition = 0;

% lib call
[errorCode, PositionerName, RawEncoderPosition] = calllib('XPS_Q8_drivers', 'PositionerRawEncoderPositionGet', socketId, PositionerName, UserEncoderPosition, RawEncoderPosition);
