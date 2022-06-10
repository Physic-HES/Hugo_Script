function [errorCode] = EventAdd(socketId, PositionerName, EventName, EventParameter, ActionName, ActionParameter1, ActionParameter2, ActionParameter3)
%EventAdd :  ** OBSOLETE ** Add an event
%
%	[errorCode] = EventAdd(socketId, PositionerName, EventName, EventParameter, ActionName, ActionParameter1, ActionParameter2, ActionParameter3)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		cstring EventName
%		cstring EventParameter
%		cstring ActionName
%		cstring ActionParameter1
%		cstring ActionParameter2
%		cstring ActionParameter3
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName, EventName, EventParameter, ActionName, ActionParameter1, ActionParameter2, ActionParameter3] = calllib('XPS_Q8_drivers', 'EventAdd', socketId, PositionerName, EventName, EventParameter, ActionName, ActionParameter1, ActionParameter2, ActionParameter3);
