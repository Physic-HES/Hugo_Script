function [errorCode, EventList] = EventListGet(socketId)
%EventListGet :  General event list
%
%	[errorCode, EventList] = EventListGet(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		cstring EventList


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
EventList = '';
for i = 1:205
	EventList = [EventList '          '];
end

% lib call
[errorCode, EventList] = calllib('XPS_Q8_drivers', 'EventListGet', socketId, EventList);
