function [errorCode] = PositionerUserTravelLimitsSet(socketId, PositionerName, UserMinimumTarget, UserMaximumTarget)
%PositionerUserTravelLimitsSet :  Update UserMinimumTarget and UserMaximumTarget
%
%	[errorCode] = PositionerUserTravelLimitsSet(socketId, PositionerName, UserMinimumTarget, UserMaximumTarget)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		double UserMinimumTarget
%		double UserMaximumTarget
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_Q8_drivers', 'PositionerUserTravelLimitsSet', socketId, PositionerName, UserMinimumTarget, UserMaximumTarget);
