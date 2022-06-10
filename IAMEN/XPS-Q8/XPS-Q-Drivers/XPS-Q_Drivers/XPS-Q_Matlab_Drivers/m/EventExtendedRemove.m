function [errorCode] = EventExtendedRemove(socketId, ID)
%EventExtendedRemove :  Remove the event and action configuration defined by ID
%
%	[errorCode] = EventExtendedRemove(socketId, ID)
%
%	* Input parameters :
%		int32 socketId
%		int32 ID
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode] = calllib('XPS_Q8_drivers', 'EventExtendedRemove', socketId, ID);
