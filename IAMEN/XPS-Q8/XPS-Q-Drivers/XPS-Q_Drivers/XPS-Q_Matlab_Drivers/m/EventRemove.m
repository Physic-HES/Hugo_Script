function [errorCode] = EventRemove(socketId, PositionerName, EventName, EventParameter)
%EventRemove :  ** OBSOLETE ** Delete an event
%
%	[errorCode] = EventRemove(socketId, PositionerName, EventName, EventParameter)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		cstring EventName
%		cstring EventParameter
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName, EventName, EventParameter] = calllib('XPS_Q8_drivers', 'EventRemove', socketId, PositionerName, EventName, EventParameter);
