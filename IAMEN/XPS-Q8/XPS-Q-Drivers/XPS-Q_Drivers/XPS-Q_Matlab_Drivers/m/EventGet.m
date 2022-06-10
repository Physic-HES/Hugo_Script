function [errorCode, EventsAndActionsList] = EventGet(socketId, PositionerName)
%EventGet :  ** OBSOLETE ** Read events and actions list
%
%	[errorCode, EventsAndActionsList] = EventGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		cstring EventsAndActionsList


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
EventsAndActionsList = '';
for i = 1:205
	EventsAndActionsList = [EventsAndActionsList '          '];
end

% lib call
[errorCode, PositionerName, EventsAndActionsList] = calllib('XPS_Q8_drivers', 'EventGet', socketId, PositionerName, EventsAndActionsList);
