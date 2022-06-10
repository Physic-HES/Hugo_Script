function [errorCode, ScanAccelerationLimit] = PositionerPositionCompareScanAccelerationLimitGet(socketId, PositionerName)
%PositionerPositionCompareScanAccelerationLimitGet :  Get position compare scan acceleration limit
%
%	[errorCode, ScanAccelerationLimit] = PositionerPositionCompareScanAccelerationLimitGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr ScanAccelerationLimit


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
ScanAccelerationLimit = 0;

% lib call
[errorCode, PositionerName, ScanAccelerationLimit] = calllib('XPS_C8_drivers', 'PositionerPositionCompareScanAccelerationLimitGet', socketId, PositionerName, ScanAccelerationLimit);
