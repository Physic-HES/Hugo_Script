function [errorCode] = PositionerPositionCompareScanAccelerationLimitSet(socketId, PositionerName, ScanAccelerationLimit)
%PositionerPositionCompareScanAccelerationLimitSet :  Set position compare scan acceleration limit
%
%	[errorCode] = PositionerPositionCompareScanAccelerationLimitSet(socketId, PositionerName, ScanAccelerationLimit)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		double ScanAccelerationLimit
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_C8_drivers', 'PositionerPositionCompareScanAccelerationLimitSet', socketId, PositionerName, ScanAccelerationLimit);
