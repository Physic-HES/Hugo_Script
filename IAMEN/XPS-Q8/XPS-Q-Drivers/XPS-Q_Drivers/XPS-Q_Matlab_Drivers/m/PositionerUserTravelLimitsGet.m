function [errorCode, UserMinimumTarget, UserMaximumTarget] = PositionerUserTravelLimitsGet(socketId, PositionerName)
%PositionerUserTravelLimitsGet :  Read UserMinimumTarget and UserMaximumTarget
%
%	[errorCode, UserMinimumTarget, UserMaximumTarget] = PositionerUserTravelLimitsGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr UserMinimumTarget
%		doublePtr UserMaximumTarget


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
UserMinimumTarget = 0;
UserMaximumTarget = 0;

% lib call
[errorCode, PositionerName, UserMinimumTarget, UserMaximumTarget] = calllib('XPS_Q8_drivers', 'PositionerUserTravelLimitsGet', socketId, PositionerName, UserMinimumTarget, UserMaximumTarget);
