function [errorCode] = PositionerCorrectorSR1OffsetAccelerationSet(socketId, PositionerName, AccelerationOffset)
%PositionerCorrectorSR1OffsetAccelerationSet :  Update SR1 corrector output acceleration offset
%
%	[errorCode] = PositionerCorrectorSR1OffsetAccelerationSet(socketId, PositionerName, AccelerationOffset)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		double AccelerationOffset
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_C8_drivers', 'PositionerCorrectorSR1OffsetAccelerationSet', socketId, PositionerName, AccelerationOffset);
