function [errorCode, AccelerationOffset] = PositionerCorrectorSR1OffsetAccelerationGet(socketId, PositionerName)
%PositionerCorrectorSR1OffsetAccelerationGet :  Read SR1 corrector output acceleration offset
%
%	[errorCode, AccelerationOffset] = PositionerCorrectorSR1OffsetAccelerationGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr AccelerationOffset


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
AccelerationOffset = 0;

% lib call
[errorCode, PositionerName, AccelerationOffset] = calllib('XPS_C8_drivers', 'PositionerCorrectorSR1OffsetAccelerationGet', socketId, PositionerName, AccelerationOffset);
