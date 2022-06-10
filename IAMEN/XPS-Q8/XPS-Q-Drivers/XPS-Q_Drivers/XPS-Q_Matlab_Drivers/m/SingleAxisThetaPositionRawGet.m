function [errorCode, RawEncoderPosition1, RawEncoderPosition2, RawEncoderPosition3] = SingleAxisThetaPositionRawGet(socketId, GroupName)
%SingleAxisThetaPositionRawGet :  Get raw encoder positions for single axis theta encoder
%
%	[errorCode, RawEncoderPosition1, RawEncoderPosition2, RawEncoderPosition3] = SingleAxisThetaPositionRawGet(socketId, GroupName)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%	* Output parameters :
%		int32 errorCode
%		doublePtr RawEncoderPosition1
%		doublePtr RawEncoderPosition2
%		doublePtr RawEncoderPosition3


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
RawEncoderPosition1 = 0;
RawEncoderPosition2 = 0;
RawEncoderPosition3 = 0;

% lib call
[errorCode, GroupName, RawEncoderPosition1, RawEncoderPosition2, RawEncoderPosition3] = calllib('XPS_Q8_drivers', 'SingleAxisThetaPositionRawGet', socketId, GroupName, RawEncoderPosition1, RawEncoderPosition2, RawEncoderPosition3);
