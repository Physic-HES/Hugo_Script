function [errorCode, ID] = EventExtendedStart(socketId)
%EventExtendedStart :  Launch the last event and action configuration and return an ID
%
%	[errorCode, ID] = EventExtendedStart(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		int32Ptr ID


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
ID = 0;

% lib call
[errorCode, ID] = calllib('XPS_Q8_drivers', 'EventExtendedStart', socketId, ID);
