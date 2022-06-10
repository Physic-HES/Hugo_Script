function [errorCode] = PositionerPositionCompareSet(socketId, PositionerName, MinimumPosition, MaximumPosition, PositionStep)
%PositionerPositionCompareSet :  Set position compare parameters
%
%	[errorCode] = PositionerPositionCompareSet(socketId, PositionerName, MinimumPosition, MaximumPosition, PositionStep)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		double MinimumPosition
%		double MaximumPosition
%		double PositionStep
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_Q8_drivers', 'PositionerPositionCompareSet', socketId, PositionerName, MinimumPosition, MaximumPosition, PositionStep);
