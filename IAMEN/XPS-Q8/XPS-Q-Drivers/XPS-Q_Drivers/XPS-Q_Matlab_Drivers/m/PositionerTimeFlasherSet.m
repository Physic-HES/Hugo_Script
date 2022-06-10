function [errorCode] = PositionerTimeFlasherSet(socketId, PositionerName, MinimumPosition, MaximumPosition, TimeInterval)
%PositionerTimeFlasherSet :  Set time flasher parameters
%
%	[errorCode] = PositionerTimeFlasherSet(socketId, PositionerName, MinimumPosition, MaximumPosition, TimeInterval)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		double MinimumPosition
%		double MaximumPosition
%		double TimeInterval
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_Q8_drivers', 'PositionerTimeFlasherSet', socketId, PositionerName, MinimumPosition, MaximumPosition, TimeInterval);
