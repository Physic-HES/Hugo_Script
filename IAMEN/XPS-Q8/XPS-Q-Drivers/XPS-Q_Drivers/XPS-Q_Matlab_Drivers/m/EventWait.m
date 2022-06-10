function [errorCode] = EventWait(socketId, PositionerName, EventName, EventParameter)
%EventWait :  ** OBSOLETE ** Wait an event
%
%	[errorCode] = EventWait(socketId, PositionerName, EventName, EventParameter)
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
[errorCode, PositionerName, EventName, EventParameter] = calllib('XPS_Q8_drivers', 'EventWait', socketId, PositionerName, EventName, EventParameter);
