function [errorCode] = PositionerPositionCompareAquadBWindowedSet(socketId, PositionerName, MinimumPosition, MaximumPosition)
%PositionerPositionCompareAquadBWindowedSet :  Set position compare AquadB windowed parameters
%
%	[errorCode] = PositionerPositionCompareAquadBWindowedSet(socketId, PositionerName, MinimumPosition, MaximumPosition)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		double MinimumPosition
%		double MaximumPosition
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_Q8_drivers', 'PositionerPositionCompareAquadBWindowedSet', socketId, PositionerName, MinimumPosition, MaximumPosition);
