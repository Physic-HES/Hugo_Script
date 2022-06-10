function [errorCode, InterpolationFactor] = PositionerHardInterpolatorFactorGet(socketId, PositionerName)
%PositionerHardInterpolatorFactorGet :  Get hard interpolator parameters
%
%	[errorCode, InterpolationFactor] = PositionerHardInterpolatorFactorGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		int32Ptr InterpolationFactor


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
InterpolationFactor = 0;

% lib call
[errorCode, PositionerName, InterpolationFactor] = calllib('XPS_Q8_drivers', 'PositionerHardInterpolatorFactorGet', socketId, PositionerName, InterpolationFactor);
